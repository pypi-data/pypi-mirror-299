from sqlalchemy import func

from threedi_schema.domain import models
from threedi_schema.infrastructure.spatialite_versions import (
    copy_model,
    get_spatialite_version,
)


def test_get_spatialite_version(empty_sqlite_v3):
    lib_version, file_version = get_spatialite_version(empty_sqlite_v3)
    assert lib_version in (3, 4, 5)
    assert file_version == 3


def test_copy_model(empty_sqlite_v3, empty_sqlite_v4):
    db_from = empty_sqlite_v3
    db_to = empty_sqlite_v4

    # Add a record to 'db_from'
    obj = models.ConnectionNode(
        id=3, code="test", the_geom="SRID=4326;POINT(-71.064544 42.287870)"
    )
    with db_from.session_scope() as session:
        session.add(obj)
        session.commit()

    # Copy it
    copy_model(db_from, db_to, models.ConnectionNode)

    # Check if it is present in 'db_to'
    with db_to.session_scope() as session:
        records = list(
            session.query(
                models.ConnectionNode.id,
                models.ConnectionNode.code,
                func.ST_AsText(models.ConnectionNode.the_geom),
            )
        )

        assert records == [(3, "test", "POINT(-71.064544 42.28787)")]


def test_copy_invalid_geometry(empty_sqlite_v3, empty_sqlite_v4):
    """Copying an invalid geometry (ST_IsValid evaluates to False) is possible"""
    db_from = empty_sqlite_v3
    db_to = empty_sqlite_v4
    # Note MP: this only works when this object is not involved in a migratin
    # This may cause issues with future database upgrades
    obj = models.GridRefinementArea(
        id=3,
        code="test",
        display_name="test",
        the_geom="SRID=4326;POLYGON((0 0, 10 10, 0 10, 10 0, 0 0))",
        refinement_level=1,
    )
    with db_from.session_scope() as session:
        session.add(obj)
        session.commit()

    copy_model(db_from, db_to, models.GridRefinementArea)

    with db_to.session_scope() as session:
        records = list(
            session.query(
                models.GridRefinementArea.id,
                func.ST_AsText(models.GridRefinementArea.the_geom),
            )
        )

        assert records == [(3, "POLYGON((0 0, 10 10, 0 10, 10 0, 0 0))")]
