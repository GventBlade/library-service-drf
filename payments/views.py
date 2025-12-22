from rest_framework import viewsets, mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(borrowing__user=self.request.user)
        return self.queryset


class SuccessView(APIView):
    def get(self,request):
        session_id = request.query_params.get('session_id')
        if session_id:
            payment = get_object_or_404(Payment, session_id=session_id)
            payment.status = "PAID"
            payment.save()
            return Response({"message": f"Payment {payment.id} was successful! Status updated to PAID."})
        return Response({"error": "No session_id found in request."}, status=400)

class CancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment was canceled. You can pay later."})
