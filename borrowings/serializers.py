from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from borrowings.models import Borrowing
from books.serializers import BookSerializer
from payments.serializers import PaymentSerializer

class BorrowingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory == 0:
            raise ValidationError({"book": "This book is currently out of stock."})

        if attrs["expected_return_date"] < timezone.now().date():
            raise ValidationError({"expected_return_date": "Expected return date cannot be in the past."})

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            book.inventory -= 1
            book.save()
            return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields


class BorrowingDetailSerializer(BorrowingSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + ("payments",)
