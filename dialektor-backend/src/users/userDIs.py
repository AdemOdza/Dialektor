from common.database import queryMany, queryOne, updateMany
from users import User
from uuid import UUID, uuid4


def insertUser(
    username: str, email: str, passwordHash: str, defaultDialect: UUID | None = None
) -> User | None:
    sql = """
        INSERT INTO users(id, username, email, default_dialect, password_hash)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, default_dialect, password_hash;
    """
    result = queryOne(sql, (uuid4(), username, email, defaultDialect, passwordHash))
    if result is None:
        return None

    return User(
        id=result["id"],
        username=result["username"],
        email=result["email"],
        defaultDialect=result["default_dialect"],
        passwordHash=result["password_hash"],
    )


def selectUsers() -> list[User]:
    sql = """
        SELECT id, username, email, default_dialect, password_hash
        FROM users;
    """
    result = queryMany(sql)
    return [
        User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            defaultDialect=row["default_dialect"],
            passwordHash=row["password_hash"],
        )
        for row in result
    ]


def selectUserByID(id: UUID) -> User | None:
    sql = """
        SELECT id, username, email, default_dialect, password_hash
        FROM users
        WHERE id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return User(
        id=result["id"],
        username=result["username"],
        email=result["email"],
        defaultDialect=result["default_dialect"],
        passwordHash=result["password_hash"],
    )


def updateUser(
    id: UUID, username: str, email: str, defaultDialect: UUID | None
) -> User | None:
    sql = """
        UPDATE users
        SET
            username = %s,
            email = %s,
            default_dialect = %s
        WHERE id = %s
        RETURNING id, username, email, default_dialect, password_hash;
    """
    result = queryOne(sql, (username, email, defaultDialect, id))
    if result is None:
        return None

    return User(
        id=result["id"],
        username=result["username"],
        email=result["email"],
        defaultDialect=result["default_dialect"],
        passwordHash=result["password_hash"],
    )


def deleteUser(id: UUID) -> UUID:
    sql = """
        DELETE FROM users
        WHERE id = %s;
    """
    updateMany(sql, (id,))

    return id
