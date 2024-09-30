# PyExcReporter

In order to to use pyreporter, you will have to subclass `ErrorReporter` and create your own reporting backend class:

```py
from pyexcreporter import ErrorReporter

class MyErrorReporter(ErrorReporter):
    def __init__(self) -> None:
        super().__init__()
        self.name = "MyErrorReporter"
    
    def report(self, exception: Exception, **kwargs):
        """Report an exception with optional additional data."""
        pass
```

Once created, register the reporter in the reporter engine.

```py

