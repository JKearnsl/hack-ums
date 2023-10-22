import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi.requests import Request
from fastapi.responses import Response

from src.dependencies.services import get_services
from src.models import schemas
from src.models.file_type import FileType
from src.services import ServiceFactory
from src.views import SessionsResponse

from src.views.user import UserResponse, UserSmallResponse, UserDocumentResponse
from src.views.s3 import S3UploadResponse

router = APIRouter()


@router.get("", response_model=UserResponse, status_code=http_status.HTTP_200_OK)
async def get_current_user(services: ServiceFactory = Depends(get_services)):
    """
    Получить модель текущего пользователя

    Требуемые права доступа: GET_SELF

    Состояние: ACTIVE
    """
    return UserResponse(content=await services.user.get_self())


@router.put("", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_current_user(data: schemas.UserUpdate, services: ServiceFactory = Depends(get_services)):
    """
    Обновить данные текущего пользователя

    Требуемые права доступа: UPDATE_SELF

    Состояние: ACTIVE
    """
    await services.user.update_self(data)


@router.put("/password", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_password(old_password: str, new_password: str, services: ServiceFactory = Depends(get_services)):
    """
    Обновить пароль текущего пользователя

    Требуемые права доступа: UPDATE_SELF

    Состояние: ACTIVE

    """
    await services.user.update_password(old_password, new_password)


@router.delete("", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_current_user(
        password: str,
        request: Request,
        response: Response,
        services: ServiceFactory = Depends(get_services)
):
    """
    Удалить текущего пользователя

    Требуемые права доступа: DELETE_SELF, LOGOUT

    Состояние: ACTIVE
    """
    await services.user.delete_self(password)
    await services.auth.logout(request, response)


@router.get("/session/list", response_model=SessionsResponse, status_code=http_status.HTTP_200_OK)
async def get_self_sessions(services: ServiceFactory = Depends(get_services)):
    """
    Получить список сессий текущего пользователя

    Требуемые права доступа: GET_SELF_SESSIONS

    Состояние: ACTIVE
    """
    return SessionsResponse(content=await services.user.get_self_sessions())


@router.get("/session/list/{user_id}", response_model=SessionsResponse, status_code=http_status.HTTP_200_OK)
async def get_user_sessions(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    """
    Получить список сессий пользователя по id

    Требуемые права доступа: GET_USER_SESSIONS

    Состояние: ACTIVE
    """
    return SessionsResponse(content=await services.user.get_user_sessions(user_id))


@router.get("/document", response_model=UserDocumentResponse, status_code=http_status.HTTP_200_OK)
async def get_document_url(services: ServiceFactory = Depends(get_services)):
    """
    Получить URL своего документа

    Требуемые права доступа: GET_SELF

    Состояние: ACTIVE
    """
    return UserDocumentResponse(content=await services.user.get_self_document_url())


@router.get("/document/{user_id}", response_model=UserDocumentResponse, status_code=http_status.HTTP_200_OK)
async def get_document_url(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    """
    Получить URL пользовательского документа по id

    Требуемые права доступа: GET_USER
    """
    return UserDocumentResponse(content=await services.user.get_user_document_url(user_id))


@router.put("/document", response_model=S3UploadResponse, status_code=http_status.HTTP_200_OK)
async def update_document(file_type: FileType, services: ServiceFactory = Depends(get_services)):
    """
    Обновить документ текущего пользователя

    Выпускается временный url для загрузки файла

    Требуемые права доступа: UPDATE_SELF

    Состояние: ACTIVE
    """
    return S3UploadResponse(content=await services.user.update_document(file_type))


@router.put("/document/{user_id}", response_model=S3UploadResponse, status_code=http_status.HTTP_200_OK)
async def update_user_document(user_id: uuid.UUID, file_type: FileType, services: ServiceFactory = Depends(get_services)):
    """
    Обновить документ пользователя по id

    Выпускается временный url для загрузки файла

    Требуемые права доступа: UPDATE_USER

    Состояние: ACTIVE

    """
    return S3UploadResponse(content=await services.user.update_user_document(user_id, file_type))


@router.delete("/session", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_current_session(session_id: str, services: ServiceFactory = Depends(get_services)):
    """
    Удалить свою сессию по id

    Требуемые права доступа: DELETE_SELF_SESSION

    Состояние: ACTIVE
    """
    await services.user.delete_self_session(session_id)


@router.delete("/session/{user_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user_session(user_id: uuid.UUID, session_id: str, services: ServiceFactory = Depends(get_services)):
    """
    Удалить сессию пользователя по id

    Требуемые права доступа: DELETE_USER_SESSION

    Состояние: ACTIVE
    """
    await services.user.delete_user_session(user_id, session_id)


@router.get("/{user_id}", response_model=UserSmallResponse, status_code=http_status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    """
    Получить модель пользователя по id

    Требуемые права доступа: GET_USER
    """
    return UserSmallResponse(content=await services.user.get_user(user_id))


@router.put("/{user_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
        user_id: uuid.UUID,
        data: schemas.UserUpdateByAdmin,
        services: ServiceFactory = Depends(get_services)
):
    """
    Обновить данные пользователя по id

    Требуемые права доступа: UPDATE_USER

    Состояние: ACTIVE
    """
    await services.user.update_user(user_id, data)
