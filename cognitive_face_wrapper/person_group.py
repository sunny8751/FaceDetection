from configuration import THROTTLE_CALLS_PER_SECOND
from rateLimitDecorator import RateLimited

import cognitive_face as CF

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def create(*args, **optionalArgs):
    return CF.person_group.create(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def delete(*args, **optionalArgs):
    return CF.person_group.delete(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def get(*args, **optionalArgs):
    return CF.person_group.get(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def get_status(*args, **optionalArgs):
    return CF.person_group.get_status(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def lists(*args, **optionalArgs):
    return CF.person_group.lists(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def train(*args, **optionalArgs):
    return CF.person_group.train(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def update(*args, **optionalArgs):
    return CF.person_group.update(*args, **optionalArgs)
