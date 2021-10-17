from rest_framework.serializers import ModelSerializer, SerializerMethodField
from sales.models import *
from users.api.serializers import *


class ProductSerializer(ModelSerializer):
    type = SerializerMethodField()
    class Meta:
        model = Product
        fields = ('type','value','qty')

    def get_type(self, obj):
        return "%s" %(obj.type)


class CashbackSerializer(ModelSerializer):
    customer = CustomerSerializer()
    products = ProductSerializer(many=True)
    # products = SerializerMethodField()
    class Meta:
        model = Cashback
        fields = ('sold_at', 'customer','total','products')