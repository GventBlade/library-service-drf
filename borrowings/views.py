from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListSerializer

from datetime import date
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if not self.request.user.is_staff:
            queryset.filter(user=self.request.user)

        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user_id=int(user_id))

        if is_active:
            is_active_bool = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active_bool)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response({'borrowing':"This book has already been returned"},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            book = borrowing.book
            book.inventory += 1
            book.save()

            borrowing.actual_return_date = date.today()
            borrowing.save()

            serializer = self.get_serializer(borrowing)
            return Response(serializer.data, status=status.HTTP_200_OK)
