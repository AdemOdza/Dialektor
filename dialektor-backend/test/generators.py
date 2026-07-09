from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
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


def generateWordVariant(
    id: UUID | None = None,
    word: str | None = None,
    baseWord: UUID | None = None,
    dialect: UUID | None = None,
) -> dict:
    sql = """
        INSERT INTO word_variants(id, word, base_word, dialect)
        VALUES(%s, %s, %s, %s)
        RETURNING id, word, base_word, dialect;
    """
    result = queryOne(
        sql,
        (
            id or uuid4(),
            word or str(uuid4()),
            baseWord or generateBaseWord()["id"],
            dialect or generateDialect()["id"],
        ),
    )
    assert result is not None

    return {
        "id": result["id"],
        "word": result["word"],
        "base_word": result["base_word"],
        "dialect": result["dialect"],
    }


def generateRequestedWord(
    id: UUID | None = None,
    word: str | None = None,
    variant: str | None = None,
    country: UUID | None = None,
    region: UUID | None = None,
    requestedBy: str | None = None,
) -> dict:
    sql = """
        INSERT INTO requested_words(id, word, variant, country, region, requested_by)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING id, word, variant, country, region, requested_by;
    """
    result = queryOne(
        sql,
        (
            id or uuid4(),
            word or str(uuid4()),
            variant,
            country or generateCountry()["id"],
            region,
            requestedBy or "testuser",
        ),
    )
    assert result is not None

    return {
        "id": result["id"],
        "word": result["word"],
        "variant": result["variant"],
        "country": result["country"],
        "region": result["region"],
        "requested_by": result["requested_by"],
    }


def generateUser(
    id: UUID | None = None,
    username: str | None = None,
    email: str | None = None,
    defaultDialect: UUID | None = None,
    passwordHash: str | None = None,
) -> dict:
    sql = """
        INSERT INTO users(id, username, email, default_dialect, password_hash)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id, username, email, default_dialect, password_hash;
    """
    result = queryOne(
        sql,
        (
            id or uuid4(),
            username or f"user_{uuid4().hex[:8]}",
            email or f"{uuid4().hex[:8]}@test.com",
            defaultDialect,
            passwordHash or "hashed_password_placeholder",
        ),
    )
    assert result is not None

    return {
        "id": result["id"],
        "username": result["username"],
        "email": result["email"],
        "default_dialect": result["default_dialect"],
        "password_hash": result["password_hash"],
    }


def generateSessionToken(
    id: UUID | None = None,
    userId: UUID | None = None,
    token: str | None = None,
    expires: datetime | None = None,
) -> dict:
    sql = """
        INSERT INTO session_tokens(id, user_id, token, expires)
        VALUES(%s, %s, %s, %s)
        RETURNING id, user_id, token, expires;
    """
    result = queryOne(
        sql,
        (
            id or uuid4(),
            userId or generateUser()["id"],
            token or str(uuid4()),
            expires or (datetime.now(timezone.utc) + timedelta(hours=24)),
        ),
    )
    assert result is not None

    return {
        "id": result["id"],
        "user_id": result["user_id"],
        "token": result["token"],
        "expires": result["expires"],
    }


def generateLanguageToCountry(
    countryId: UUID | None = None,
    languageId: UUID | None = None,
    official: bool = False,
) -> dict:
    sql = """
        INSERT INTO language_to_countries(country_id, language_id, official)
        VALUES(%s, %s, %s)
        RETURNING country_id, language_id, official;
    """
    result = queryOne(
        sql,
        (
            countryId or generateCountry()["id"],
            languageId or generateLanguage()["id"],
            official,
        ),
    )
    assert result is not None

    return {
        "country_id": result["country_id"],
        "language_id": result["language_id"],
        "official": result["official"],
    }
