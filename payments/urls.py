from django.urls import path, include
from rest_framework import routers
from payments.views import SuccessView, CancelView, PaymentViewSet

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("success/", SuccessView.as_view(), name="payment-success"),
    path("cancel/", CancelView.as_view(), name="payment-cancel"),
    path("", include(router.urls)),
]

app_name = "payments"
