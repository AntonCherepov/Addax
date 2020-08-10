from django.db.models import Model, ForeignKey, CASCADE, IntegerField, \
    CharField, DateTimeField, OneToOneField
from balance.constants import (OPERATION_ORDER_COMPLETE,
                               OPERATION_BALANCE_REPLENISHMENT)
from users.models import User


class Balance(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    current_value = IntegerField(default=0)

    def is_positive(self):
        return True if self.current_value >= 0 else False

    def change_value(self, operation_value_difference, operation_name):
        self.current_value += int(operation_value_difference)
        BalanceHistory.objects.create(
            balance=self,
            change_value=operation_value_difference,
            operation_name=operation_name,
            current_balance_value=self.current_value
        )
        self.save()


class BalanceHistory(Model):
    balance = ForeignKey(Balance, on_delete=CASCADE)
    change_value = IntegerField()
    current_balance_value = IntegerField()
    operation_date = DateTimeField(auto_now_add=True)
    operation_name = CharField(max_length=50, choices=(
        (OPERATION_ORDER_COMPLETE, OPERATION_ORDER_COMPLETE),
        (OPERATION_BALANCE_REPLENISHMENT, OPERATION_BALANCE_REPLENISHMENT),
    ))
