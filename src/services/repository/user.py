from sqlalchemy import func, select, text
from sqlalchemy.orm import joinedload

from src.models import tables
from src.services.repository.base import BaseRepository


class UserRepo(BaseRepository[tables.User]):
    table = tables.User

    async def get(self, as_full: bool = False, **kwargs) -> tables.User | None:
        req = select(self.table).filter_by(**kwargs)
        if as_full:
            req = req.options(joinedload(self.table.role).subqueryload(tables.Role.permissions))
        return (await self._session.execute(req)).scalars().first()

    async def get_by_email_insensitive(self, email: str, as_full: bool = False) -> tables.User | None:
        req = select(self.table).where(func.lower(self.table.email) == email.lower())
        if as_full:
            req = req.options(joinedload(self.table.role).subqueryload(tables.Role.permissions))
        return (await self._session.execute(req)).scalar_one_or_none()

    async def get_all(
            self, limit: int = 100,
            offset: int = 0,
            as_full: bool = False,
            **kwargs
    ) -> list[tables.User]:
        req = select(self.table).filter_by(**kwargs)
        if as_full:
            req = req.options(joinedload(self.table.role).subqueryload(tables.Role.permissions))

        result = (await self._session.execute(req.limit(limit).offset(offset))).unique()
        return result.scalars().all()
