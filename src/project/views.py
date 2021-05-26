import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def index(request):
    message = 'Server is live, current time is '
    return Response(data=message, status=status.HTTP_200_OK)
