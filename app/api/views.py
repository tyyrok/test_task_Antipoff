from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import CadastralNumberSerializer

class QueryView(APIView):
    serializer_class = CadastralNumberSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ResultView(APIView):
    pass

class PingView(APIView):
    """View for check whether server is up"""
    def get(self, request):
        data = {"data": "pong"}
        return Response(data=data, status=status.HTTP_200_OK)

class HistoryView(APIView):
    pass
