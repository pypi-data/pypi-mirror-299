from .abstract_backend import ErrorReporter
from .singleton_meta import ReporterSingletonMeta

class Reporter(metaclass= ReporterSingletonMeta):
    def __init__(self, *reporters, **kwargs):
        self.reporters : list[ErrorReporter] = reporters
        self.config = kwargs
    
    def register(self, reporter: ErrorReporter):
        self.reporters.append(reporter)
        
    def report(self, exception: Exception, **kwargs):
        reporter_name = kwargs.pop('name', None)
        
        if reporter_name in [reporter.name for reporter in self.reporters]:
            for reporter in self.reporters:
                if reporter.name == reporter_name:
                    reporter.report(exception, **kwargs)
                    return
               
        for reporter in self.reporters:
            reporter.report(exception, **kwargs)
