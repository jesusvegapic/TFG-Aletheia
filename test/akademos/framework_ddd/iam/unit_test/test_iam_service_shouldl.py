from unittest.mock import AsyncMock
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.domain.entities import User
from test.akademos.framework_ddd.iam.unit_test.iam_module import TestIamModule


class IamServiceShould(TestIamModule):

    async def test_validate_user_by_basic_auth_if_user_exists(self):
        self.repository.get_by_email = AsyncMock()
        user = User(
            id=User.next_id().hex,
            email="pepito@gmail.com",
            hashed_password=IamService.hash_password("1lkjas232134"),
            is_superuser=True
        )
        self.repository.get_by_email.return_value = user

        token = await self.iam_service.authenticate_with_email_and_password(
            "pepito@gmail.com",
            "1lkjas232134"
        )

        user_info = self.iam_service.auth_by_token(token)

        self.assertEqual(user_info.user_id, user.id)
        self.assertEqual(user_info.email, user.email)
        self.assertEqual(user_info.is_superuser, user.is_superuser)
