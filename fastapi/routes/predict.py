from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models.schemas import PredictRequest, PredictResponse
from models.database_models import User, Prediction
from database import get_session
from security.jwt import validar_token_jwt


predict_router = APIRouter()


@predict_router.post("/predict", response_model=PredictResponse)
async def predict(
    data: PredictRequest,
    username: str = Depends(validar_token_jwt)
):
    texto = data.message.lower()

    if "reembolso" in texto:
        intent = "refund"
    else:
        intent = "general_support"

    return {"intent": intent}


@predict_router.get("/predict/{prediction_id}")
async def get_prediction(
    prediction_id: int,
    username: str = Depends(validar_token_jwt),
    session: Session = Depends(get_session)
):
    usuario = session.exec(
        select(User).where(User.username == username)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    prediction = session.exec(
        select(Prediction).where(
            Prediction.id == prediction_id,
            Prediction.owner_id == usuario.id
        )
    ).first()

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction não encontrada"
        )

    return prediction

