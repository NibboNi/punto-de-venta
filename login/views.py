from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
# from django.templatetags.static import static

# Create your views here.


def home(request):
    additional_css = "landing.css"

    return render(request, 'login/home.html', {"additional_css": additional_css})


def login(request):
    additional_css = "login.css"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login/login.html', {
                "additional_css": additional_css,
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, 'login/login.html', {"additional_css": additional_css})
