from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import requests

from sales.models import *
from users.models import Customer
from .serializers import *
from .validations import validate_cpf, validate_type


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
        
        # "Verifica" se o formato da data é válido. Como a data será salva em um modelo DateTimeField, se o formato não estiver de acordo, então não salva. ====
        try:
            cash = Cashback()
            cash.sold_at = data['sold_at']
            cash.customer = customer
            cash.save()
        except:
            cash.delete()
            return Response("data invalida")
        #=========

        t= 0
        cashback_total = 0
        for product in data['products']:
            if validate_type(product['type']):
                if float(product['value']) <= 0 or float(product['qty']) <= 0: # se for passado um valor ou quantidade menor igual a ZERO, ele a API irá ignorar esta compra e seguir para o proximo valor válido.
                    continue
                pt = ProductType.objects.get(product_type = product['type'])
                prod = Product()
                prod.type = pt
                prod.value = product['value']
                prod.qty = product['qty']
                prod.save()
                cash.products.add(prod)
                cash.save()
                t+=float(product['value']) * float(product['qty'])
                cashback_total += (float(product['value']) * float(product['qty'])) * (float(pt.cashback)/100)

        t='{:.2f}'.format(t) # apenas para adicionar uma casa decimal à direita, já que por padrão estão vindo com uma.

        if float(t) != float(data['total']) or float(t) <= 0: # Se o total for ZERO ou diferente do somado na API, todos os dados serão descartados - com excessão do cliente.
            for prod in cash.products.all():
                prod.delete()
            cash.delete()
            return Response("Invalid Total.")
        else:
            cash.total= t
            cash.cashback = cashback_total
            cash.save()
            return Response("Todos os dados são válidos.")
        