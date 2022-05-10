from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import RawData, DataBatch
from .serializers import RawDataSerializer, DataBatchSerializer
from bson import ObjectId
import re

MODELS = {
        'rawdata'   : RawData,
        'databatch' : DataBatch
        }

SERIALIZERS = {
        'rawdata': RawDataSerializer,
        'databatch': DataBatchSerializer
        }


def index(request):
    return render(request, 'index.html')


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api(request, collection):
    Model = MODELS[collection.lower()]
    Serializer = SERIALIZERS[collection.lower()]
    filters,order_by = parse_params(request, Model)
    data = parse_data(request)

    if request.method == 'GET':
        query = Model.objects.filter(**filters).order_by(*order_by)
        resp = Serializer(query, many=True)

    elif request.method == 'POST':
        resp = Serializer(data=data, many=True)
        if resp.is_valid():
            resp.save()
        else:
            return Response(status=400)

    elif request.method == 'PUT':
        query = Model.objects.get(pk = ObjectId(data[0]['_id']))
        resp = Serializer(query, data=data[0])
        if resp.is_valid():
            resp.save()
        else:
            return Response(status=400)

    elif request.method == 'DELETE':
        # CUIDADO: TODOS OS MATCHES SERÃO APAGADOS!
        # Por segurança, se não for enviado nenhum filtro,
        # para não apagar tudo, é retornado um HTTP400
        if len(filters)>0:
            query = Model.objects.filter(**filters)
            for item in query:
                item.delete()
            query = Model.objects.filter(**filters)
            resp = Serializer(query, many=True)
        else:
            return Response(status=400)

    return Response(resp.data)


def parse_params(request, Model):
    params = {}
    filters = {}
    order_by = []

    #Tratando os valores recebidos
    for key, value in request.query_params.items():  
        if re.match( r'^\((.+,)+.+\)$', value):
            value_list = value[1:-1].split(',')
            params[key] = value_list
        else:
            params[key] = value

    #Separando os campos (filters,order_by,etc...)
    keys = list(params.keys())
    for key in keys:
        if key.split('__')[0] in Model.__dict__:
            filters[key] = params[key]

        elif key == 'order_by':
            if type(params[key]) is list:
                order_by = params[key]
            else:
                order_by = [params[key]]
        # <<<<  COLOCAR AQUI A OPÇÂO PARA OS 
        #       PRIMEIROS n ELEMENTOS
        #       OU ULTIMOS n ELEMENTOS

    return filters,order_by

def parse_data(request):
    if type(request.data) is dict:
        return [request.data]
    return request.data