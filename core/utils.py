def pagination(objects, offset=0, limit=25):
    """
    Custom offset/limit pagination with deleting duplicates
    and order by "id"
    """
    objects = objects.distinct().order_by("id")
    count = objects.count()
    if offset:
        objects = objects[int(offset)::]
    if limit:
        limit = int(limit)
        if limit <= 50:
            objects = objects[:limit:]
    else:
        objects = objects[:25:]
    return objects, count


def string_to_set(fields):
    """Parser for parameter values in request"""
    return set(str(fields).split(","))