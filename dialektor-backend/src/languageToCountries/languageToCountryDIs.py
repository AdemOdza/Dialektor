from common.database import queryMany, queryOne, updateMany
from languageToCountries import LanguageToCountry
from uuid import UUID


def insertLanguageToCountry(
    countryId: UUID, languageId: UUID, official: bool = False
) -> LanguageToCountry | None:
    sql = """
        INSERT INTO language_to_countries(country_id, language_id, official)
        VALUES (%s, %s, %s)
        RETURNING country_id, language_id, official;
    """
    result = queryOne(sql, (countryId, languageId, official))
    if result is None:
        return None

    return LanguageToCountry(
        countryId=result["country_id"],
        languageId=result["language_id"],
        official=result["official"],
    )


def selectLanguageToCountries() -> list[LanguageToCountry]:
    sql = """
        SELECT country_id, language_id, official
        FROM language_to_countries;
    """
    result = queryMany(sql)
    return [
        LanguageToCountry(
            countryId=row["country_id"],
            languageId=row["language_id"],
            official=row["official"],
        )
        for row in result
    ]


def selectCountriesByLanguage(languageId: UUID) -> list[LanguageToCountry]:
    sql = """
        SELECT country_id, language_id, official
        FROM language_to_countries
        WHERE language_id = %s;
    """
    result = queryMany(sql, (languageId,))
    return [
        LanguageToCountry(
            countryId=row["country_id"],
            languageId=row["language_id"],
            official=row["official"],
        )
        for row in result
    ]


def selectLanguagesByCountry(countryId: UUID) -> list[LanguageToCountry]:
    sql = """
        SELECT country_id, language_id, official
        FROM language_to_countries
        WHERE country_id = %s;
    """
    result = queryMany(sql, (countryId,))
    return [
        LanguageToCountry(
            countryId=row["country_id"],
            languageId=row["language_id"],
            official=row["official"],
        )
        for row in result
    ]


def updateLanguageToCountry(
    countryId: UUID, languageId: UUID, official: bool
) -> LanguageToCountry | None:
    sql = """
        UPDATE language_to_countries
        SET official = %s
        WHERE country_id = %s AND language_id = %s
        RETURNING country_id, language_id, official;
    """
    result = queryOne(sql, (official, countryId, languageId))
    if result is None:
        return None

    return LanguageToCountry(
        countryId=result["country_id"],
        languageId=result["language_id"],
        official=result["official"],
    )


def deleteLanguageToCountry(countryId: UUID, languageId: UUID) -> bool:
    sql = """
        DELETE FROM language_to_countries
        WHERE country_id = %s AND language_id = %s;
    """
    return updateMany(sql, (countryId, languageId)) or False
