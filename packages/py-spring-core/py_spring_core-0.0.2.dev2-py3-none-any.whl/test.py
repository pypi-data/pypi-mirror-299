from loguru import logger
from py_spring_core.core.entities.component import Component


class TestService(Component):
    def test(self, x: int, y: int) -> None: ...
