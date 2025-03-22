from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.


@login_required
def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def users(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    users = User.objects.all()
    return render(request, 'dashboard/users/read.html', {"users": users})


@login_required
def users_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        user = User.objects.get(id=pk)
        profile = Profile.objects.get(user=user)
        contact = profile.contact
        legal_data = profile.legal_data
        address = legal_data.address

        if "borrar" in request.path:
            user.delete()
            return redirect("users")
    else:
        user = None
        profile = None
        contact = None
        legal_data = None
        address = None

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        contact_form = ContactForm(request.POST, instance=contact)
        address_form = AddressForm(request.POST, instance=address)
        legal_data_form = LegalDataForm(request.POST, instance=legal_data)

        if user_form.is_valid() and profile_form.is_valid() and contact_form.is_valid() and address_form.is_valid() and legal_data_form.is_valid():
            user = user_form.save(commit=False)
            # Encripta la contraseña
            user.set_password(user_form.cleaned_data["password1"])
            user.save()

            # Guardar los datos individuales primero
            contact = contact_form.save()
            address = address_form.save()

            legal_data = legal_data_form.save(commit=False)
            legal_data.address = address  # Asigna la dirección al modelo LegalData
            legal_data.save()

            # Crear el perfil con los datos guardados
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.contact = contact
            profile.legal_data = legal_data
            profile.save()

            return redirect("users")
        else:
            print(user_form.errors)
            print(profile_form.errors)
            print(contact_form.errors)
            print(address_form.errors)
            print(legal_data_form.errors)
    else:
        address_form = AddressForm(instance=address)
        legal_data_form = LegalDataForm(instance=legal_data)
        contact_form = ContactForm(instance=contact)
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)

    context = {"address_form": address_form, "contact_form": contact_form,
               "profile_form": profile_form, "user_form": user_form, "legal_data_form": legal_data_form}

    return render(request, 'dashboard/users/form.html', context)


def signout(request):
    logout(request)
    return redirect("home")


