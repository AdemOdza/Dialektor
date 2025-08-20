from typing import Any, LiteralString, Optional
import psycopg
from psycopg.rows import dict_row
from common import getEnv


def slots(numSlots: int) -> str:
    return ", ".join(["%s" for i in range(0, numSlots)])


dbHost = getEnv("DATABASE_HOST", "localhost")
dbPort = getEnv("DATABASE_PORT", "5432")
dbUser = getEnv("DATABASE_USER", "postgres")
dbPassword = getEnv("DATABASE_PASSWORD", "postgres")
dbName = getEnv("DATABASE_NAME", "postgres")

connString = f"postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"


def _query(
    sql: LiteralString,
    params: Optional[tuple[Any, ...]] = None,
    asDict=True,
    fetchOne=False,
    dbConnection: Optional[psycopg.Connection] = None,
) -> dict | list[dict] | None:
    # Set prepare_threshold to 0 to prepare every statement

    with psycopg.connect(conninfo=connString) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params=params, prepare=True)
            func = cur.fetchone if fetchOne else cur.fetchall
            return func()


def _transact(
    sql: LiteralString,
    params: Optional[tuple[Any, ...]] = None,
    asDict=True,
    fetchOne=False,
    dbConnection: Optional[psycopg.Connection] = None,
) -> bool:
    # Set prepare_threshold to 0 to prepare every statement

    try:
        with psycopg.connect(
            conninfo=connString,
            prepare_threshold=0,
        ) as conn:
            with conn.cursor() as cur:
                with conn.transaction() as trx:
                    cur.execute(sql, params=params, prepare=True)
        return True
    except:
        return False


def queryOne(
    sql: LiteralString, params: Optional[tuple[Any, ...]] = None
) -> dict | None:
    result = _query(sql, params, fetchOne=True)
    if isinstance(result, list):
        return result[0] if result else None
    return result


def queryMany(
    sql: LiteralString, params: Optional[tuple[Any, ...]] = None
) -> list[dict]:
    result = _query(sql, params, fetchOne=False)
    if isinstance(result, dict):
        return [result]
    return result or []


def updateOne(
    sql: LiteralString, params: Optional[tuple[Any, ...]] = None
) -> bool | None:
    return _transact(sql, params, fetchOne=True)


def updateMany(
    sql: LiteralString, params: Optional[tuple[Any, ...]] = None
) -> bool | None:
    return _transact(sql, params, fetchOne=False)
