from common.database import queryMany, queryOne, updateMany
from wordVariants import WordVariant
from uuid import UUID, uuid4


def insertWordVariant(word: str, baseWord: UUID, dialect: UUID) -> WordVariant | None:
    sql = """
        INSERT INTO word_variants(id, word, base_word, dialect)
        VALUES (%s, %s, %s, %s)
        RETURNING id, word, base_word, dialect;
    """
    result = queryOne(sql, (uuid4(), word, baseWord, dialect))
    if result is None:
        return None

    return WordVariant(
        id=result["id"],
        word=result["word"],
        baseWord=result["base_word"],
        dialect=result["dialect"],
    )


def selectWordVariants() -> list[WordVariant]:
    sql = """
        SELECT id, word, base_word, dialect
        FROM word_variants;
    """
    result = queryMany(sql)
    return [
        WordVariant(
            id=row["id"],
            word=row["word"],
            baseWord=row["base_word"],
            dialect=row["dialect"],
        )
        for row in result
    ]


def selectWordVariant(id: UUID) -> WordVariant | None:
    sql = """
        SELECT id, word, base_word, dialect
        FROM word_variants
        WHERE id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return WordVariant(
        id=result["id"],
        word=result["word"],
        baseWord=result["base_word"],
        dialect=result["dialect"],
    )


def selectWordVariantsByBaseWord(baseWordId: UUID) -> list[WordVariant]:
    sql = """
        SELECT id, word, base_word, dialect
        FROM word_variants
        WHERE base_word = %s;
    """
    result = queryMany(sql, (baseWordId,))
    return [
        WordVariant(
            id=row["id"],
            word=row["word"],
            baseWord=row["base_word"],
            dialect=row["dialect"],
        )
        for row in result
    ]


def selectWordVariantsByDialect(dialectId: UUID) -> list[WordVariant]:
    sql = """
        SELECT id, word, base_word, dialect
        FROM word_variants
        WHERE dialect = %s;
    """
    result = queryMany(sql, (dialectId,))
    return [
        WordVariant(
            id=row["id"],
            word=row["word"],
            baseWord=row["base_word"],
            dialect=row["dialect"],
        )
        for row in result
    ]


def updateWordVariant(
    id: UUID, word: str, baseWord: UUID, dialect: UUID
) -> WordVariant | None:
    sql = """
        UPDATE word_variants
        SET
            word = %s,
            base_word = %s,
            dialect = %s
        WHERE id = %s
        RETURNING id, word, base_word, dialect;
    """
    result = queryOne(sql, (word, baseWord, dialect, id))
    if result is None:
        return None

    return WordVariant(
        id=result["id"],
        word=result["word"],
        baseWord=result["base_word"],
        dialect=result["dialect"],
    )


def deleteWordVariant(id: UUID) -> UUID:
    sql = """
        DELETE FROM word_variants
        WHERE id = %s;
    """
    updateMany(sql, (id,))

    return id
