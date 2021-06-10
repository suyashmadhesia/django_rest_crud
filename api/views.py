import io

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.views import APIView

from .models import Student
from .serializers import StudentSerializer


# Normal class Based View(can be use in django)
@method_decorator(csrf_exempt, name='dispatch')
class StudentAPI(View):

    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        # print(python_data)
        id = python_data.get('id', None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        # json_data = JSONRenderer().render(serializer.data)
        # # print(json_data)
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        json_data = request.body
        data_stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=data_stream)
        serializer = StudentSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created Successfully !!'}
            res_data = JSONRenderer().render(res)
            return HttpResponse(res_data, content_type='application/json')
        res_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(res_data, content_type='application/json')

    def put(self, request, *args, **kwargs):
        json_data = request.body
        print(json_data)
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        id = python_data.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializer(stu, data=python_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'msg': 'Data Updated Successfully!!'
            }
            response_json = JSONRenderer().render(response)
            return HttpResponse(response_json, content_type='application/json')
        res_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(res_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        json_body = request.body
        data_stream = io.BytesIO(json_body)
        python_data = JSONParser().parse(stream=data_stream)
        id = python_data.get('id')
        print(id)
        stu = Student.objects.get(id=id)
        stu.delete()
        response = {
            'msg': 'Data Deleted Successfully !!!'
        }
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data, content_type='application/json')


# Function based Api View
# Now when we get post or do any CRUD thing we have to pass headers in which content-Type = 'application/json'
# is defined which in form of JSON

@api_view(['POST', 'GET', 'DELETE'])
def hello_world(request):
    if request.method == 'POST':
        data = request.data
        return Response({'msg': data})
    return Response({'msg': 'Hello world'})


# this class is using GenericAPIVIew which reduce lines of code for like validation, getting data from json and and
# returning data in json very easily

class StdAPI(APIView):

    def get(self, request, format=None):
        all_students = Student.objects.all()
        serializer = StudentSerializer(all_students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     return


# generic api view # no pk value is passed

class StListApi(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StCreateAPi(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# concrete View class in django rest_framework
'''
    ListApiView , Createapiview, Reteriveapiview, UdateAPIview,DestroyAPiView
    ListCreateAPIView, RetrieveUdateAPIView, RetrieveDestroyAPIView, RetriveUpdateDestroyAPIView
'''


class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# all concrete view is done same as StudentList(ListAPIView) class

# ViewSet class
'''
    A ViewSet class is simply a type of class based view, that does not provide any method handlers such as get()
    or post() , and instead provides actions such as list() and create() retrieve() update() partial_update() destroy() 
'''


class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(id=id)
            serial = StudentSerializer(stu)
            return Response(serial.data)

    # all functions all defined same as list
