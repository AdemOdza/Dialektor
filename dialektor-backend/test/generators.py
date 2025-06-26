from uuid import UUID, uuid4
from test.common import queryOne


def generateVersion(id: UUID | None = None, version: UUID | None = None) -> dict:
    sql = """
        INSERT INTO versions(id, version)
        VALUES(%s, %s)
        RETURNING id, version;
    """
    return queryOne(sql, (id or uuid4(), version or uuid4()))


def generateCountry(id: UUID | None = None, name: UUID | None = None) -> dict:
    sql = """
        INSERT INTO countries(id, name)
        VALUES(%s, %s)
        RETURNING id, name;
    """
    return queryOne(
        sql,
        (
            id or uuid4(),
            name or uuid4(),
        ),
    )
