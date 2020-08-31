# OrderStatus
SELECTION_OF_MASTERS = 'sm'
MASTER_SELECTED = 'ms'
CANCELED_BY_CLIENT = 'cc'
CANCELED_BY_MASTER = 'cm'
CLIENT_DID_NOT_ARRIVE = 'na'
SUCCESSFULLY_COMPLETED = 'cs'
ORDER_STATUS_CHOICES = [
    (SELECTION_OF_MASTERS, 'Подбор мастеров'),
    (MASTER_SELECTED, 'Выбран мастер'),
    (CANCELED_BY_CLIENT, 'Отменена клиентом'),
    (CANCELED_BY_MASTER, 'Отменена мастером'),
    (CLIENT_DID_NOT_ARRIVE, 'Клиент не приехал'),
    (SUCCESSFULLY_COMPLETED, 'Завершена успешно'),
]

# ReplyStatus
SELECTED = 'sl'
CONSIDERED = 'cs'
REJECTED = 'rj'
RECALLED = 'rc'
REPLY_STATUS_CHOICES = [
    (SELECTED, 'selected'),
    (CONSIDERED, 'considered'),
    (REJECTED, 'rejected'),
    (RECALLED, 'recalled'),
]
