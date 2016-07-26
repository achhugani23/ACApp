from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, viewsets
from ACApps.models import Account
from ACApps.permissions import IsAccountOwner
from ACApps.serializers import AccountSerializer
from rest_framework.response import Response

class AccountViewSet(viewsets.ModelViewSet):
	lookup_field = 'username'
	queryset = Account.objects.all()
	serializer_class = AccountSerializer

	def getpermissions(self):
		if self.request.method in permissions.SAFE_METHODS:
			return (permissions.Allowany(), )
		if self.request.method == 'POST':
			return (permissions.Allowany(), )
		return (permissions.IsAuthenticated(), IsAccountOwner(), )
	def create(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			Account.objects.create_user(**serializer.validated_data)

		return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

		return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)