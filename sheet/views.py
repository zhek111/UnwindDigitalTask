from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_cost_rub = sum([order.cost_rub for order in self.get_queryset()])
        response.data = {
            'results': response.data,
            'total': total_cost_rub,
        }
        return response
