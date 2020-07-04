# Custom Exceptions
class Error(Exception):
    """Base class for other exceptions
    """
    pass

class OptionOutOfRange(Error):
    """Raised when option selected from menu is out of range
    """
    pass