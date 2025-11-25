from django.db import models
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

class AnalysisRequest(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='analysis_requests',
        verbose_name="사용자"
    )
    analysis_target = models.CharField(verbose_name="분석대상", max_length=20)
    period_type = models.CharField(verbose_name="기간유형", max_length=10)
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일")
    result_image_url = models.CharField(verbose_name="차트이미지 URL", max_length=255, blank=True, null=True)
    result_summary = models.TextField(verbose_name="결과요약", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        db_table = 'analysis_requests'
        verbose_name = '분석 요청'
        ordering = ['-created_at']


class AnalysisSchedule(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="사용자"
    )
    schedule_type = models.CharField(verbose_name="주기 유형", max_length=10)
    run_day = models.CharField(verbose_name="실행 요일/날짜", max_length=10)
    is_active = models.BooleanField(verbose_name="활성화 여부", default=True)

    class Meta:
        db_table = 'analysis_schedule'
        verbose_name = '분석 일정'