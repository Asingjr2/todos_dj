from django.urls import path

from . import views 
from .views import (
    RegisterView, 
    LoginView, 
    TaskListView, 
    TaskDetailView, 
    TaskDeleteView,
    TaskCreateView,
    TaskUpdateView,
    HomeView, 
    StatusUpdateView
)


urlpatterns = [
    # General paths
    path("", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    # Task Urls
    path("home", HomeView.as_view(), name="home"),
    path("create", TaskCreateView.as_view(), name="task_create"),
    path("<uuid:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("update/<uuid:pk>", TaskUpdateView.as_view(), name="task_update"),
    path("delete/<uuid:pk>", TaskDeleteView.as_view(), name="task_delete"),
    path("all_tasks", TaskListView.as_view(), name="all_tasks"),
    path("status_update/<uuid:pk>", StatusUpdateView.as_view(), name="status_update")
]