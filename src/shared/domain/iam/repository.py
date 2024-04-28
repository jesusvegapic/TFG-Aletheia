class UserRepository(GenericRepository[GenericUUID, User]):
    @abstractmethod
    def get_by_email(self, email: Email) -> User | None:
        ...

    @abstractmethod
    def get_by_access_token(self, access_token: str) -> User | None:
        ...