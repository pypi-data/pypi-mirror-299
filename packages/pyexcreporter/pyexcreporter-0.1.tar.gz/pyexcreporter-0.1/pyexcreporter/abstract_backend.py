from abc import ABC, abstractmethod

class ErrorReporter(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.name = self.__class__.__name__
    
    @abstractmethod
    def report(self, exception: Exception, **kwargs):
        """Report an exception with optional additional data."""
        pass
