from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SpinRequestSerializer, SpinResponseSerializer
from .utils import spin_slot_machine_logic


class SpinSlotMachineView(APIView):
    def post(self, request):
        serializer = SpinRequestSerializer(data=request.data)
        if serializer.is_valid():
            initial_money = serializer.validated_data['initial_money']
            stavka = serializer.validated_data['stavka']
            result = spin_slot_machine_logic(initial_money, stavka)
            response_serializer = SpinResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
