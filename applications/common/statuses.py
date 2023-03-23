from rest_framework.views import status

# 200
OK_200 = {
    'detail': 'OK',
    'code': 'OK',
    'number': status.HTTP_200_OK
}
RESERVE_SUCCESSFUL_200 = {
    'detail': 'Successful reserve',
    'code': 'reserve_successful',
    'number': status.HTTP_200_OK
}
# 201
CREATED_201 = {
    'detail': 'Created',
    'code': 'created',
    'number': status.HTTP_201_CREATED
}
# 204
DELETED_204 = {
    'detail': 'Deleted',
    'code': 'deleted',
    'number': status.HTTP_204_NO_CONTENT
}
# 400
BAD_REQUEST_400 = {
    'detail': 'Bad request',
    'code': 'bad_request',
    'number': status.HTTP_400_BAD_REQUEST
}
OTP_EXPIRED_400 = {
    'detail': 'Otp expired',
    'code': 'otp expired',
    'number': status.HTTP_400_BAD_REQUEST
}
RESERVE_NOT_ENOUGH_BED_400 = {
    'detail': 'room has not enough bed for reserve',
    'code': 'not_enough_bed',
    'number': status.HTTP_400_BAD_REQUEST
}

# 404
NOT_FOUND_404 = {
    'detail': 'Not found',
    'code': 'not_found',
    'number': status.HTTP_404_NOT_FOUND
}
USER_NOT_FOUND_404 = {
    'detail': 'User not found',
    'code': 'user_not_found',
    'number': status.HTTP_404_NOT_FOUND
}
OWNER_NOT_FOUND_404 = {
    'detail': 'Owner not found',
    'code': 'owner_not_found',
    'number': status.HTTP_404_NOT_FOUND
}
ROOM_NOT_FOUND_404 = {
    'detail': 'Room not found',
    'code': 'room_not_found',
    'number': status.HTTP_404_NOT_FOUND
}
PLACE_NOT_FOUND_404 = {
    'detail': 'Place not found',
    'code': 'place_not_found',
    'number': status.HTTP_404_NOT_FOUND
}
USER_NOT_OWNER_404 = {
    'detail': 'User Not Owner',
    'code': 'user_not_owner',
    'number': status.HTTP_404_NOT_FOUND
}

# 403
FORBIDDEN_403 = {
    'detail': 'Forbidden',
    'code': 'forbidden',
    'number': status.HTTP_403_FORBIDDEN
}
USER_BLOCKED_403 = {
    'detail': 'User is block',
    'code': 'user_is_block',
    'number': status.HTTP_403_FORBIDDEN
}
OWNER_BLOCKED_403 = {
    'detail': 'Owner is block',
    'code': 'owner_is_block',
    'number': status.HTTP_403_FORBIDDEN
}

# 409
CONFLICT_409 = {
    'detail': 'Conflict',
    'code': 'conflict',
    'number': status.HTTP_409_CONFLICT
}
OWNERSHIP_ERROR_409 = {
    'detail': 'It does not belong to you',
    'code': 'ownership_error',
    'number': status.HTTP_409_CONFLICT
}
ROOM_ALREADY_RESERVED_409 = {
    'detail': 'Room already reserved',
    'code': 'room_already_reserved',
    'number': status.HTTP_409_CONFLICT
}
ROOM_ALREADY_EXISTS_409 = {
    'detail': 'Room already exists',
    'code': 'room_already_exists',
    'number': status.HTTP_409_CONFLICT
}
PLACE_ALREADY_EXISTS_409 = {
    'detail': 'Place already exists',
    'code': 'place_already_exists',
    'number': status.HTTP_409_CONFLICT
}
USER_ALREADY_EXISTS_409 = {
    'detail': 'User already exists',
    'code': 'user_already_exists',
    'number': status.HTTP_409_CONFLICT
}

# 500
SERVER_ERROR_500 = {
    'detail': 'Server error',
    'code': 'server_error',
    'number': status.HTTP_500_INTERNAL_SERVER_ERROR
}
