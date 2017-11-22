from configuration import THROTTLE_CALLS_PER_SECOND
from rateLimitDecorator import RateLimited

import cognitive_face as CF

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def add_face(*args, **optionalArgs):
    return CF.person.add_face(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def create(*args, **optionalArgs):
    return CF.person.create(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def delete(*args, **optionalArgs):
    return CF.person.delete(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def delete_face(*args, **optionalArgs):
    return CF.person.delete_face(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def get(*args, **optionalArgs):
    return CF.person.get(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def get_face(*args, **optionalArgs):
    return CF.person.get_face(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def lists(*args, **optionalArgs):
    return CF.person.lists(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def update(*args, **optionalArgs):
    return CF.person.update(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def update_face(*args, **optionalArgs):
    return CF.person.update_face(*args, **optionalArgs)
