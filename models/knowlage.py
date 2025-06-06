
from pydantic import BaseModel, Field

class KnowlageSearchModel(BaseModel):
    company: str = Field(default="investa")
    q: str = Field(..., min_length=10, description="q is required")