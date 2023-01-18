from user import User


class Channel:
    def __init__(self, name) -> None:
        self.users: dict[str, User] = {}
        self.name = name

    def addUser(self, user: User):
        self.users[user.nick] = user

    def removeUser(self, nick):
        self.users.pop(nick)