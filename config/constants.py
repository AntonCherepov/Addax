AVATAR = 'AV'
MASTER_GALLERY = 'MG'
MASTER_WORKPLACE = 'MW'
ORDER = 'OR'

ALBUM_TYPE_CHOICES = [
    (AVATAR, 'Avatar'),
    (MASTER_GALLERY, 'MasterGallery'),
    (MASTER_WORKPLACE, 'MasterWorkPlace'),
    (ORDER, 'Order'),
]
MAX_ALBUM_COUNTS = {
    AVATAR: 1,
    ORDER: 5,
    MASTER_WORKPLACE: 2000,
    MASTER_GALLERY: 2000,
}

MASTER_ALBUMS = [AVATAR, MASTER_GALLERY, MASTER_WORKPLACE]

DEFAULT_FIELDS = {
    "MasterAccount": {
        "id", "types", "status",
        "gallery_album_id", "workplace_album_id", "about_myself",
        "name", "address",
    },
    "Order": {
        "id", "city", "master_type",
        "status", "date_created", "request_date_from",
        "request_date_to", "description", "selection_date",
        "album_id",
    },
    "Reply": {
        "id", "suggested_time_from", "suggested_time_to",
        "cost", "comment", "order_id",
        "master_id", "date_created", "status",
    }
}
DEFAULT_EXCLUDE_FIELDS = {
    "MasterAccount": {
    },
    "Order": {
        "replies"
    },
    "Reply": {
        "master"
    }
}