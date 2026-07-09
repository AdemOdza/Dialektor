from common.database import queryMany, queryOne, updateMany
from sessionTokens import SessionToken
from datetime import datetime
from uuid import UUID, uuid4


def insertSessionToken(
    userId: UUID, token: str, expires: datetime
) -> SessionToken | None:
    sql = """
        INSERT INTO session_tokens(id, user_id, token, expires)
        VALUES (%s, %s, %s, %s)
        RETURNING id, user_id, token, expires;
    """
    result = queryOne(sql, (uuid4(), userId, token, expires))
    if result is None:
        return None

    return SessionToken(
        id=result["id"],
        userId=result["user_id"],
        token=result["token"],
        expires=result["expires"],
    )


def selectSessionTokens() -> list[SessionToken]:
    sql = """
        SELECT id, user_id, token, expires
        FROM session_tokens;
    """
    result = queryMany(sql)
    return [
        SessionToken(
            id=row["id"],
            userId=row["user_id"],
            token=row["token"],
            expires=row["expires"],
        )
        for row in result
    ]


def selectSessionToken(id: UUID) -> SessionToken | None:
    sql = """
        SELECT id, user_id, token, expires
        FROM session_tokens
        WHERE id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return SessionToken(
        id=result["id"],
        userId=result["user_id"],
        token=result["token"],
        expires=result["expires"],
    )


def selectSessionTokensByUser(userId: UUID) -> list[SessionToken]:
    sql = """
        SELECT id, user_id, token, expires
        FROM session_tokens
        WHERE user_id = %s;
    """
    result = queryMany(sql, (userId,))
    return [
        SessionToken(
            id=row["id"],
            userId=row["user_id"],
            token=row["token"],
            expires=row["expires"],
        )
        for row in result
    ]


def deleteSessionToken(id: UUID) -> UUID:
    sql = """
        DELETE FROM session_tokens
        WHERE id = %s;
    """
    updateMany(sql, (id,))

    return id


def deleteExpiredTokens() -> bool:
    sql = """
        DELETE FROM session_tokens
        WHERE expires < NOW();
    """
    return updateMany(sql) or False
