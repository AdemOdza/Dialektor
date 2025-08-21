from uuid import UUID, uuid4
from common.database import slots, queryOne, queryMany, updateOne, updateMany
from regions import Region


def selectRegions() -> list[Region]:
    sql = """
        SELECT 
            id,
            name,
            country
        FROM
            regions;
    """
    result = queryMany(sql)
    return [
        *map(
            lambda row: Region(id=row["id"], name=row["name"], country=row["country"]),
            result,
        )
    ]


def selectRegionById(regionId: UUID) -> Region | None:
    sql = """
        SELECT 
            id,
            name,
            country
        FROM
            regions
        WHERE
            id = %s;
    """

    result = queryOne(sql, (regionId,))

    if result is None:
        return None

    return Region(id=result["id"], name=result["name"], country=result["country"])


def selectRegionsByCountryId(countryId: UUID) -> list[Region]:
    sql = """
        SELECT 
            id,
            name,
            country
        FROM
            regions
        WHERE
            country = %s;
    """

    result = queryMany(sql, (countryId,))
    return [
        *map(
            lambda row: Region(id=row["id"], name=row["name"], country=row["country"]),
            result,
        )
    ]


def insertRegion(countryId: UUID, name: str) -> Region | None:
    sql = """
        INSERT INTO regions(id, country, name)
        VALUES (%s, %s, %s)
        RETURNING id, country, name;
    """
    result = queryOne(sql, (uuid4(), countryId, name))

    if result is None:
        return None

    return Region(
        id=result["id"],
        country=result["country"],
        name=result["name"],
    )


def updateRegion(regionId: UUID, countryId: UUID, name: str) -> list[Region] | None:
    sql = """
        UPDATE regions
        SET
            country = %s,
            name = %s
        WHERE id = %s
        RETURNING id, country, name;
    """
    result = queryMany(sql, (countryId, name, regionId))
    if result is None:
        return None

    return [
        *map(
            lambda row: Region(id=row["id"], name=row["name"], country=row["country"]),
            result,
        )
    ]


def deleteRegion(regionId: UUID) -> Region | None:
    sql = """
        DELETE FROM regions
        WHERE id = %s
        RETURNING id, country, name;
    """
    result = queryOne(sql, (regionId,))
    if result is None:
        return None

    return Region(
        id=result["id"],
        country=result["country"],
        name=result["name"],
    )
