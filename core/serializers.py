from rest_framework.serializers import ModelSerializer


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude_fields = set(kwargs.pop('exclude_fields', None))
        if isinstance(fields, str):
            fields = self.raw_fields_to_set(fields)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            existing = set(self.fields)
            allowed = set(fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    @staticmethod
    def raw_fields_to_set(fields):
        return set(str(fields).split(","))
