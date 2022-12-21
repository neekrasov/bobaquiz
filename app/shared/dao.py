from typing import Protocol


class DAO(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

    async def flush(self) -> None:
        ...


class DAOReader(Protocol):
    ...
