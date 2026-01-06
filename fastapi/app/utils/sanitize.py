import re

def clean_sql(sql: str) -> str:
    sql = sql.strip()

    # Remove ```sql ``` blocks
    sql = re.sub(r"^```[\w]*", "", sql)
    sql = re.sub(r"```$", "", sql)

    # Remove leading language tag like "sql\n"
    sql = re.sub(r"^\s*sql\s*\n", "", sql, flags=re.IGNORECASE)

    return sql.strip()
