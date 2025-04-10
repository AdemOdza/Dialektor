from typing import Any
import psycopg
from psycopg.rows import dict_row

# TODO: Set up environment variable system for pytest
dbHost = 'localhost'
dbPort = '5432'
dbUser = 'postgres'
dbPassword = 'postgres'
dbName = 'postgres'

connString = f'postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}'

def _query(sql: str, params: tuple[Any, ...] = None, asDict = True, fetchOne = False, dbConnection: psycopg.Connection = None) -> list[tuple[Any, ...]] | tuple[Any, ...]:
    # Set prepare_threshold to 0 to prepare every statement
    if dbConnection is not None:
        with dbConnection as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params = params, prepare = True)
                func = (cur.fetchone if fetchOne else cur.fetchall)
            return func()

    with psycopg.connect(
        conninfo=connString,
        row_factory= dict_row if asDict else None
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params = params, prepare = True)
            func = (cur.fetchone if fetchOne else cur.fetchall)
            return func()
        
def _transact(sql: str, params: tuple[Any, ...] = None, asDict = True, fetchOne = False, dbConnection: psycopg.Connection = None) -> list[tuple[Any, ...]] | tuple[Any, ...]:
    # Set prepare_threshold to 0 to prepare every statement
    if dbConnection is not None:
        with dbConnection as conn:
            with conn.cursor() as cur:
                with conn.transaction() as trx:
                    trx.execute(sql, params = params, prepare = True)
                    func = (trx.fetchone if fetchOne else trx.fetchall)
                    return func()
    
    with psycopg.connect(
        conninfo=connString,
        prepare_threshold=0, 
        row_factory= dict_row if asDict else None
    ) as conn:
        with conn.cursor() as cur:
            with conn.transaction() as trx:
                trx.execute(sql, params = params, prepare = True)
                func = (trx.fetchone if fetchOne else trx.fetchall)
                return func()
        
def queryOne(sql: str, params: tuple[Any, ...] = None):
    return _query(sql, params, fetchOne = True)

def queryMany(sql: str, params: tuple[Any, ...] = None):
    return _query(sql, params, fetchOne = False)

def updateOne(sql: str, params: tuple[Any, ...] = None):
    return _transact(sql, params, fetchOne = True)

def updateMany(sql: str, params: tuple[Any, ...] = None):
    return _transact(sql, params, fetchOne = False)