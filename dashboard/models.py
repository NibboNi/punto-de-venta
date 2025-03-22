from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Contact(models.Model):
    phone = models.CharField(max_length=15, verbose_name="teléfono")
    cellphone = models.CharField(max_length=15, verbose_name="celular")
    email = models.EmailField()
    social_url = models.URLField(
        verbose_name="url social", null=True, blank=True)

    def __str__(self):
        return "Contacto"


class Address(models.Model):
    street = models.CharField(
        max_length=255, verbose_name="calle", null=False, blank=False)
    exterior_num = models.CharField(
        max_length=50, verbose_name="número ext.", null=False, blank=False)
    interior_num = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="número int.")
    colony = models.CharField(
        max_length=255, verbose_name="colonia", null=False, blank=False)
    city = models.CharField(
        max_length=255, verbose_name="ciudad", null=False, blank=False)
    state = models.CharField(
        max_length=255, verbose_name="estado", null=False, blank=False)
    postal_code = models.CharField(
        max_length=10, verbose_name="codigo postal", null=False, blank=False)

    def __str__(self):
        return f"{self.street} {self.exterior_num}, {self.colony}, {self.city}"


class LegalData(models.Model):
    rfc = models.CharField(max_length=13, unique=True)
    company_name = models.CharField(
        max_length=255, verbose_name="razón social")
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f"{self.company_name} - {self.rfc}"


class Business(models.Model):
    legal_data = models.ForeignKey(
        LegalData, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True)
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)


class Client(models.Model):
    legal_data = models.ForeignKey(
        LegalData, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True)
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)


class Profile(models.Model):
    USER_TYPES = [
        ("admin", "Administrador"),
        ("vendedor", "Vendedor"),
    ]

    USER_GENDERS = [
        ("m", "masculino"),
        ("f", "femenino"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20, choices=USER_TYPES, default="vendedor", verbose_name="tipo")
    name = models.CharField(
        max_length=20, verbose_name="nombre", default="", blank=False)
    surnames = models.CharField(
        max_length=100, verbose_name="apellidos", default="", blank=False)
    gender = models.CharField(
        max_length=20, choices=USER_GENDERS, default="m", verbose_name="género")
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True)
    legal_data = models.ForeignKey(
        LegalData, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Brand(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False)
    description = models.TextField(
        verbose_name="descripción", max_length=200, blank=True, null=True)
    existence = models.IntegerField(verbose_name="existencia", default=1)
    existence_min = models.IntegerField(
        verbose_name="existencia mínima", default=1)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.00, verbose_name="precio de venta")
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name="marca")
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, default=1, verbose_name="departamento")
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, default=1, verbose_name="unidad de medida")


class Register(models.Model):
    REGISTER_STATES = [
        ("a", "abierto"),
        ("c", "cerrado"),
    ]

    key = models.CharField(
        max_length=3, verbose_name="clave", null=False, blank=False, unique=True)
    name = models.CharField(
        max_length=100, verbose_name="nombre", null=False, blank=False,)
    state = models.CharField(
        max_length=20, choices=REGISTER_STATES, default="c", verbose_name="estado")

    def __str__(self):
        return self.name


class RegisterSession(models.Model):
    register = models.ForeignKey(
        Register, on_delete=models.CASCADE, verbose_name="Caja")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="usuario", default="")
    closed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha y hora de cierre")
    opened_at = models.DateTimeField(
        default=now, verbose_name="Fecha y hora de apertura")
    initial_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Monto inicial")
    total_sold = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Total vendido")
    final_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Saldo final")

    def __str__(self):
        return self.register.name
