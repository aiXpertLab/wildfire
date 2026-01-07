from pydantic import BaseModel

class HumanQuery(BaseModel):
    query: str
    top_k: int = 50

class ResultString(BaseModel):
    result: str


class ResultList(BaseModel):
    results: list[dict]  # list of dicts from SQL query
    
    