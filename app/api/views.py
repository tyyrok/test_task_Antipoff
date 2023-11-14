from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from api.serializers import CadastralNumberSerializer, \
                HistorySerializer
from api.models import CadastralNumber, History
from api.tasks import mock_request_to_third_party

class QueryView(APIView):
    """POST View for making request with number, long, alt"""
    serializer_class = CadastralNumberSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            record = History.objects.create(
                request_type='query',
                number=instance
            )
            mock_request_to_third_party.delay(instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultView(RetrieveAPIView):
    """GET View for getting result by providing number"""
    serializer_class = CadastralNumberSerializer
    
    def get_object(self):
        try:
            number = CadastralNumber.objects.get(number=self.kwargs['number'])
        except:
            raise ValidationError(detail={'detail': 'Incorrect number of the object'})
        History.objects.create(
            request_type='result',
            number=number
        )
        return number    

class PingView(APIView):
    """View for check whether server is up"""
    def get(self, request):
        data = {"data": "pong"}
        return Response(data=data, status=status.HTTP_200_OK)

class HistoryView(ListAPIView):
    serializer_class = HistorySerializer
    
    def get_queryset(self):
        queryset = (
            History.objects.filter(number__number=self.kwargs['number'])
                            .order_by('-timestamp')
        )
                                
        if len(queryset) == 0:
            raise ValidationError(
                detail={'detail': 'Incorrect number of the object'}
            )
        History.objects.create(
            request_type='history', 
            number=queryset[0].number
        )
        return queryset
