from uuid import uuid4
from enum import Enum

from .order_status import getOrderStatusExtended


class Statuses(Enum):
    created = 'CREATED'
    deposited = 'DEPOSITED'
    refunded = 'REFUNDED'
    declined = 'DECLINED'
    reversed = 'REVERSED'  # TODO: check it by real case


def parse_jsonParams(d):
    if d is None:
        return None

    result = []
    for k, v in d.items():
        result.append({
            'name': k,
            'value': v,
        })
    return result


class SberbankOrder:
    def registerPreAuth(self, *, orderNumber, amount, returnUrl, failUrl,
                        description, jsonParams, host='http://localhost:8000'):

        self.orderNumber = orderNumber
        self.preauth_amount = amount
        self.returnUrl = returnUrl
        self.failUrl = failUrl
        self.description = description
        self.merchantOrderParams = parse_jsonParams(jsonParams)
        # self.lang  # TODO:

        self.id = str(uuid4())
        template = '{}/payment/payment_ru.html?mdOrder={}'
        self.form_url = template.format(host, self.id)

        self.status = Statuses.created

        # moneys amount
        self.approvedAmount = 0
        self.depositedAmount = 0  # current amount
        self.refundedAmount = 0

        return {
            'orderId': self.id,
            'formUrl': self.form_url,
        }

    def deposit(self, amount):
        if amount > self.preauth_amount:
            raise ValueError()

        self.approvedAmount = amount
        self.depositedAmount = amount

        self.status = Statuses.deposited

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }

    def reverse(self):
        if self.status != Statuses.created:
            return {
                'errorCode': '7',
                'errorMessage': 'Операция невозможна для текущего состояния платежа',
            }

        self.status = Statuses.reversed

        self.approvedAmount = 0

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }

    def refund(self, amount):
        if self.status not in [Statuses.deposited, Statuses.refunded]:
            return {
                'errorCode': '7',
                'errorMessage': 'Платёж должен быть в корректном состоянии',
            }

        if amount > self.depositedAmount:
            return {
                'errorCode': '7',
                'errorMessage': 'Неверная сумма депозита',
            }

        self.depositedAmount -= amount
        self.refundedAmount += amount

        self.status = Statuses.refunded

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }

    def getOrderStatusExtended(self):
        return getOrderStatusExtended(self)
