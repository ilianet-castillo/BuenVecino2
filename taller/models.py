from django.db import models


class Contact(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=255, help_text='Nombre del contacto')
    address = models.TextField(verbose_name='Dirección', help_text='Dirección del contacto')
    email = models.EmailField(verbose_name='Correo electrónico', help_text='Correo electrónico del contacto')
    phone = models.PositiveIntegerField(verbose_name='Teléfono', help_text='Teléfono del contacto')
    tcp = models.CharField(verbose_name='TCP', max_length=255, help_text='Nombre del trabajador por cuenta propia')
    nit = models.PositiveIntegerField(verbose_name='NIT', help_text='Número de identidad del contacto')
    no_check_cup = models.PositiveIntegerField(verbose_name='# de la cuenta en cup',
                                               help_text='Número de cuenta de CUP del contacto')

    class Meta:
        verbose_name = 'contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return self.name


class Type(models.Model):
    type = models.CharField(verbose_name='Tipo', max_length=255, help_text='Tipo de factura')
    title = models.CharField(verbose_name='Título', max_length=255, help_text='Título de la factura')

    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.title


class UnitMeasurement(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=255, unique=True, help_text='Unidad de médida')

    class Meta:
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'Unidades de medida'

    def __str__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=255, help_text='Nombre de la empresa')
    phone = models.PositiveIntegerField(verbose_name='Télefono', help_text='# de teléfono')
    address = models.TextField(verbose_name='Dirección', help_text='Dirección de la empresa')
    comments = models.TextField(verbose_name='Comentarios', help_text='Comentarios')

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.name


class Mechanical(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=255, help_text='Nombre del mecánico')
    last_name = models.CharField(verbose_name='Apellidos', max_length=255, help_text='Apellidos del mecánico')
    ci = models.PositiveIntegerField(verbose_name='Canet Identidad', help_text='Carnet Identidad')
    address = models.TextField(verbose_name='Dirección', help_text='Dirección')

    class Meta:
        verbose_name = 'mecánico'
        verbose_name_plural = 'Mecánicos'

    def __str__(self):
        return self.name


class Piece(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=255, unique=True, help_text='Nombre de la pieza')

    class Meta:
        verbose_name = 'pieza'
        verbose_name_plural = 'Piezas'

    def __str__(self):
        return self.name


class MethodPayment(models.Model):
    type = models.CharField(verbose_name='Tipo', max_length=255, unique=True, help_text='Tipo de forma de pago')

    class Meta:
        verbose_name = 'método de pago'
        verbose_name_plural = 'Métodos de pago'

    def __str__(self):
        return self.type


class ServiceGuarantee(models.Model):
    description = models.TextField(verbose_name='Descripción', unique=True,
                                   help_text="Pautas de la garantía del servicio ofrecido")

    class Meta:
        verbose_name = 'garantía de servicio'
        verbose_name_plural = 'Garantías de servicio'

    def __str__(self):
        return self.description


