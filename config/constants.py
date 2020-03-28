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

DEFAULT_MASTER_FIELDS = [
            "id", "types",
            "avatar_album_id", "gallery_album_id",
            "workplace_album_id", "about_myself",
            "name", "address",
            "status_code"
        ]
