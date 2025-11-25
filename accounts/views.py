from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    사용자의 Account 모델에 대한 CRUD API 엔드포인트.
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만 접근 가능

    def get_queryset(self):
        """현재 로그인된 사용자의 Account만 필터링하여 반환합니다."""
        # QuerySet을 현재 요청 사용자(self.request.user)의 계좌로 제한합니다.
        return Account.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """계좌 생성 시 user 필드를 자동으로 현재 사용자로 설정합니다."""
        # user=self.request.user를 serializer에 전달하여 저장합니다.
        serializer.save(user=self.request.user)