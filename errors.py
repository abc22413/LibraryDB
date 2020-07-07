# Custom Exceptions
class Error(Exception):
    """Base class for other exceptions
    """
    pass

class OptionOutOfRange(Error):
    """Raised when option selected from menu is out of range
    """
    pass

class DBConnectionError(Error):
    """Raised when option selected from menu is out of range
    """
    pass

class ObjNotHaveAttr(Error):
    '''Raised when mongoDB object does not have requested field for editing
    '''
    pass

class BookNotHaveAttr(ObjNotHaveAttr):
    '''Raised when mongoDB Book does not have requested field for editing
    '''
    pass

class UserNotHaveAttr(ObjNotHaveAttr):
    '''Raised when mongoDB User does not have requested field for editing
    '''
    pass