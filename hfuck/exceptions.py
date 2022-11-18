class ChallengeError(Exception):
    pass

class RequestRejected(ChallengeError):
    pass

class GetCaptchaRejected(ChallengeError):
    pass