import re
from sqlalchemy import text

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|grant|revoke|merge)\b",
    re.IGNORECASE,
)

ALLOWED_TABLES = {"innov"}
DEFAULT_LIMIT = 50
MAX_LIMIT = 200


class SQLGuardError(ValueError):
    pass


def guard_sql(sql: str) -> str:
    if not sql:
        raise SQLGuardError("Empty SQL")

    s = sql.strip().rstrip(";")
    lower = s.lower()

    # 1. SELECT-only
    if not lower.startswith("select"):
        raise SQLGuardError("Only SELECT statements are allowed")

    # 2. Block forbidden keywords
    if FORBIDDEN_KEYWORDS.search(lower):
        raise SQLGuardError("Forbidden SQL keyword detected")

    # 3. Table whitelist
    if not any(f" from {t} " in f" {lower} " for t in ALLOWED_TABLES):
        raise SQLGuardError("Query references non-whitelisted tables")

    # 4. Enforce LIMIT
    if " limit " not in f" {lower} ":
        s = f"{s} LIMIT {DEFAULT_LIMIT}"
    else:
        # cap excessive limits
        s = re.sub(
            r"limit\s+(\d+)",
            lambda m: f"LIMIT {min(int(m.group(1)), MAX_LIMIT)}",
            s,
            flags=re.IGNORECASE,
        )

    return s
