from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView
from .views import RegisterView

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view()),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view()),
    path("auth/register/", RegisterView.as_view(), name="register"),
]
