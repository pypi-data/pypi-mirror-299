class SElementMergedException(Exception):
    def __init__(self, msg):
        super(Exception, self).__init__(msg)


class ModelNotFoundException(Exception):
    def __init__(self, msg):
        super(Exception, self).__init__(msg)
