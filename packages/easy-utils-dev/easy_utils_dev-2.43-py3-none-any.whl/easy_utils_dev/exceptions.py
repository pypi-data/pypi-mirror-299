
class NetworkElementNotReachable(Exception) :
    def __init__(self ,message='Network Element Is Not Reachable.'):
        super().__init__(message)
