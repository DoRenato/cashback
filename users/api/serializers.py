from rest_framework.serializers import ModelSerializer
from users.models import Customer

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ('document','name')