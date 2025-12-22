from django.contrib import admin
from borrowings.models import Borrowing

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book",
        "borrow_date",
        "expected_return_date",
        "actual_return_date"
    )
    list_filter = ("actual_return_date", "borrow_date")
    search_fields = ("user__email", "book__title")
