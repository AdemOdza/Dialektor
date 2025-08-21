from uuid import UUID, uuid4
from dialects import Dialect
from common.database import queryMany, queryOne, updateOne, slots


def insertDialect(languageId: UUID, name: str) -> Dialect | None:
    sql = """
        INSERT INTO dialects(id, language_id, name)
        VALUES (%s, %s, %s)
        RETURNING id, language_id, name;
    """

    result = queryOne(
        sql,
        (
            uuid4(),
            languageId,
            name,
        ),
    )
    if result is None:
        return None

    return Dialect(
        id=result["id"], languageId=result["language_id"], name=result["name"]
    )


def selectDialects() -> list[Dialect]:
    sql = """
        SELECT id, language_id, name
        FROM dialects;
    """

    result = queryMany(sql)
    return [
        *map(
            lambda row: Dialect(
                id=row["id"], languageId=row["language_id"], name=row["name"]
            ),
            result,
        )
    ]


def selectDialectById(id: UUID) -> Dialect | None:
    sql = """
        SELECT id, language_id, name
        FROM dialects
        WHERE id = %s;
    """

    result = queryOne(sql, (id,))
    if result is None:
        return None
    return Dialect(
        id=result["id"], languageId=result["language_id"], name=result["name"]
    )


def selectDialectsByLanguage(languageId: UUID) -> list[Dialect]:
    sql = """
        SELECT id, language_id, name
        FROM dialects
        WHERE language_id = %s;
    """

    result = queryMany(sql, (languageId,))
    return [
        *map(
            lambda row: Dialect(
                id=row["id"], languageId=row["language_id"], name=row["name"]
            ),
            result,
        )
    ]


def updateDialect(id: UUID, languageId: UUID, name: str) -> Dialect | None:
    # ID and Language ID composite key. Name should be the only thing that changes
    sql = """
        UPDATE dialects
        SET name = %s
        WHERE id = %s AND language_id = %s
        RETURNING id, language_id, name;
    """

    result = queryOne(
        sql,
        (
            name,
            id,
            languageId,
        ),
    )
    if result is None:
        return None

    return Dialect(
        id=result["id"], languageId=result["language_id"], name=result["name"]
    )


def deleteDialect(id: UUID, languageId: UUID) -> Dialect | None:
    sql = """
        DELETE FROM dialects
        WHERE id = %s AND language_id = %s
        RETURNING id, language_id, name;
    """

    result = queryOne(
        sql,
        (
            id,
            languageId,
        ),
    )
    if result is None:
        return None

    return Dialect(
        id=result["id"], languageId=result["language_id"], name=result["name"]
    )
