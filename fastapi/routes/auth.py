from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from security.jwt import USUARIO_ADMIN, gerar_token
from security.rate_limit import LIMITE_AUTENTICACAO, limiter


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/token")
@limiter.limit(LIMITE_AUTENTICACAO)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):

    if (
        form_data.username != USUARIO_ADMIN["username"]
        or form_data.password != USUARIO_ADMIN["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    token = gerar_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }