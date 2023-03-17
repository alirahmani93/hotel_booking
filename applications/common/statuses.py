from rest_framework.views import status

OK_200 = {
    'detail': 'OK',
    'code': 'OK',
    'number': status.HTTP_200_OK
}
CREATED_201 = {
    'detail': 'Created',
    'code': 'created',
    'number': status.HTTP_201_CREATED
}
DELETED_204 = {
    'detail': 'Deleted',
    'code': 'deleted',
    'number': status.HTTP_204_NO_CONTENT
}
RESERVE_SUCCESSFUL_211 = {
    'detail': 'Successful reserve',
    'code': 'reserve_successful',
    'number': 211
}
# 400
BAD_REQUEST_400 = {
    'detail': 'Bad request',
    'code': 'bad_request',
    'number': 400
}
USER_NOT_FOUND_450 = {
    'detail': 'User not found',
    'code': 'user_not_found',
    'number': 450
}
OWNER_NOT_FOUND_451 = {
    'detail': 'Owner not found',
    'code': 'owner_not_found',
    'number': 451
}
ROOM_NOT_FOUND_452 = {
    'detail': 'Room not found',
    'code': 'room_not_found',
    'number': 451
}

USER_BLOCKED_453 = {
    'detail': 'User is block',
    'code': 'user_is_block',
    'number': 453
}
ROOM_ALREADY_RESERVED_454 = {
    'detail': 'Room already reserved',
    'code': 'room_already_reserved',
    'number': 454
}
OWNER_BLOCKED_455 = {
    'detail': 'Owner is block',
    'code': 'owner_is_block',
    'number': 455
}

ROOM_ALREADY_EXISTS_456 = {
    'detail': 'Room already exists',
    'code': 'room_already_exists',
    'number': 456
}
PLACE_NOT_FOUND_457 = {
    'detail': 'Place not found',
    'code': 'place_not_found',
    'number': 451
}
USER_NOT_OWNER_458 = {
    'detail': 'User Not Owner',
    'code': 'user_not_owner',
    'number': 458
}

PLACE_ALREADY_EXISTS_459 = {
    'detail': 'Place already exists',
    'code': 'place_already_exists',
    'number': 459
}
RESERVE_NOT_ENOUGH_BED_460 = {
    'detail': 'room has not enough bed for reserve',
    'code': 'not_enough_bed',
    'number': 460
}

USER_ALREADY_EXISTS_461 = {
    'detail': 'User already exists',
    'code': 'user_already_exists',
    'number': 461
}
OTP_EXPIRED = {
    'detail': 'Otp expired',
    'code': 'otp expired',
    'number': 462
}
OWNERSHIP_ERROR_463 = {
    'detail': 'It does not belong to you',
    'code': 'ownership_error',
    'number': 463
}

# 500
SERVER_ERROR_500 = {
    'detail': 'Server error',
    'code': 'server_error',
    'number': status.HTTP_500_INTERNAL_SERVER_ERROR
}