@login_required
def brands(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    brands = Brand.objects.all()
    return render(request, 'dashboard/brands/read.html', {"brands": brands})


@login_required
def brands_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        brand = Brand.objects.get(id=pk)
        if "borrar" in request.path:
            brand.delete()
            return redirect("brands")
    else:
        brand = None

    if request.method == "POST":
        brand_form = BrandForm(request.POST, instance=brand)

        if brand_form.is_valid():
            brand = brand_form.save()

            return redirect("brands")
        else:
            print(brand_form.errors)
    else:
        brand_form = BrandForm(instance=brand)

    context = {"brand_form": brand_form}

    return render(request, 'dashboard/brands/form.html', context)


@login_required
def departments(request):

    departments = Department.objects.all()
    return render(request, 'dashboard/departments/read.html', {"departments": departments})


@login_required
def departments_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        department = Department.objects.get(id=pk)
        if "borrar" in request.path:
            department.delete()
            return redirect("departments")
    else:
        department = None

    if request.method == "POST":
        department_form = DepartmentForm(request.POST, instance=department)

        if department_form.is_valid():
            department = department_form.save()

            return redirect("departments")
        else:
            print(department_form.errors)
    else:
        department_form = DepartmentForm(instance=department)

    context = {"department_form": department_form}

    return render(request, 'dashboard/departments/form.html', context)


@login_required
def sizes(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    sizes = Size.objects.all()
    return render(request, 'dashboard/sizes/read.html', {"sizes": sizes})


@login_required
def sizes_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        size = Size.objects.get(id=pk)
        if "borrar" in request.path:
            size.delete()
            return redirect("sizes")
    else:
        size = None

    if request.method == "POST":
        size_form = SizeForm(request.POST, instance=size)

        if size_form.is_valid():
            size = size_form.save()

            return redirect("sizes")
        else:
            print(size_form.errors)
    else:
        size_form = SizeForm(instance=size)

    context = {"size_form": size_form}

    return render(request, 'dashboard/sizes/form.html', context)


@login_required
def registers(request):
    registers = Register.objects.all()

    context = {
        "registers": registers,
    }

    return render(request, "dashboard/registers/read.html", context)


@login_required
def registers_manage(request, pk=None):
    if pk:
        register = Register.objects.get(id=pk)
        if "borrar" in request.path:
            register.delete()
            return redirect("registers")
    else:
        register = None

    if request.method == "POST":
        register_form = RegisterForm(request.POST, instance=register)

        if register_form.is_valid():
            register = register_form.save()

            return redirect("registers")
        else:
            print(register_form.errors)
    else:
        register_form = RegisterForm(instance=register)

    context = {"register_form": register_form}

    return render(request, "dashboard/registers/form.html", context)


@login_required
def registers_open(request, pk):
    register = Register.objects.get(id=pk)
    register_session = None

    if RegisterSession.objects.filter(user=request.user, closed_at__isnull=True).exists():
        messages.error(request, "Ya tiene una caja abierta.")
        messages.error(request, "Cierre su caja antes de abrir otra.")
        return redirect("registers")

    if request.method == "POST":
        register_form = RegisterSessionForm(request.POST, instance=register)
        register_session_form = RegisterSessionForm(
            request.POST, instance=register_session)

        if register_form.is_valid() and register_session_form.is_valid():
            register = register_form.save(commit=False)
            register_session = register_session_form.save(commit=False)

            register.state = "a"
            register.save()

            register_session.user = request.user
            register_session.register = register
            register_session.save()

            return redirect("registers")
        else:
            print(register_form.errors)
            print(register_session_form.errors)
    else:
        register_form = RegisterForm(instance=register)
        register_session_form = RegisterSessionForm()

    context = {
        "register_form": register_form,
        "register_session_form": register_session_form,
    }

    return render(request, "dashboard/registers/open.html", context)


@login_required
def registers_close(request, pk):
    register = Register.objects.get(id=pk)
    register_session = RegisterSession.objects.get(
        register=register, closed_at__isnull=True)

    if register_session.user != request.user:
        messages.error(request, "Esta caja no fue abierta por usted.")
        return redirect("registers")

    form = RegisterSessionForm(request.POST or None, instance=register_session)
    if request.method == "POST":
        if form.is_valid():
            register_session = form.save(commit=False)
            register_session.closed_at = timezone.now()

            total_sold = register_session.total_sold or 0
            register_session.final_balance = register_session.initial_amount + total_sold

            register_session.save()

            register.state = "c"
            register.save()

            return redirect("registers")
        else:
            print(form.errors)

    context = {
        "register": register,
        "register_session": register_session,
        "form": form,
    }

    return render(request, "dashboard/registers/close.html", context)


@login_required
def products(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    products = Product.objects.all()
    return render(request, "dashboard/products/read.html", {"products": products})


@login_required
def products_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        product = Product.objects.get(id=pk)
        brand = product.brand
        department = product.department
        size = product.size
        if "borrar" in request.path:
            product.delete()
            return redirect("products")
    else:
        product = None
        brand = None
        department = None
        size = None

    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product)
        brand_form = BrandForm(request.POST, instance=brand)
        department_form = DepartmentForm(request.POST, instance=department)
        size_form = SizeForm(request.POST, instance=size)

        if product_form.is_valid() and brand_form.is_valid() and department_form.is_valid() and size_form.is_valid():
            product = product_form.save(commit=False)

            brand = brand_form.save()
            department = department_form.save()
            size = size_form.save()

            product.brand = brand
            product.department = department
            product.size = size

            product.save()

            return redirect("products")
        else:
            print(product_form.errors)
            print(brand_form.errors)
            print(department_form.errors)
            print(size_form.errors)
    else:
        product_form = ProductForm(instance=product)
        brand_form = BrandForm(instance=brand)
        department_form = DepartmentForm(instance=department)
        size_form = SizeForm(instance=size)

    context = {"product_form": product_form, "brand_form": brand_form,
               "department_form": department_form, "size_form": size_form}

    return render(request, 'dashboard/products/form.html', context)
