from configuration import THROTTLE_CALLS_PER_SECOND
from rateLimitDecorator import RateLimited

import cognitive_face as CF

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def detect(*args, **optionalArgs):
    return CF.face.detect(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def find_similars(*args, **optionalArgs):
    return CF.face.find_similars(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def group(*args, **optionalArgs):
    return CF.face.group(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def identify(*args, **optionalArgs):
    return CF.face.identify(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def verify(*args, **optionalArgs):
    return CF.face.verify(*args, **optionalArgs)
