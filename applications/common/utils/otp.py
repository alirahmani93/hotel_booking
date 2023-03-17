import random
from abc import ABC, abstractmethod

from django.core.cache import cache


class OtpMeta(ABC):

    @staticmethod
    def create_opt_code():
        return random.randint(a=100, b=1000)

    @abstractmethod
    def send_sms(self, mobile_number: str) -> bool:
        print(self.create_opt_code())
        return True

    @staticmethod
    def set_cache(otp, mobile_number):
        return cache.set(otp, mobile_number, timeout=60 * 4)


class HamrahAval(OtpMeta):
    def __init__(self):
        pass

    def send_sms(self, mobile_number: str) -> bool:
        otp = self.create_opt_code()
        self.set_cache(otp, mobile_number)
        print(f"mobile_number: {mobile_number} otp_code:{otp}")
        return True


hamrah_aval = HamrahAval()


class Otp:
    default_modul = hamrah_aval.send_sms
    modules = {
        "0919": hamrah_aval.send_sms,
        "0912": hamrah_aval.send_sms,
    }

    def __select_operator(self, mobile_number: str):
        operator = self.modules.get(mobile_number[:4])
        return operator

    def send_sms(self, mobile_number):
        return self.__select_operator(mobile_number)(mobile_number)

    def get_cache(self, otp):
        return cache.get(otp)


OTP = Otp()
