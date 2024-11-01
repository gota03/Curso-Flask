import uuid
import qrcode

class Pix:

    def __init__(self):
        pass

    def create_payment(self):
        bank_payment_id = uuid.uuid4()

        hash_payment = f'hash_payment_{bank_payment_id}'

        qr_code = qrcode.make(hash_payment)
        qr_code.save(f'static\qrcode\qr_code_payment_{bank_payment_id}.png')

        return {
            'bank_payment_id': bank_payment_id,
            'qr_code_path': f'qr_code_payment_{bank_payment_id}'
        }