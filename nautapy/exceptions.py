class NautaException(Exception):
    pass


class NautaFormatException(NautaException):
    pass


class NautaPreLoginException(NautaException):
    pass


class NautaLoginException(NautaException):
    pass


class NautaLogoutException(NautaException):
    pass

