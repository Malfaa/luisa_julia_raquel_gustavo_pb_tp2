from pydantic import BaseModel, ConfigDict


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str


class PredictResponse(BaseModel):
    message: str
    intent: str

