from .base import BaseView
from src.models import schemas


class UserResponse(BaseView):
    content: schemas.UserMedium


class UserFullResponse(BaseView):
    content: schemas.User


class UsersFullResponse(BaseView):
    content: list[schemas.User]


class UserDocumentResponse(BaseView):
    content: schemas.UserDocument
