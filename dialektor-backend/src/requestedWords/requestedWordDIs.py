from common.database import queryMany, queryOne, updateMany
from requestedWords import RequestedWord
from uuid import UUID, uuid4


def insertRequestedWord(
    word: str,
    country: UUID,
    requestedBy: str,
    variant: str | None = None,
    region: UUID | None = None,
) -> RequestedWord | None:
    sql = """
        INSERT INTO requested_words(id, word, variant, country, region, requested_by)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, word, variant, country, region, requested_by;
    """
    result = queryOne(sql, (uuid4(), word, variant, country, region, requestedBy))
    if result is None:
        return None

    return RequestedWord(
        id=result["id"],
        word=result["word"],
        variant=result["variant"],
        country=result["country"],
        region=result["region"],
        requestedBy=result["requested_by"],
    )


def selectRequestedWords() -> list[RequestedWord]:
    sql = """
        SELECT id, word, variant, country, region, requested_by
        FROM requested_words;
    """
    result = queryMany(sql)
    return [
        RequestedWord(
            id=row["id"],
            word=row["word"],
            variant=row["variant"],
            country=row["country"],
            region=row["region"],
            requestedBy=row["requested_by"],
        )
        for row in result
    ]


def selectRequestedWord(id: UUID) -> RequestedWord | None:
    sql = """
        SELECT id, word, variant, country, region, requested_by
        FROM requested_words
        WHERE id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return RequestedWord(
        id=result["id"],
        word=result["word"],
        variant=result["variant"],
        country=result["country"],
        region=result["region"],
        requestedBy=result["requested_by"],
    )


def updateRequestedWord(
    id: UUID,
    word: str,
    variant: str | None,
    country: UUID,
    region: UUID | None,
    requestedBy: str,
) -> RequestedWord | None:
    sql = """
        UPDATE requested_words
        SET
            word = %s,
            variant = %s,
            country = %s,
            region = %s,
            requested_by = %s
        WHERE id = %s
        RETURNING id, word, variant, country, region, requested_by;
    """
    result = queryOne(sql, (word, variant, country, region, requestedBy, id))
    if result is None:
        return None

    return RequestedWord(
        id=result["id"],
        word=result["word"],
        variant=result["variant"],
        country=result["country"],
        region=result["region"],
        requestedBy=result["requested_by"],
    )


def deleteRequestedWord(id: UUID) -> UUID:
    sql = """
        DELETE FROM requested_words
        WHERE id = %s;
    """
    updateMany(sql, (id,))

    return id
