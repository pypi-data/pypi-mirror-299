from abc import ABC, abstractmethod


class IPage(ABC):
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def _setTemplate(self):
        pass

    @abstractmethod
    def _setStyle(self)->str:
        pass