from uuid import UUID, uuid4
from test.common import queryOne


def generateVersion(id: UUID | None = None, version: UUID | None = None) -> dict:
    sql = """
        INSERT INTO versions(id, version)
        VALUES(%s, %s)
        RETURNING id, version;
    """
    result = queryOne(sql, (id or uuid4(), version or uuid4()))
    assert result is not None

    return {
        "id": result["id"],
        "version": result["version"],
    }


def generateCountry(id: UUID | None = None, name: UUID | str | None = None) -> dict:
    sql = """
        INSERT INTO countries(id, name)
        VALUES(%s, %s)
        RETURNING id, name;
    """
    result = queryOne(
        sql,
        (
            id or uuid4(),
            name or uuid4(),
        ),
    )
    assert result is not None

    return {
        "id": result["id"],
        "name": result["name"],
    }


def generateRegion(
    id: UUID | None = None, name: UUID | str | None = None, country: UUID | None = None
) -> dict:
    sql = """
        INSERT INTO regions(id, name, country)
        VALUES(%s, %s, %s)
        RETURNING id, name, country;
    """
    result = queryOne(
        sql,
        (id or uuid4(), name or uuid4(), country or generateCountry()["id"]),
    )
    assert result is not None

    return {"id": result["id"], "name": result["name"], "country": result["country"]}


def generateLanguage(
    id: UUID | None = None, name: str | None = None, script: str | None = None
) -> dict:
    sql = """
        INSERT INTO languages(id, name, script)
        VALUES(%s, %s, %s)
        RETURNING id, name, script;
    """
    result = queryOne(
        sql,
        (id or uuid4(), name or uuid4(), script or "LATIN"),
    )
    assert result is not None

    return {
        "id": result["id"],
        "name": result["name"],
        "script": result["script"],
    }


def generateDialect(
    id: UUID | None = None, name: UUID | None = None, languageId: UUID | None = None
) -> dict:
    sql = """
        INSERT INTO dialects(id, name, language_id)
        VALUES(%s, %s, %s)
        RETURNING id, name, language_id;
    """
    result = queryOne(
        sql,
        (id or uuid4(), name or uuid4(), languageId or generateLanguage()["id"]),
    )
    assert result is not None

    return {
        "id": result["id"],
        "name": result["name"],
        "language_id": result["language_id"],
    }


def generateBaseWord(
    id: UUID | None = None, word: str | None = None, languageId: UUID | None = None
) -> dict:
    sql = """
        INSERT INTO base_words(id, word, language_id)
        VALUES(%s, %s, %s)
        RETURNING id, word, language_id;
    """
    result = queryOne(
        sql,
        (id or uuid4(), word or str(uuid4()), languageId or generateLanguage()["id"]),
    )
    assert result is not None

    return {
        "id": result["id"],
        "word": result["word"],
        "language_id": result["language_id"],
    }
