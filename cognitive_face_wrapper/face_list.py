from configuration import THROTTLE_CALLS_PER_SECOND
from rateLimitDecorator import RateLimited

import cognitive_face as CF

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def add_face(*args, **optionalArgs):
    return CF.face_list.add_face(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def create(*args, **optionalArgs):
    return CF.face_list.create(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def delete_face(*args, **optionalArgs):
    return CF.face_list.delete_face(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def delete(*args, **optionalArgs):
    return CF.face_list.delete(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def get(*args, **optionalArgs):
    return CF.face_list.get(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def lists(*args, **optionalArgs):
    return CF.face_list.lists(*args, **optionalArgs)

@RateLimited(THROTTLE_CALLS_PER_SECOND)
def update(*args, **optionalArgs):
    return CF.face_list.update(*args, **optionalArgs)
