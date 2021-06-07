import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def student_all(request):
    if request.method == 'PUT':
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
    if request.method == 'GET':
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
        json_data = JSONRenderer().render(serializer.data)
        # print(json_data)
        return HttpResponse(json_data, content_type='application/json')
    if request.method == "POST":
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
    if request.method == "DELETE":
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


