from typing import Any
import psycopg
from psycopg.rows import dict_row

# TODO: Set up environment variable system for pytest
dbHost = "localhost"
dbPort = "5432"
dbUser = "postgres"
dbPassword = "postgres"
dbName = "postgres"

connString = f"postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"


def _query(
    sql: str,
    params: tuple[Any, ...] = None,
    asDict=True,
    fetchOne=False,
    dbConnection: psycopg.Connection = None,
) -> list[tuple[Any, ...]] | tuple[Any, ...]:
    # Set prepare_threshold to 0 to prepare every statement

    with psycopg.connect(
        conninfo=connString, row_factory=dict_row if asDict else None
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params=params, prepare=True)
            func = cur.fetchone if fetchOne else cur.fetchall
            return func()


def _transact(
    sql: str,
    params: tuple[Any, ...] = None,
    asDict=True,
    fetchOne=False,
    dbConnection: psycopg.Connection = None,
) -> bool:
    # Set prepare_threshold to 0 to prepare every statement

    try:
        with psycopg.connect(
            conninfo=connString,
            prepare_threshold=0,
            row_factory=dict_row if asDict else None,
        ) as conn:
            with conn.cursor() as cur:
                with conn.transaction() as trx:
                    cur.execute(sql, params=params, prepare=True)
        return True
    except:
        return False


def queryOne(sql: str, params: tuple[Any, ...] = None):
    return _query(sql, params, fetchOne=True)


def queryMany(sql: str, params: tuple[Any, ...] = None):
    return _query(sql, params, fetchOne=False)


def update(sql: str, params: tuple[Any, ...] = None):
    _transact(sql, params)


def truncate_db():
    update(f"TRUNCATE TABLE versions CASCADE;")
    update(f"TRUNCATE TABLE languages CASCADE;")
    update(f"TRUNCATE TABLE countries CASCADE;")
    update(f"TRUNCATE TABLE regions CASCADE;")
    update(f"TRUNCATE TABLE dialects CASCADE;")
    update(f"TRUNCATE TABLE base_words CASCADE;")
    update(f"TRUNCATE TABLE word_variants CASCADE;")
    update(f"TRUNCATE TABLE requested_words CASCADE;")
    update(f"TRUNCATE TABLE users CASCADE;")
    update(f"TRUNCATE TABLE session_tokens CASCADE;")
