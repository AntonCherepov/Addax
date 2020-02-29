from django.db.models import Model, CharField, ForeignKey, SET_NULL


class City(Model):

    name = CharField(max_length=200)


class MasterType(Model):

    name = CharField(max_length=45)


class MasterStatus(Model):

    code = CharField(max_length=2, unique=True, primary_key=True)
    name = CharField(max_length=15)

    def __str__(self):
        return self.code


class UserType(Model):
    code = CharField(max_length=1, unique=True, primary_key=True)
    name = CharField(max_length=15)

    def __str__(self):
        return self.code


class UserStatus(Model):
    code = CharField(max_length=2, unique=True, primary_key=True)
    name = CharField(max_length=15)

    def __str__(self):
        return self.code


class OrderStatus(Model):
    code = CharField(max_length=2, unique=True, primary_key=True)
    name = CharField(max_length=15)

    def __str__(self):
        return self.code


class ReplyStatus(Model):
    code = CharField(max_length=2, unique=True, primary_key=True)
    name = CharField(max_length=10)

    def __str__(self):
        return self.code


class TableType(Model):
    code = CharField(max_length=1, unique=True, primary_key=True)
    name = CharField(max_length=10)

    def __str__(self):
        return self.code


class Table(Model):
    code = CharField(max_length=5, unique=True, primary_key=True)
    name = CharField(max_length=20)
    table_type = ForeignKey(TableType, on_delete=SET_NULL, null=True)