class Vehicle(models.Model):
    mark = models.CharField(verbose_name='Marca', max_length=255, help_text='Marca del vehiculo')
    model = models.CharField(verbose_name='Modelo', max_length=255, help_text='Modelo del vehiculo')
    tag = models.CharField(verbose_name='Chapa', max_length=7, help_text='Chapa del vehiculo')
    enterprise = models.ForeignKey(Enterprise, verbose_name='Empresa', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return self.mark


class WorkshopOrder(models.Model):
    entry_date = models.DateTimeField(verbose_name='Fecha de entrada', auto_now=True)
    vehicle = models.ForeignKey(Vehicle, verbose_name='Vehículo', on_delete=models.CASCADE, help_text='Vehículo')
    mechanical = models.ForeignKey(Mechanical, verbose_name='Mecánico responsable', related_name='mecanico_id',
                                   on_delete=models.CASCADE, help_text='Nombre del mecánico')
    enterprise = models.ForeignKey(Enterprise, verbose_name='Cliente o Empresa', on_delete=models.CASCADE,
                                   help_text='Nombre de la empresa')
    estimation = models.DecimalField(verbose_name='Presupuesto', max_digits=7, decimal_places=2,
                                     help_text='Presupuesto disponible')
    estimated_time = models.PositiveIntegerField(verbose_name='Tiempo estimado', help_text='Tiempo estimado en horas')
    mileage = models.PositiveIntegerField(verbose_name='kilometraje', help_text='kms recorrido por vehículo')
    assistant = models.ForeignKey(Mechanical, verbose_name='Ayudante', related_name='ayudante_id',
                                  on_delete=models.CASCADE)
    defection = models.TextField(verbose_name='Defectación', help_text='Problemas encontrados en el vehículo')
    work_done = models.TextField(verbose_name='Trabajo realizado', help_text='Descripción del trabajo realizado')
    delivery_date = models.DateField(verbose_name='Fecha de entrega al cliente', help_text='Fecha que será entregado')
    complaints_suggestions = models.TextField(verbose_name='Quejas o sugerencias',
                                              help_text='Quejas y sugerencias de los clientes')
    method_payment = models.ForeignKey(MethodPayment, verbose_name='Forma de pago', on_delete=models.CASCADE,
                                       help_text='Forma de pago')
    workforce_cost = models.DecimalField(verbose_name='Costo mano de obra', max_digits=7, decimal_places=2,
                                         help_text='Valor de la mano de obra')
    description_raw_materials_parts = models.TextField(verbose_name='Descripción Materias primas y piezas',
                                                       help_text='Nombre de las materias primas y piezas')
    amount = models.DecimalField(verbose_name='Importe en Piezas y Materias primas', max_digits=7, decimal_places=2,
                                 help_text='Importe')
    service_guarantee = models.ForeignKey(ServiceGuarantee, verbose_name='Garantía del servicio',
                                          on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'orden del taller'
        verbose_name_plural = 'Ordenes del taller'

    def __str__(self):
        return str(self.pk)


class PhysicalState(models.Model):
    workshop_order = models.ForeignKey(WorkshopOrder, verbose_name='Orden del taller', on_delete=models.CASCADE,
                                       help_text='Orden del taller')
    piece = models.ForeignKey(Piece, verbose_name='Pieza', on_delete=models.CASCADE, help_text='Pieza')
    description = models.TextField(verbose_name='Descripción',
                                   help_text='Como se encuentra el vehículo al entrar al taller')

    class Meta:
        verbose_name = 'estado físico'
        verbose_name_plural = 'Estados físicos'

    def __str__(self):
        return self.description


class Invoice(models.Model):
    type = models.ForeignKey(Type, verbose_name='Tipo', on_delete=models.CASCADE, help_text='Tipo de factura')
    contact = models.ForeignKey(Contact, verbose_name='Contacto', on_delete=models.CASCADE, help_text='Contacto')
    workshop_order = models.OneToOneField(WorkshopOrder, verbose_name='Orden del taller', on_delete=models.CASCADE,
                                          primary_key=True,
                                          help_text='Orden del taller correspondiente')
    services_provided = models.DecimalField(verbose_name='Servicios Prestados en el Taller', max_digits=7,
                                            decimal_places=2, help_text='Servicios Prestados en el Taller')
    expendable_material = models.DecimalField(verbose_name='Material Gastable', max_digits=7, decimal_places=2,
                                              help_text='Material Gastable')
    workforce = models.DecimalField(verbose_name='Mano de Obra', max_digits=7, decimal_places=2,
                                    help_text='Mano de Obra')
    date = models.DateTimeField(verbose_name='Fecha', help_text='Fecha de la factura', auto_now=True)

    class Meta:
        verbose_name = 'factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return str(self.pk)


class Provenance(models.Model):
    provenance = models.CharField(verbose_name='Procedencia', max_length=255, help_text='Procedencia')

    class Meta:
        verbose_name = 'procedencia'
        verbose_name_plural = 'Procedencias'

    def __str__(self):
        return self.provenance


class Activity(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name='Factura', on_delete=models.CASCADE,
                                help_text='Factura correspondiente')
    code = models.PositiveIntegerField(verbose_name='Código', unique=True, help_text='Código')
    description = models.CharField(verbose_name='Descripción', max_length=255, help_text='Descripción')
    unit_measurement = models.ForeignKey(UnitMeasurement, verbose_name='Unidad de medidas', on_delete=models.CASCADE,
                                         help_text='Unidad de medida')
    hours_worked = models.DecimalField(verbose_name='Horas trabajadas', max_digits=4, decimal_places=2,
                                       help_text='Cantidad de horas trabajadas')
    provenance = models.ForeignKey(Provenance, verbose_name='Procedencia', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Precio', max_digits=7, decimal_places=2, help_text='Precio')
    amount = models.PositiveIntegerField(verbose_name='Cantidad', help_text='Cantidad')

    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return str(self.code)
