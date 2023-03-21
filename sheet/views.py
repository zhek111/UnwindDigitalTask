from django.db.models import Sum
from rest_framework import generics

from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_cost_rub = self.__get_total_cost_rub()
        response.data = {
            'results': response.data,
            'total': total_cost_rub,
        }
        return response

    def __get_total_cost_rub(self):
        return self.get_queryset().aggregate(
            total_cost_rub=Sum('cost_rub'))['total_cost_rub']
