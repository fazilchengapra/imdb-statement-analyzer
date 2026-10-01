from pydantic import BaseModel

class ReviewReq(BaseModel):
    review:str
