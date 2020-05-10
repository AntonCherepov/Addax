from rest_framework.exceptions import ValidationError


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


def get_possible_choice_values(possible_choices):
    return [ch[0] for ch in possible_choices]


def get_status_name(status_choices, status_code):
    status_codes = get_possible_choice_values(status_choices)
    status_code_index = status_codes.index(status_code)
    status_name = status_choices[status_code_index][1]
    return status_name
