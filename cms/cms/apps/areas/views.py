from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ViewSet, GenericViewSet

# addresses/
from users.models import User
from .models import Address
from .serializers import UserAddressesSerializer


class Addresses(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        addresses = request.user.addresses.filter(is_deleted=False)
        serializer = UserAddressesSerializer(addresses, many=True)
        data = {
            'addresses': serializer.data,
            'limit': 15,
            'default_address_id': request.user.default_address.id if request.user.default_address else 0
        }
        return Response(data)

    def destroy(self, request, pk):
        address = Address.objects.get(pk=pk)
        address.is_deleted = True
        address.save()
        return Response(status=204)

    def update(self, request, pk):
        address = Address.objects.get(pk=pk)
        data = request.data
        serializer = UserAddressesSerializer(instance=address, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = UserAddressesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        user = request.user
        address = Address.objects.get(pk=pk)
        user.default_address = address
        user.save()

        return Response({"message": "ok"})
