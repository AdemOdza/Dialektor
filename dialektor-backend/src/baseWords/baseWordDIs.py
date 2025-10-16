from common.database import queryMany, queryOne, updateMany
from baseWords import BaseWord
from uuid import UUID, uuid4


def insertBaseWord(word: str, languageId: UUID) -> BaseWord | None:
    sql = """
        INSERT INTO base_words(id, word, language_id)
        VALUES (%s, %s, %s)
        RETURNING id, word, language_id;
    """
    result = queryOne(
        sql,
        (
            uuid4(),
            word,
            languageId,
        ),
    )

    if result is None:
        return None

    return BaseWord(
        id=result["id"], word=result["word"], languageId=result["language_id"]
    )


def selectBaseWords() -> list[BaseWord]:
    sql = f"""
        SELECT
            id, word, language_id
        FROM
            base_words;
    """
    result = queryMany(sql)

    return [
        *map(
            lambda row: BaseWord(
                id=row["id"], word=row["word"], languageId=row["language_id"]
            ),
            result,
        )
    ]


def selectBaseWordByLanguage(id: UUID, languageId: UUID) -> BaseWord | None:
    sql = """
        SELECT
            bw.id, bw.word, l.id as language_id
        FROM
            base_words bw RIGHT JOIN languages l ON bw.language_id=l.id
        WHERE
            bw.id = %s AND l.id = %s;
    """
    result = queryOne(sql, (id, languageId))

    if result is None:
        return None

    return BaseWord(
        id=result["id"], word=result["word"], languageId=result["language_id"]
    )


def selectBaseWordsByLanguage(languageId: UUID) -> list[BaseWord]:
    sql = """
        SELECT
            bw.id, bw.word, l.id as language_id
        FROM
            base_words bw RIGHT JOIN languages l ON bw.language_id=l.id
        WHERE l.id = %s;
    """
    result = queryMany(sql, (languageId,))

    return [
        *map(
            lambda row: BaseWord(
                id=row["id"], word=row["word"], languageId=row["language_id"]
            ),
            result,
        )
    ]


def selectBaseWord(id: UUID) -> BaseWord | None:
    sql = f"""
        SELECT
            id, word, language_id
        FROM
            base_words
        WHERE 
            id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return BaseWord(
        id=result["id"], word=result["word"], languageId=result["language_id"]
    )


def updateBaseWord(id: UUID, word: str, languageId: UUID) -> BaseWord | None:
    sql = f"""
        UPDATE 
            base_words
        SET 
            word = %s,
            language_id = %s
        WHERE 
            id = %s
        RETURNING 
            id, word, language_id;
    """
    result = queryOne(sql, (word, languageId, id))
    if result is None:
        return None

    return BaseWord(
        id=result["id"], word=result["word"], languageId=result["language_id"]
    )


def deleteBaseWord(id: UUID) -> UUID:
    sql = """
        DELETE FROM base_words
        WHERE id = %s;
    """
    # TODO: Removed returning, see if that causes issues
    updateMany(sql, (id,))

    return id
