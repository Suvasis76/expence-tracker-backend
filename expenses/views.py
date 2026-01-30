from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from .models import Expense
from .serializers import ExpenseSerializer

from rest_framework import status, permissions
from .serializers import RegisterSerializer

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from datetime import datetime





class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        expense = get_object_or_404(
            Expense, pk=pk, user=request.user
        )

        serializer = ExpenseSerializer(
            expense, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        expense = get_object_or_404(
            Expense, pk=pk, user=request.user
        )
        expense.delete()
        return Response({"message": "Expense deleted"}, status=200)

    

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

