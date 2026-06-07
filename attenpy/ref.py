from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True, kw_only=True)
class UserRef:
    user_id: int | None = None
    username: str | None = None
    me: Literal[True] | None = None

    def __str__(self) -> str:
        match self.value:
            case "username", username:
                return username
            case "user_id", user_id:
                return f":{user_id}"
            case "me", _:
                return ":me"
        raise ValueError()

    def __post_init__(self):
        if sum(i is not None for i in (self.username, self.user_id, self.me)) != 1:
            raise ValueError

    @property
    def value(
        self,
    ) -> Union[
        tuple[Literal["username"], str],
        tuple[Literal["user_id"], int],
        tuple[Literal["me"], Literal[True]],
    ]:
        if self.username is not None:
            return "username", self.username
        elif self.user_id is not None:
            return "user_id", self.user_id
        elif self.me is not None:
            return "me", self.me
        raise ValueError

    @classmethod
    def from_str(cls, path: str):
        if path.startswith(":"):
            user_id = path[1:]
            if user_id == "me":
                return cls(me=True)
            if user_id.isdecimal():
                return cls(user_id=int(user_id))
        return cls(username=path)
