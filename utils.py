import random
from hashlib import sha256
from django.core.cache import cache


def hash_otp(otp):
    return sha256(otp.encode()).hexdigest()


def generate_otp(phone_number, expires_at=120):
    otp_code = random.randint(100000, 999999)
    hashed_otp = hash_otp(str(otp_code))
    cache.set(f"otp_{phone_number}", hashed_otp, expires_at)
    cache.set(f"otp_attempt_{phone_number}", 0, expires_at)
    return otp_code


def verify_otp(user_phone, user_otp):
    ...