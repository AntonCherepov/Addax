# UserType
CLIENT = 'c'
MASTER = 'm'
USER_TYPE_CHOICES = [
    (CLIENT, 'Client'),
    (MASTER, 'Master'),
]

# UserStatus
USER_REGISTERED = 'rg'
USER_CONFIRMED = 'cf'
USER_BANNED = 'bn'
USER_STATUS_CHOICES = [
    (USER_REGISTERED, 'registered'),
    (USER_CONFIRMED, 'confirmed'),
    (USER_BANNED, 'banned'),
]

# MasterStatus
MASTER_VERIFIED = 'vr'
MASTER_UNVERIFIED = 'uv'
MASTER_BANNED = 'bn'
MASTER_STATUS_CHOICES = [
    (MASTER_VERIFIED, 'verified'),
    (MASTER_UNVERIFIED, 'unverified'),
    (MASTER_BANNED, 'banned'),
]
