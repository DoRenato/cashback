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
        data= request.data # Armazenda o JSON recebido na requisição POST neste dicionario python.

        # VERIFICA SE O CLIENTE JA ESTÁ SALVO NO SISTEMA, CASO CONTRÁRIO, CRIA UM NOVO CLIENTE SE O CPF FOR VÁLIDO UTILIZANDO A FUNÇÃO validate_cpf.
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
            return Response("Invalid Date")
        #=========

        t= 0
        cashback_total = 0
        for product in data['products']:
            if validate_type(product['type']):
                if float(product['value']) <= 0 or float(product['qty']) <= 0: # se for passado um valor ou quantidade menor igual a ZERO, a API irá ignorar este produto e seguir para o proximo valor válido.
                    continue
                pt = ProductType.objects.get(product_type = product['type']) # puxa do banco um produto onde o tipo seja igual ao que foi recebido, assim podendo ver e associar ao cashback do mesmo.
                prod = Product() # gerando um novo modelo de produto para ficar salvo no banco.
                prod.type = pt # Como esse campo é uma chave estrangeira, ele associa o produto ja cadastrado do banco à esse campo.
                prod.value = product['value']
                prod.qty = product['qty']
                prod.save()
                cash.products.add(prod) # sempre cada novo produto do laço é adicionado a esse campo ManyToMany
                cash.save()
                t+=float(product['value']) * float(product['qty']) #Variável onde sempre irá incrementar o valor de cada produto para ao final ter o valor total da compra.
                cashback_total += (float(product['value']) * float(product['qty'])) * (float(pt.cashback)/100) # mesma logica da anterior, só que para ter o cashback total da compra.

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

            # Etapa final. Os dados necessários estão sendo salvos em 'data', na linha seguinte, utilizei o modulo 'requests'
            # para enviá-los para a API externa e gerar o cashback de fato.
            data={'document':customer.document, 'cashback': cash.cashback}
            requests.post('https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback', data)
            return Response("Cashback generated.")
        