from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.


def landing(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("panel/")
        else:
            return render(request, "login/home.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/home.html")
