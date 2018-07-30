from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .models import Task
from .forms import TaskCreateForm, RegisterForm, LoginForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = "task/reg.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        """ Overriding base post method to encrpyt user password and validate registration from data."""

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            return redirect("/login")
        else:
            if 'username' in form.errors:
                messages.warning(request, 'Username does not meet requirements.  Please try again.')
            if 'password' in form.errors:
                messages.warning(request, 'Passwrod does not meet requirements.  Please try again.')
            return redirect("/")


class LoginView(View):
    form_class = LoginForm
    template_name = "task/log.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form":form})
    
    def post(self, request):
        form = LoginForm()
        submitted_form = self.form_class(request.POST)
        if submitted_form.is_valid():
            try: 
                username = submitted_form.cleaned_data["username"]
                password = submitted_form.cleaned_data["password"]
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    messages.warning(request, 'Username or password does not match our records')
                    return redirect("/login")
            except: 
                messages.warning(request, 'Username or password does not match our records')
                return render(request, self.template_name, {"form":form})
            

class HomeView(LoginRequiredMixin, View):
    """ Starting webpage for logged in user.  
    
    Has django mixin requiring credentials or 
    the user will be redirected to the login screen.

    """

    template_name = "task/home.html"
    queryset = Task.objects.all()

    def get(self, request):
        total_tasks = Task.objects.all().filter(creator__id = str(self.request.user.id)).count()
        return render(request, self.template_name, {"total_tasks":total_tasks})


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create view for new tasks with defined html template name paired with object."""

    model = Task 
    fields = ["name", "description"]
    template_name = "task/task_create.html"
    template_name_suffix = "_create"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().filter(creator__id = str(self.request.user.id)).count()
        return context

    # If valid form work correctly...need something if it doesn't
    def form_valid(self, form): 
        form.instance.creator = self.request.user
        self.object = form.save()
        print("success")
        return redirect("/home")

    def form_invalid(self, form):
        print(form.errors)
        if "name" in form.errors:
            messages.warning(self.request, 'Name must be between 5 and 100 characters')
        if "description" in form.errors:
            messages.warning(self.request, 'Description must be between 5 and 250 characters')
        return redirect("/create")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["name", "description"]
    template_name = "task/task_update.html"
    success_url = "/all_tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().filter(creator__id = str(self.request.user.id)).count()
        return context


class TaskListView(LoginRequiredMixin, ListView): 
    model = Task 
    template_name = "task/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().filter(creator__id = str(self.request.user.id)).count()
        return context

    def get_queryset(self, *args, **kwargs):
        q_set = Task.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            q_set = q_set.filter(
                Q(name__icontains = query) |
                Q(description__icontains = query)
            )
        return q_set.filter(creator__id = str(self.request.user.id))


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task 
    success_url = reverse_lazy("all_tasks")
    template_name_suffix = "_delete"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = TaskCreateForm
        context["total_tasks"] = Task.objects.all().filter(creator__id = str(self.request.user.id)).count()
        return context


class StatusUpdateView(View):
    """View updating task status."""

    lookup_field = "pk"

    def post(self, request, pk):
        task = Task.objects.get(id = pk)
        if(request.POST["change"] == "to_yes"):
            task.status = "YES"
        else:
            task.status = "NO"
        task.save()
        return redirect("/home")


def logout_view(request):
    """Clears session data created at login."""

    logout(request)
    return redirect("/login")
