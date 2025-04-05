from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "Пользователь успешно зарегистрирован!"}, status=status.HTTP_201_CREATED)


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        return Response({'balance': profile.balance})

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Укажи сумму'}, status=400)
        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Неверная сумма'}, status=400)

        profile = request.user.userprofile
        profile.balance += amount
        profile.save()
        return Response({'balance': profile.balance}, status=status.HTTP_200_OK)