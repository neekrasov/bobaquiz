from app.shared import CommandHandler, Mediator
from .command import CreateUserCommand
from ...protocols.dao import UserDAO
from ...entities.user import (
    UserEntity,
    SubscriptionLevelEntity,
    SubscriptionLevelEnum,
)


class CreateBaseUserCommandHandler(CommandHandler):
    def __init__(self, mediator: Mediator, user_dao: UserDAO):
        self.user_dao = user_dao

    async def execute(
        self,
        command: CreateUserCommand,
    ):
        user = command.user
        await self.user_dao.add_user(
            UserEntity(
                id=UserEntity.generate_id(),
                **user.dict(),
                subscription=SubscriptionLevelEntity(
                    id=SubscriptionLevelEntity.generate_id(),
                    type=SubscriptionLevelEnum.FREE,
                )
            )
        )
        await self.user_dao.commit()
