from albums.models import Photo


def create_photos(files, user, album):
    photos = []
    for key in tuple(files):
        Photo.validate(files[key])
        photo = Photo(user=user, image=files[key], album=album)
        photos.append(photo)
    photos = Photo.objects.bulk_create(photos)
    return photos
