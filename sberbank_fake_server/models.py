from uuid import uuid4


class SberbankOrder:
    def registerPreAuth(self, *, orderNumber, amount, returnUrl, failUrl,
                        description, host='http://localhost:8000'):

        self.orderNumber = orderNumber
        self.amount = amount
        self.returnUrl = returnUrl
        self.failUrl = failUrl
        self.description = description

        self.id = str(uuid4())
        template = '{}/payment/payment_ru.html?mdOrder={}'
        self.form_url = template.format(host, self.id)

        self.status = 'preauth'

        return {
            'orderId': self.id,
            'formUrl': self.form_url,
        }

    def deposit(self, amount):
        if amount > self.amount:
            raise ValueError()

        self.amount = amount
        self.status = 'deposit'

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }

    def reverse(self):
        if self.status not in ['preauth', 'deposit']:
            return {
                'errorCode': '7',
                'errorMessage': 'Операция невозможна для текущего состояния платежа',
            }

        self.status = 'reverse'

        return {
            'errorCode': '0',
            'errorMessage': 'Успешно',
        }
