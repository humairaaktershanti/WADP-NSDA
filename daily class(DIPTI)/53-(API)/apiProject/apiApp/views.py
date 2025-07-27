from django.shortcuts import render
from apiApp.serializers import *
from apiApp.models import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@api_view(['GET'])
def studentList(request):
    if request.method == 'GET':
        studentData = studentModel.objects.all()
        serializer = StudentSerializer(studentData, many=True)
        return Response({
            "success": True,
            "message": "Student List successfully get.",
            "studentData": serializer.data
        }, status=status.HTTP_200_OK)
       


# @api_view(['GET'])
# def studentList(request):
#     if request.method == 'GET':
#         studentData = studentModel.objects.all()
#         serializer = StudentSerializer(studentData, many=True)
#         return Response(serializer.data)
