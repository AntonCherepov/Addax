from django.db.models import QuerySet
from rest_framework.serializers import ModelSerializer

from config.constants import DEFAULT_FIELDS, DEFAULT_EXCLUDE_FIELDS
from core.utils import string_to_set


class DynamicFieldsModelSerializer(ModelSerializer):
    """Controls returned fields by ModelSerializer

    A ModelSerializer that takes an additional `fields` and
    `exclude_fields` argument that controls which fields should
    be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        if isinstance(fields, str):
            fields = string_to_set(fields)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if exclude_fields is not None:
            for field_name in set(exclude_fields):
                self.fields.pop(field_name)
        try:
            class_name = self.get_objects_class_name(*args)
            if fields is not None:
                # Add to return default fields
                if 'default' in fields:
                    fields = fields.union(DEFAULT_FIELDS[class_name])
                    for field_name in DEFAULT_EXCLUDE_FIELDS[class_name]:
                        if field_name not in fields:
                            fields.discard(field_name)
                existing = set(self.fields)
                allowed = set(fields)

                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            else:
                for field_name in DEFAULT_EXCLUDE_FIELDS[class_name]:
                    self.fields.pop(field_name)
        except (IndexError, KeyError):
            pass

    @staticmethod
    def get_objects_class_name(*args):
        # If query of objects
        if isinstance(args[0], QuerySet):
            objects_name = type(args[0][0]).__name__
        # If one object
        else:
            objects_name = type(args[0]).__name__
        return objects_name
