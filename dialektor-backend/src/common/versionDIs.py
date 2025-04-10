from common.database import queryOne


def selectVersion():
    sql = """
        SELECT * FROM versions;
    """

    return queryOne(sql)
