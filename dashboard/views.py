import django_excel as excel
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import timezone
from django.utils.dateparse import parse_date
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

    items = User.objects.all()
    context = {"items": items, "title": "usuario"}
    return render(request, 'dashboard/users/read.html', context)


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

    items = Brand.objects.all()
    context = {"items": items, "title": "marca"}
    return render(request, 'dashboard/brands/read.html', context)


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
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    items = Department.objects.all()
    context = {"items": items, "title": "departamento"}
    return render(request, 'dashboard/departments/read.html', context)


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

    items = Size.objects.all()
    context = {"items": items, "title": "medida"}
    return render(request, 'dashboard/sizes/read.html', context)


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
    items = Register.objects.all()
    context = {"items": items, "title": "caja"}
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

    items = Product.objects.all()
    context = {"items": items, "title": "producto"}
    return render(request, "dashboard/products/read.html", context)


@login_required
def products_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        product = Product.objects.get(id=pk)
        if "borrar" in request.path:
            product.delete()
            return redirect("products")
    else:
        product = None

    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.save()

            return redirect("products")
        else:
            print(product_form.errors)

    else:
        product_form = ProductForm(instance=product)

    context = {"product_form": product_form}

    return render(request, 'dashboard/products/form.html', context)


@login_required
def businesses(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    items = Business.objects.all()
    context = {"items": items, "title": "negocio"}
    return render(request, "dashboard/businesses/read.html", context)


@login_required
def businesses_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        business = Business.objects.get(id=pk)
        contact = business.contact
        legal_data = business.legal_data
        address = legal_data.address

        if "borrar" in request.path:
            business.delete()
            return redirect("businesses")
    else:
        business = None
        contact = None
        legal_data = None
        address = None

    if request.method == "POST":
        business_form = BusinessForm(request.POST, instance=business)
        contact_form = ContactForm(request.POST, instance=contact)
        address_form = AddressForm(request.POST, instance=address)
        legal_data_form = LegalDataForm(request.POST, instance=legal_data)

        if business_form.is_valid() and contact_form.is_valid() and address_form.is_valid() and legal_data_form.is_valid():
            business = business_form.save(commit=False)

            contact = contact_form.save()
            address = address_form.save()

            legal_data = legal_data_form.save(commit=False)
            legal_data.address = address
            legal_data.save()

            business.contact = contact
            business.legal_data = legal_data

            business.save()

            return redirect("businesses")
        else:
            print(business_form.errors)
            print(contact_form.errors)
            print(address_form.errors)
            print(legal_data_form.errors)

    else:
        address_form = AddressForm(instance=address)
        legal_data_form = LegalDataForm(instance=legal_data)
        contact_form = ContactForm(instance=contact)
        business_form = BusinessForm(instance=business)

    context = {"address_form": address_form, "contact_form": contact_form,
               "business_form": business_form, "legal_data_form": legal_data_form}

    return render(request, 'dashboard/businesses/form.html', context)


@login_required
def clients(request):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    items = Client.objects.all()
    context = {"items": items, "title": "cliente"}
    return render(request, "dashboard/clients/read.html", context)


@login_required
def clients_manage(request, pk=None):
    if request.user.profile.type == "vendedor":
        return redirect("dashboard")

    if pk:
        client = Client.objects.get(id=pk)
        contact = client.contact
        legal_data = client.legal_data
        address = client.address

        if "borrar" in request.path:
            client.delete()
            return redirect("clients")
    else:
        client = None
        contact = None
        legal_data = None
        address = None

    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        contact_form = ContactForm(request.POST, instance=contact)
        address_form = AddressForm(request.POST, instance=address)
        legal_data_form = LegalDataForm(request.POST, instance=legal_data)

        if client_form.is_valid() and contact_form.is_valid() and address_form.is_valid() and legal_data_form.is_valid():
            client = client_form.save(commit=False)

            contact = contact_form.save()
            address = address_form.save()

            legal_data = legal_data_form.save(commit=False)
            legal_data.address = address
            legal_data.save()

            client.contact = contact
            client.legal_data = legal_data

            client.save()

            return redirect("clients")
        else:
            print(client_form.errors)
            print(contact_form.errors)
            print(address_form.errors)
            print(legal_data_form.errors)

    else:
        address_form = AddressForm(instance=address)
        legal_data_form = LegalDataForm(instance=legal_data)
        contact_form = ContactForm(instance=contact)
        client_form = ClientForm(instance=client)

    context = {"address_form": address_form, "contact_form": contact_form,
               "client_form": client_form, "legal_data_form": legal_data_form}

    return render(request, 'dashboard/clients/form.html', context)


@login_required
def sales(request):
    register_is_open = False
    sales_exist = Sale.objects.exists()

    if RegisterSession.objects.filter(user=request.user, closed_at__isnull=True).exists():
        register_is_open = True

    context = {"register_is_open": register_is_open,
               "sales_exist": sales_exist}

    return render(request, "dashboard/sales/read.html", context)


@login_required
def sales_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            client_id = int(data.get("client"))
            total = Decimal(data.get("total"))
            payment = Decimal(data.get("import"))
            change = Decimal(data.get("change"))
            payment_method = data.get("payment")
            products = data.get("products", [])

            register = RegisterSession.objects.filter(
                user=request.user, closed_at__isnull=True).first()
            client = Client.objects.get(id=client_id)

            sale = Sale.objects.create(
                register=register,
                client=client,
                total=total,
                payment=payment,
                payment_method=payment_method,
                change=change
            )

            for item in products:
                product_id = int(item.get("id"))
                product_qty = int(item.get("qty", 1))
                product_discount = Decimal(item.get("discount", 0))

                product = Product.objects.get(id=product_id)
                product.existence = product.existence - product_qty

                SaleProduct.objects.create(
                    sale=sale,
                    product=product,
                    quantity=product_qty,
                    discount=product_discount
                )

            return JsonResponse({"message": "¡venta creada!", "sale": sale.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "dashboard/sales/create.html")


@login_required
def autocomplete_clients(request):
    query = request.GET.get('c', '')
    clients = Client.objects.filter(name__icontains=query)[
        :10] if query else []
    data = list(clients.values('id', 'name'))
    return JsonResponse({'data': data})


@login_required
def autocomplete_products(request):
    query = request.GET.get('p', '')
    products = Product.objects.filter(name__icontains=query)[
        :10] if query else []
    data = list(products.values('id', 'name', "sale_price",
                "existence", "existence_min"))
    return JsonResponse({'data': data})


@login_required
def reports(request):
    sales = Sale.objects.all().order_by("-id")
    registers = Register.objects.all()
    clients = Client.objects.all()
    users = User.objects.all()

    register_id = request.GET.get("register")
    seller_id = request.GET.get("seller")
    client_id = request.GET.get("client")
    payment_method = request.GET.get("payment_method")
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")
    download_all = False

    if register_id:
        download_all = True
        sales = sales.filter(register__register_id=register_id)
    if seller_id:
        download_all = True
        sales = sales.filter(register__user_id=seller_id)
    if client_id:
        download_all = True
        sales = sales.filter(client=client_id)
    if payment_method:
        download_all = True
        sales = sales.filter(payment_method=payment_method)
    if date_start and date_end:
        download_all = True
        date_start_parsed = parse_date(date_start)
        date_end_parsed = parse_date(date_end)

        if date_start_parsed and date_end_parsed:
            download_all = True
            sales = sales.filter(created_at__date__range=[
                                 date_start_parsed, date_end_parsed])

    payments_methods = [
        {"value": "", "label": "todos los método"},
        {"value": "transferencia", "label": "transferencia"},
        {"value": "efectivo", "label": "efectivo"},
        {"value": "tarjeta de crédito", "label": "tarjeta de crédito"},
        {"value": "tarjeta de débito", "label": "tarjeta de débito"}
    ]

    context = {"sales": sales, "registers": registers,
               "clients": clients, "users": users, "payment_methods": payments_methods, "download_all": download_all}

    return render(request, "dashboard/reports/read.html", context)


def sales_invoice(request, pk):
    template_path = 'dashboard/pdf_template.html'
    sale = Sale.objects.get(id=pk)
    products = SaleProduct.objects.filter(sale=sale)

    context = {'sale': sale, 'products': products}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF', status=500)

    return response


def sales_csv(request, pk):
    headers = ["ID Venta", "Fecha", "Caja", "Vendedor", "Cliente", "Total", "Pago",
               "Cambio", "Método de Pago", "Producto", "Cantidad", "Descuento"]
    data = [headers]

    sale = Sale.objects.get(id=pk)
    sale_products = SaleProduct.objects.filter(sale=sale)

    first_row = True

    if sale_products.exists():
        for item in sale_products:
            if first_row:
                data.append([
                    sale.id,
                    sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    sale.register.register.name,
                    sale.register.user.username,
                    sale.client.name if sale.client else "Cliente eliminado",
                    sale.total,
                    sale.payment,
                    sale.change,
                    sale.payment_method,
                    item.product.name if item.product else "Producto eliminado",
                    item.quantity,
                    item.discount,
                ])
                first_row = False
            else:
                data.append([
                    "", "", "", "", "", "", "", "", "",
                    item.product.name if item.product else "Producto eliminado",
                    item.quantity,
                    item.discount,
                ])
    else:
        data.append([
            sale.id,
            sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            sale.register.register.name,
            sale.register.user.username,
            sale.client.name if sale.client else "Cliente eliminado",
            sale.total,
            sale.payment,
            sale.change,
            sale.payment_method,
            "Sin productos",
            "",
            "",
        ])

    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, "xlsx", file_name=f"venta_{sale.id}.xlsx")


@login_required
def export_sales_csv(request):
    headers = ["ID Venta", "Fecha", "Caja", "Vendedor", "Cliente", "Total", "Pago",
               "Cambio", "Método de Pago", "Producto", "Cantidad", "Descuento"]
    data = [headers]

    # Filtrar las ventas según los parámetros
    sales = Sale.objects.all().order_by("-id")

    register_id = request.GET.get("register")
    seller_id = request.GET.get("seller")
    client_id = request.GET.get("client")
    payment_method = request.GET.get("payment_method")
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    if register_id:
        sales = sales.filter(register__register_id=register_id)
    if seller_id:
        sales = sales.filter(register__user_id=seller_id)
    if client_id:
        sales = sales.filter(client=client_id)
    if payment_method:
        sales = sales.filter(payment_method=payment_method)
    if date_start and date_end:
        date_start_parsed = parse_date(date_start)
        date_end_parsed = parse_date(date_end)
        if date_start_parsed and date_end_parsed:
            sales = sales.filter(created_at__date__range=[
                                 date_start_parsed, date_end_parsed])

    # Generar los datos para el archivo Excel
    for sale in sales:
        sale_products = SaleProduct.objects.filter(sale=sale)
        first_row = True

        if sale_products.exists():
            for item in sale_products:
                if first_row:
                    data.append([
                        sale.id,
                        sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        sale.register.register.name,
                        sale.register.user.username,
                        sale.client.name if sale.client else "Cliente eliminado",
                        sale.total,
                        sale.payment,
                        sale.change,
                        sale.payment_method,
                        item.product.name if item.product else "Producto eliminado",
                        item.quantity,
                        item.discount,
                    ])
                    first_row = False
                else:
                    data.append([
                        "", "", "", "", "", "", "", "", "",
                        item.product.name if item.product else "Producto eliminado",
                        item.quantity,
                        item.discount,
                    ])
        else:
            data.append([
                sale.id,
                sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                sale.register.register.name,
                sale.register.user.username,
                sale.client.name if sale.client else "Cliente eliminado",
                sale.total,
                sale.payment,
                sale.change,
                sale.payment_method,
                "Sin productos",
                "",
                "",
            ])

    # Crear y retornar el archivo Excel
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, "xlsx", file_name="ventas_filtradas.xlsx")
