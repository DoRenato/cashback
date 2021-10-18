import json
from django.core import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sales.models import *
from users.models import Customer
from .serializers import *
from .valida_cpf import validate_cpf


class CashbackViewSet(ModelViewSet):
    queryset = Cashback.objects.all()
    serializer_class = CashbackSerializer

    def create(self, request, *args, **kwargs):
        data= request.data # Armazenda o JSON enviado neste dicionario chamado 'data'.

        # VERIFICA SE O CLIENTE JA ESTÁ SALVO NO SISTEMA, CASO CONTRÁRIO, CRIA UM NOVO CLIENTE SE O CPF FOR VÁLIDO ATRAVÉS DA FUNÇÃO valida_cpf.
        try:
            customer = Customer.objects.get(document=data['customer']['document'])
        except:
            if validate_cpf(data['customer']['document']) == False:
                return Response("Invalid CPF.")
            else:
                customer = Customer()
                customer.document = data['customer']['document']
                customer.name = data['customer']['name']
                customer.save()
                
        # =======
        
        # Verifica se o formato da data é válido ====
        try:
            cash = Cashback()
            cash.sold_at = data['sold_at']
            cash.customer = customer
            cash.save()
        except:
            customer.delete()
            return Response("data invalida")
        #=========

        t= 0
        for product in data['products']:
            pt = ProductType.objects.get(product_type = product['type'])
            prod = Product()
            prod.type = pt
            prod.value = product['value']
            prod.qty = product['qty']
            prod.save()
            cash.products.add(prod)
            cash.save()
            t+=float(product['value']) * float(product['qty'])
        cash.total= t
        cash.save()
        return Response(data['customer']['document'])