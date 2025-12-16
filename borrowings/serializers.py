from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_title",
            "user",
        )
        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")

    def validate(self, attrs):
        data = super().validate(attrs)
        book = data["book"]

        if book.inventory == 0:
            raise ValidationError({"book": "This book not allow. inventory is 0."})

        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]

            if book.inventory == 0:
                raise ValidationError({"book": "The delivery failed, the book was simply taken away."})
            book.inventory -= 1
            book.save()

        borrowing = Borrowing.objects.create(**validated_data)

        return borrowing
