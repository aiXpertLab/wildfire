from pydantic import BaseModel

class AllRequestString(BaseModel):
    query: str



class AgentResponseString(BaseModel):
    answer: str

class SQLAgentResponseList(BaseModel):
    results: list[dict]  # list of dicts from SQL query