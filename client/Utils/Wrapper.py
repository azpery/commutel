class Wrapper:

    @staticmethod
    def wrapStatus( message):
        return "/s " + str(message)

    @staticmethod
    def wrapMessage(message):
        return "/m " + message

    @staticmethod
    def wrapInfo(message):
        return "/i " + message

    @staticmethod
    def wrapError(message):
        return "/e " + message

    @staticmethod
    def wrapCommand(message):
        return "/c " + message