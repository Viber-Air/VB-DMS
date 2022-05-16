from multiprocessing import Pool
from statistics import fmean, stdev
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Module, RawData
from .serializers import UserProfileSerializer, ModuleSerializer, RawDataSerializer
from bson import ObjectId
import re


#====================================================================#
#                       /api/module & /api/rawdata                   #
#====================================================================#

MODELS = {
        'userprofile'   : UserProfile,
        'module'        : Module,
        'rawdata'       : RawData,
        }

SERIALIZERS = {
        'userprofile'   : UserProfileSerializer,
        'module'        : ModuleSerializer,
        'rawdata'       : RawDataSerializer,
        }

@api_view(['GET', 'POST', 'DELETE'])
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
            erro = resp.errors
            return Response(resp.errors,status=400)

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


#====================================================================#
#                           /api/api_databatch                       #
#====================================================================#

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_databatch(request):
    params = request.query_params
    window_size = int(params['window_size'])

    #get rawdatas
    filters,_ = parse_params(request, RawData)
    raw_datas = RawData.objects.filter(**filters)

    #split rawdatas
    raw_batches = []
    n_batches = int( len(raw_datas)/window_size )
    for i in range(n_batches):
        start = i*window_size
        end   = start+window_size
        raw_batches.append(raw_datas[start:end])

    #process requested features
    with Pool() as p:
        processed_batches = p.map(process_databatch, raw_batches)
    
    #return response
    for batch in processed_batches:
        batch['module_num']  = params['module_num']
        batch['window_size'] = params['window_size']
    return Response(processed_batches)

def process_databatch(raw_batch):
    resp = {}
    times = [raw_data.timestamp for raw_data in raw_batch]
    measures = {}
    for raw_data in raw_batch:
        for measure in raw_data.measures:
            try:
                measures[measure['name']].append(measure['value'])
            except KeyError:
                measures[measure['name']] = [measure['value']]

    resp['starting_timestamp']  = min(times)
    resp['ending_timestamp']    = max(times)
    resp['window_size']         = len(raw_batch)
    #TODO normalization
    
    #process time features
    time_features = {}
    time_features['batch_mean'] = [{'name':name, 'value':fmean(value)} for name,value in measures.items()]
    time_features['batch_std']  = [{'name':name, 'value':stdev(value)} for name,value in measures.items()]
    resp['time_features'] = time_features
    #TODO other batch analysis
    #TODO rolling mean
    #TODO freq and time_freq analysis
    return resp

#====================================================================#
#                             USEFUL FUNCS                           #
#====================================================================#

def parse_params(request, Model):
    params = {}
    filters = {}
    order_by = []

    #Tratando os valores recebidos
    for key, value in request.query_params.items():  
        if re.match( r'^\((.+,)+.+\)$', value):
            value_list = value[1:-1].split(',')
            params[key] = value_list
        elif key.startswith('_id'):
            params[key] = ObjectId(value)
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
    resp = []
    if type(request.data) is dict:
        resp = [request.data]
    else:
        resp = request.data

    for data in resp:
        for key,value in data.items():
            if key.startswith('_id'):
                data[key] = ObjectId(value)
    return resp
