from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
# from django.templatetags.static import static

# Create your views here.


def home(request):
    return render(request, 'login/home.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login/login.html', {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, 'login/login.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def business(request):
    return render(request, 'dashboard/business/business.html')


def business_add(request):
    return render(request, 'dashboard/business/add.html')


def panel(request):
    return render(request, 'adminlte/panel.html')


def clientes(request):
    return render(request, 'adminlte/clientes.html')


def clientes_consultar(request):
    return render(request, 'adminlte/clientes_consulta.html')
