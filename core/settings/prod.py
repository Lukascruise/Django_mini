from .base import *

# --- Core Security Settings ---
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY") # 배포 시 이 키는 secrets.json 또는 환경 변수에 있어야 합니다.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# 배포 환경에서는 ' * '를 허용하지 않습니다. 실제 도메인만 허용합니다.
# secrets.json 또는 환경 변수에 'prod.example.com,api.example.com' 형태로 설정해야 합니다.
ALLOWED_HOSTS_STRING = get_secret("ALLOWED_HOSTS")

if ALLOWED_HOSTS_STRING:
    if isinstance(ALLOWED_HOSTS_STRING, str):
        # 환경 변수나 secrets.json의 콤마 구분 문자열인 경우 처리
        ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_STRING.split(',')]
    elif isinstance(ALLOWED_HOSTS_STRING, list):
        # secrets.json에 JSON 리스트 형태로 저장된 경우 처리
        ALLOWED_HOSTS = ALLOWED_HOSTS_STRING
    else:
        # 그 외 부적절한 타입인 경우
        raise ImproperlyConfigured("ALLOWED_HOSTS는 콤마로 구분된 문자열 또는 리스트여야 합니다.")
else:
    # Allowed hosts가 설정되지 않았다면 예외를 발생시켜 보안을 강화합니다.
    raise ImproperlyConfigured("ALLOWED_HOSTS must be set in production environment.")


# --- Database for Production ---
# DB_HOST, DB_PASSWORD 등은 반드시 환경 변수/secrets.json을 통해 설정되어야 합니다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("DB_USER"),
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": get_secret("DB_HOST"),
        "PORT": get_secret("DB_PORT", "5432"),
    }
}


# --- Production Static and Media Files ---
# 배포 환경에서는 정적 파일을 Nginx/S3 등을 통해 제공합니다.
# (STATICFILES_STORAGE 설정: 필요시 S3 백엔드 등을 사용하도록 추가 설정 가능)


# --- Additional Security Settings (Production Only) ---
SECURE_SSL_REDIRECT = get_secret("SECURE_SSL_REDIRECT", False)
SECURE_HSTS_SECONDS = get_secret("SECURE_HSTS_SECONDS", 0)

if SECURE_HSTS_SECONDS > 0:
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True