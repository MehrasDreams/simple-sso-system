import random
from .redis_manager import REDIS_MANAGER


class OtpManager:

    def remove_code(self, phone):
        try:

            remove_code = REDIS_MANAGER.remove_by_key(phone)
            return True
        except:
            return False

    def send_otp_code(self):
        # Send via  api later

        pass

    def create_otp_code(self, phone):

        # Change body id later | when fucking melipayamak give the accesses

        random_otp = random.randint(10000, 99999)

        response = {}

        get_or_create_code = REDIS_MANAGER.get_key(key=phone)

        if get_or_create_code != None:
            response.update({'data': 'code exits'})
        elif get_or_create_code == None:
            REDIS_MANAGER.set_key(key=phone, value=random_otp)

            # TODO: working on performance remove it later from the main database
            response.update({'data': 'code has been sent', 'code': random_otp})
        return response

    def otp_checker(self, phone, code):
        response = False

        get_or_create_code = REDIS_MANAGER.get_key(key=phone)

        if get_or_create_code != None:

            decoded_response = get_or_create_code.decode('utf-8')
            response = False

            if decoded_response == code:
                response = True

        return response


OTP_MANAGER = OtpManager()

# TODO: add the time limit for the codes
