from enum import Enum


class Statuses(Enum):
    created = 'CREATED'
    deposited = 'DEPOSITED'
    refunded = 'REFUNDED'
    declined = 'DECLINED'
    reversed = 'REVERSED'  # TODO: check it by real case
