from common.database import queryMany, updateMany, updateOne
from scripts import Script


def selectScripts() -> list[Script]:
    sql = """
        SELECT name FROM scripts;
    """
    result = queryMany(sql)
    return [*map(lambda x: Script(name=x["name"]), result)]


def deleteScript(name: str):
    sql = """
        DELETE FROM 
            scripts 
        WHERE LOWER(name)=LOWER(%s)
        RETURNING name;
    """
    updateMany(sql, (name,))


def insertScript(name: str) -> str:
    sql = """
        INSERT INTO 
            scripts(name) 
        VALUES 
            (%s)
        RETURNING name;
    """
    result = updateOne(sql, (name,))
    return Script(name=result["name"])
