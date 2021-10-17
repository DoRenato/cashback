from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json

from .models import *

# Create your views here.

def getCashback(request):
    dataCashback = serializers.serialize("json", Cashback.objects.all(), fields=('sold_at', 'total', 'customer', 'products'))

    cashback = json.loads(dataCashback)

    return JsonResponse({'cashback':cashback})
    # dataM = serializers.serialize("json", Membro.objects.all(), fields=('usuario', 'nome','avatar','id'))
    # dataP = serializers.serialize("json", Planejamento.objects.filter(id=id), fields=('membros'))
    # dataC = serializers.serialize("json", Convite.objects.filter(planejamento=id), fields=('convidado'))
    
    # j = json.loads(dataM)
    # p = json.loads(dataP)
    # c = json.loads(dataC)

    # return JsonResponse({'membros':j, 'plan':p, 'conv':c})