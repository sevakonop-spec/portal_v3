from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('directory/', views.directory, name='directory'),
    path('org/', views.org_tree, name='org_tree'),
]