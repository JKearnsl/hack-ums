from .base import BaseView
from src.models import schemas


class UserResponse(BaseView):
    content: schemas.UserMedium


class UserSmallResponse(BaseView):
    content: schemas.UserSmall


class UserDocumentResponse(BaseView):
    content: schemas.UserDocument


class UserListResponse(BaseView):
    content: list[schemas.UserSmall]
