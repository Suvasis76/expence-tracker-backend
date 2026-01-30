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





class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.GET.get("date")
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        expenses = Expense.objects.filter(user=request.user)

        if date:
            expenses = expenses.filter(date=date)
        elif from_date and to_date:
            expenses = expenses.filter(date__range=[from_date, to_date])
        else:
            expenses = expenses.filter(date=now().date())

        expenses = expenses.order_by("-created_at")

        serializer = ExpenseSerializer(expenses, many=True)

        total = expenses.aggregate(
            total=Coalesce(
                Sum("amount"),
                0,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )["total"]

        return Response({
            "total": total,
            "expenses": serializer.data
        })
    
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

