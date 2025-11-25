from django.db import models
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

class Account(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,   # 계좌가 삭제되면 거래 내역도 삭제
        related_name='accounts',
        verbose_name="사용자"
    )
    account_number = models.CharField(verbose_name="계좌번호", max_length=30, unique=True)
    bank_code = models.CharField(verbose_name="은행코드", max_length=10)
    account_type = models.CharField(verbose_name="계좌종류", max_length=10)
    name = models.CharField(verbose_name="계좌별칭", max_length=60)
    # balance = models.BigIntegerField(verbose_name="잔액(원 단위)")
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        db_table = 'accounts'
        verbose_name = '계좌'