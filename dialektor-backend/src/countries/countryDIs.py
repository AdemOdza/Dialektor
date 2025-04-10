from common.database import queryMany, queryOne, slots, updateMany
from countries import Country
from uuid import UUID, uuid4


def insertCountry(name: str) -> Country:
    sql = f"""
        INSERT INTO countries(id, name)
        VALUES ({slots(2)})
        RETURNING id, name;
    """
    result = queryOne(
        sql,
        (
            uuid4(),
            name,
        ),
    )

    return Country(id=result["id"], name=result["name"])


def selectCountries() -> list[Country]:
    rows = queryMany("SELECT * FROM countries;")
    return [Country(id=row["id"], name=row["name"]) for row in rows]


def selectCountryByID(id: UUID) -> Country | None:
    sql = """
        SELECT *
        FROM countries
        WHERE id = %s;
    """
    result = queryOne(sql, (id,))
    if result is None:
        return None

    return Country(id=result["id"], name=result["name"])


def updateCountry(id: UUID, name: str) -> Country:
    sql = f"""
        UPDATE 
            countries
        SET 
            name = %s
        WHERE 
            id = %s
        RETURNING 
            id, name;
    """
    result = queryOne(sql, (name, id))

    return Country(id=result["id"], name=result["name"])


def deleteCountry(id: UUID) -> UUID:
    sql = """
        DELETE FROM countries
        WHERE id = %s
        RETURNING id;
    """
    updateMany(sql, (id,))
