from uuid import UUID, uuid4
from languages import Language
from common.database import queryMany, queryOne, updateMany, updateOne, slots


def selectLanguages() -> list[Language]:
    sql = """
        SELECT 
            id,
            name,
            script
        FROM languages;
    """
    result = queryMany(sql)
    return [
        *map(
            lambda row: Language(
                id=row["id"],
                name=row["name"],
                script=row["script"],
            ),
            result,
        )
    ]


def selectLanguageByID(id: UUID) -> Language | None:
    sql = """
        SELECT 
            id,
            name,
            script
        FROM languages
        WHERE id=%s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return Language(id=result["id"], name=result["name"], script=result["script"])


def insertLanguage(name: str, script: str) -> Language:
    sql = f"""
        INSERT INTO languages(id, name, script)
        VALUES ({slots(3)})
        RETURNING id, name, script;
    """
    result = updateOne(sql, (uuid4(), name, script.upper()))
    if result is None:
        return None

    return Language(id=result["id"], name=result["name"], script=result["script"])


def updateLanguage(id: UUID, name: str, script: str) -> Language:
    sql = f"""
        UPDATE languages
        SET
            name = %s,
            script = %s
        WHERE id = %s
        RETURNING id, name, script;
    """
    result = updateOne(sql, (name, script.upper(), id))
    if result is None:
        return None

    return Language(id=result["id"], name=result["name"], script=result["script"])


def deleteLanguage(id: UUID) -> UUID:
    sql = """
        DELETE FROM languages
        WHERE id = %s
        RETURNING id;
    """
    updateMany(sql, (id,))

    return id
