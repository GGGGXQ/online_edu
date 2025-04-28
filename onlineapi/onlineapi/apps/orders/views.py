from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderModelSerializer


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    """创建订单"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
