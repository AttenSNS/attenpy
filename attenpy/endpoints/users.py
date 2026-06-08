from typing import TYPE_CHECKING

from ..ref import UserRef

if TYPE_CHECKING:
    from ..client import Client


class UserEndpoint:
    def __init__(self, client: Client):
        self.client = client

    def get(self, user: UserRef | str):
        pass
