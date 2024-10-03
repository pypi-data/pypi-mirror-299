from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr

from fastapi_users_pelicanq import exceptions, models, schemas
from fastapi_users_pelicanq.manager import BaseUserManager, UserManagerDependency
from fastapi_users_pelicanq.router.common import ErrorCode, ErrorModel

class RequestVerifyBody(BaseModel):
    email: EmailStr
    
class VerifyBody(BaseModel):
    token: str
    
def get_verify_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
):
    router = APIRouter()

    @router.post(
        "/request-verify-token",
        status_code=status.HTTP_202_ACCEPTED,
        name="verify:request-token",
    )
    async def request_verify_token(
        request: Request,
        body: RequestVerifyBody,
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        email = body.email
        try:
            user = await user_manager.get_by_email(email)
            await user_manager.request_verify(user, request)
        except (
            exceptions.UserNotExists,
            exceptions.UserInactive,
            exceptions.UserAlreadyVerified,
        ):
            pass

        return None

    @router.post(
        "/verify",
        response_model=user_schema,
        name="verify:verify",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.VERIFY_USER_BAD_TOKEN: {
                                "summary": "Bad token, not existing user or"
                                "not the e-mail currently set for the user.",
                                "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                            },
                            ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                                "summary": "The user is already verified.",
                                "value": {
                                    "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                                },
                            },
                        }
                    }
                },
            }
        },
    )
    async def verify(
        request: Request,
        body: VerifyBody,
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        token = body.token
        try:
            user = await user_manager.verify(token, request)
            return schemas.model_validate(user_schema, user)
        except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )
        except exceptions.UserAlreadyVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )

    return router
