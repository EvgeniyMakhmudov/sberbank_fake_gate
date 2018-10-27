from uuid import uuid4

from .order_status import getOrderStatusExtended
from .datas import Statuses


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

        self.status = Statuses.created  # Generally mapping to payment status
        self.orderStatus = 0

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
        self.orderStatus = 2

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
        self.orderStatus = 3  # TODO: check is it really

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
        self.orderStatus = 4

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }

    def ask3ds(self):
        self.orderStatus = 5

    def decline(self):
        self.status = Statuses.declined
        self.orderStatus = 6

    def getOrderStatusExtended(self):
        return getOrderStatusExtended(self)
