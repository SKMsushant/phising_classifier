import sys

def error_message_detail(error, error_detail:sys):
    #exc_tb-is a special object that contains the traceback information
    # _,_-will be assigned to the first two values of the tuple returned by "error_detail.exc_info()" i.e type and value and exception traceback will be assigned to exc_tb
    _,_,exc_tb=error_detail.exc_info()


    #exc.tb-traceback object that contains the traceback information
    #tb_frame-refers to the frame object of the traceback which reprsents the current stack frame
    #f_code- code object being executed in the current frame
    #co_filename- name of the file in which the code object was defined
    #file_name-name of the file will be assigned to the file_name returned from co_filename
    file_name=exc_tb.tb_frame.f_code.co_filename

    #{0},{1},{2} will be replaced by file_name, line number and error message respectively as provided in the format method
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message

class CustomException(Exception):
    #__init__ -constructor method that is called when an instance/object of the CustomException is created
    def __init__(self, error_message, error_detail:sys):
        """
        :param error_message: str: Error message in string format
        """
        super().__init__(error_message)
        self.error_message=error_message_detail(
            error_message, error_detail=error_detail)   

    #__str__-method that returns a string representation of the object when it is printed or converted to a string
    def __str__(self):
        return self.error_message