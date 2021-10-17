import json
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sales.models import *
from users.models import Customer
from .serializers import *

class CashbackViewSet(ModelViewSet):
    queryset = Cashback.objects.all()
    serializer_class = CashbackSerializer

    def create(self, request, *args, **kwargs):
        d={}
        d['data'] = request.POST['data']
        data = json.loads(d['data']) # A partir do momento que dou um POST, ele vem em formato de string. Este comando converte a string recebida em JSON.
        
        # VERIFICA SE O CLIENTE JA ESTÁ SALVO, CASO CONTRÁRIO, CRIA UM NOVO CLIENTE NO SISTEMA, ASSIM FACILITANDO FUTURAS COMPRAS.
        try:
            customer = Customer.objects.get(document=data['customer']['document'])
        except:
            customer = Customer()
            customer.document = data['customer']['document']
            customer.name = data['customer']['name']
            customer.save()
        # =======
        
        cash = Cashback()
        cash.sold_at = data['sold_at']
        cash.customer = customer
        cash.save()
        t= 0
        for i in data['products']:
            pt = ProductType.objects.get(product_type = i['type'])
            prod = Product()
            prod.type = pt
            prod.value = i['value']
            prod.qty = i['qty']
            prod.save()
            cash.products.add(prod)
            cash.save()
            t+=float(i['value']) * float(i['qty'])
        cash.total= t
        cash.save()
        return Response(data['customer']['document'])