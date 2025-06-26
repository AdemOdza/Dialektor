from uuid import UUID, uuid4
from test.common import queryOne


def generateVersion(id: UUID | None = None, version: UUID | None = None) -> dict:
    sql = """
        INSERT INTO versions(id, version)
        VALUES(%s, %s)
        RETURNING id, version;
    """
    return queryOne(sql, (id or uuid4(), version or uuid4()))


def generateCountry(id: UUID | None = None, name: UUID | str | None = None) -> dict:
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


def generateLanguage(
    id: UUID | None = None, name: UUID | None = None, script: str | None = None
):
    sql = """
        INSERT INTO languages(id, name, script)
        VALUES(%s, %s, %s)
        RETURNING id, name, script;
    """
    return queryOne(
        sql,
        (id or uuid4(), name or uuid4(), script or "LATIN"),
    )


def generateDialect(
    id: UUID | None = None, name: UUID | None = None, languageId: UUID | None = None
):
    sql = """
        INSERT INTO dialects(id, name, language_id)
        VALUES(%s, %s, %s)
        RETURNING id, name, language_id;
    """
    return queryOne(
        sql,
        (id or uuid4(), name or uuid4(), languageId or generateLanguage()["id"]),
    )
