import inspect
import traceback
from antbase import Auth

class Log:
    __client      = Auth.get_logging_client()
    __logger      = __client.logger(Auth.get_anthill_name())

    @staticmethod
    def __log(severity, *args, **kwargs):

        message = ' '.join(map(str, args)) if len(args) > 0 else ''
        frame = inspect.currentframe()
        stack = traceback.extract_stack(frame)
        structured_stack = [
            {
                'file': frame.filename,
                'line': frame.lineno,
                'function': frame.name,
                'code': frame.line
            } for frame in stack
        ]
        
        Log.__logger.log_struct(
            {                
                'severity'      : severity,
                'message'       : message,
                'sourceLocation': {
                    'file'      : frame.f_back.f_back.f_code.co_filename,
                    'function'  : frame.f_back.f_back.f_code.co_name,
                    'line'      : frame.f_back.f_back.f_lineno },
                'stack'         : structured_stack,
                'labels'        : {**kwargs}
            }
        ) 

    @staticmethod
    def log(*args, **kwargs): Log.__log("DEFAULT", *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs): Log.__log("INFO", *args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs): Log.__log("DEBUG", *args, **kwargs)

    @staticmethod
    def warning(warning_name, *args, **kwargs): Log.__log("WARNING", *args, **kwargs, warning=warning_name)

    @staticmethod
    def error(error_name, *args, **kwargs): Log.__log("ERROR", *args, **kwargs, error=error_name)

    @staticmethod
    def pc(precondition, *args, **kwargs):
        if not precondition:
            Log.__log("CRITICAL", *args, **kwargs, error="PreconditionError")
            raise Exception("PreconditionError")