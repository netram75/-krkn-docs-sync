import abc
import logging
from dataclasses import dataclass


@dataclass
class ScenarioResult:
    success: bool
    message: str = ""


class BaseScenario(abc.ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def setup(self, config: dict) -> None:
        pass

    @abc.abstractmethod
    def run(self) -> ScenarioResult:
        pass

    @abc.abstractmethod
    def teardown(self) -> None:
        pass

    def execute(self, config: dict) -> ScenarioResult:
        self.setup(config)
        try:
            return self.run()
        finally:
            self.teardown()
