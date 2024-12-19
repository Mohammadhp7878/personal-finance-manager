import random
import logging
from rest_framework.exceptions import ValidationError  
from hashlib import sha256
from django.core.cache import cache


logger = logging.getLogger(__name__)

def hash_otp(otp):
    return sha256(otp.encode()).hexdigest()


def generate_otp(phone_number, expires_at=120):
    otp_code = random.randint(100000, 999999)
    hashed_otp = hash_otp(str(otp_code))
    cache.set(f"otp_{phone_number}", hashed_otp, expires_at)
    cache.set(f"otp_attempt_{phone_number}", 0, expires_at)
    return otp_code


def verify_otp(user_phone, user_otp):
    if not user_otp.isdigit():
        logger.warning(f"invalid otp sent")
        raise ValidationError("invalid otp")
    
    cached_otp = cache.get(f"otp_{user_phone}")
    attempts = cache.get(f"otp_attempt_{user_phone}")

    
    if not cached_otp:
        logger.warning(f"the otp fot user with {user_phone} phone number expired")
        raise ValidationError("you need to resend the otp code")
    
    ttl = cache.ttl(f"otp_{user_phone}")
    
    max_try_allowed = 3 
    
    if attempts > max_try_allowed:
        logger.warning(f"user with {user_phone} phonumber exeeded the maximum attemps allowed")
        raise ValidationError("maximum OTP attempts reached")

    if cached_otp and str(cached_otp) == hash_otp(user_otp):
        logger.info(f"user with {user_phone} phone number is logged in")
        cache.delete(f'otp_{user_phone}')
        return True
    
    attempts += 1
    cache.set(f"otp_attempt_{user_phone}", attempts, ttl)
    logger.warning(f"user with {user_phone} phone number failed to login fot {attempts} time")
    raise ValidationError(f"invalid OTP. attempts allowed: {max_try_allowed - attempts}, ttl:{ttl}") 
    