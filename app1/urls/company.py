from django.urls import path
from app1.views import company as views

urlpatterns = [
    path('list/', views.CompanyList.as_view()),
    path('create/', views.CompanyCreate.as_view()),
    path('update/', views.CompanyUpdate.as_view()),
    path('delete/', views.CompanyDelete.as_view())
]
