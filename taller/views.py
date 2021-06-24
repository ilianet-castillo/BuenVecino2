import io
import os

from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer

from .models import WorkshopOrder, PhysicalState, Invoice, Activity


def export_workshop_order_pdf(request, object_id):
    workshop_order = WorkshopOrder.objects.filter(pk=object_id).first()
    physicals_state = PhysicalState.objects.filter(workshop_order=workshop_order)

    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'CalibriB.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Workshop_Order_Title',
                              fontName='Calibri-Bold',
                              fontSize=20,
                              leading=24,
                              alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal',
                              fontName='Calibri'))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_12',
                              parent=styles['Workshop_Order_Normal'],
                              fontSize=12,
                              leading=14.4))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_12_Right',
                              parent=styles['Workshop_Order_Normal_12'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_Bold_12',
                              parent=styles['Workshop_Order_Normal_12'],
                              fontName='Calibri-Bold'))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_Bold_12_Right',
                              parent=styles['Workshop_Order_Normal_Bold_12'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_12_Justify',
                              parent=styles['Workshop_Order_Normal_12'],
                              alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_Bold_12_Center',
                              parent=styles['Workshop_Order_Normal_Bold_12'],
                              alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_14',
                              parent=styles['Workshop_Order_Normal'],
                              fontSize=14,
                              leading=16.8))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_14_Right',
                              parent=styles['Workshop_Order_Normal_14'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_Bold_14',
                              parent=styles['Workshop_Order_Normal_14'],
                              fontName='Calibri-Bold'))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_Bold_14_Right',
                              parent=styles['Workshop_Order_Normal_Bold_14'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_14_Justify',
                              parent=styles['Workshop_Order_Normal_14'],
                              alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_14_Center',
                              parent=styles['Workshop_Order_Normal_14'],
                              alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_16',
                              parent=styles['Workshop_Order_Normal'],
                              fontSize=16,
                              leading=19.2))
    styles.add(ParagraphStyle(name='Workshop_Order_Normal_16_Justify',
                              parent=styles['Workshop_Order_Normal_16'],
                              alignment=TA_JUSTIFY))

    doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            topMargin=3.55 * cm,
                            bottomMargin=3.18 * cm,
                            leftMargin=1.27 * cm,
                            rightMargin=1.27 * cm,
                            title='Orden de taller',
                            author='Taller Buen Vecino')

    body = list()

    rows = list()
    rows.append([Paragraph('ORDEN DE TRABAJO', styles['Workshop_Order_Title'])])
    rows.append([Paragraph('No. Orden:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph(str(workshop_order), styles['Workshop_Order_Normal_14']),
                 Paragraph('Nombre Cliente o Empresa:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph(workshop_order.enterprise.name, styles['Workshop_Order_Normal_14'])])
    rows.append([Paragraph('Fecha de entrada:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph(workshop_order.entry_date.strftime('%d/%m/%Y'), styles['Workshop_Order_Normal_14']),
                 Paragraph('Presupuesto:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('$ {:,.2f}'.format(workshop_order.estimation), styles['Workshop_Order_Normal_14_Right'])])
    rows.append([Paragraph('Marca y Modelo:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('{} / {}'.format(workshop_order.vehicle.mark, workshop_order.vehicle.model),
                           styles['Workshop_Order_Normal_14']),
                 Paragraph('Tiempo estimado:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('{:.2f} hs'.format(workshop_order.estimated_time),
                           styles['Workshop_Order_Normal_14_Right'])])
    rows.append([Paragraph('Chapa:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph(workshop_order.vehicle.tag, styles['Workshop_Order_Normal_14']),
                 Paragraph('Kilometraje:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('{} km'.format(workshop_order.mileage), styles['Workshop_Order_Normal_14_Right'])])
    rows.append([Paragraph('Mecánico Responsable:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('{} {}'.format(workshop_order.mechanical.name, workshop_order.mechanical.last_name),
                           styles['Workshop_Order_Normal_14']),
                 Paragraph('Ayudante:', styles['Workshop_Order_Normal_Bold_14_Right']),
                 Paragraph('{} {}'.format(workshop_order.assistant.name, workshop_order.assistant.last_name),
                           styles['Workshop_Order_Normal_14'])])
    rows.append([[Paragraph('Defectación:', styles['Workshop_Order_Normal_Bold_14']),
                  Paragraph(workshop_order.defection, styles['Workshop_Order_Normal_14_Justify'])]])
    rows.append([[Paragraph('Trabajo realizado:', styles['Workshop_Order_Normal_Bold_14']),
                  Paragraph(workshop_order.work_done, styles['Workshop_Order_Normal_14_Justify'])]])
    rows.append(
        [Paragraph('Estado físico del vehículo al entrar al taller', styles['Workshop_Order_Normal_14_Center'])])
    for physical_state in physicals_state:
        rows.append([Paragraph(physical_state.piece.name, styles['Workshop_Order_Normal_14_Justify']),
                     Paragraph(physical_state.description, styles['Workshop_Order_Normal_14_Justify'])])
    rows.append([Paragraph('Fecha de entrega al cliente:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph(workshop_order.delivery_date.strftime('%d/%m/%Y'), styles['Workshop_Order_Normal_12']),
                 Paragraph('Forma de pago:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph(workshop_order.method_payment.type, styles['Workshop_Order_Normal_12'])])
    rows.append([Paragraph('Nombre del cliente:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph(workshop_order.enterprise.name, styles['Workshop_Order_Normal_12']),
                 Paragraph('Costo mano de obra:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph('$ {:,.2f}'.format(workshop_order.workforce_cost),
                           styles['Workshop_Order_Normal_12_Right'])])
    rows.append(
        [[Paragraph('Quejas o sugerencias:', styles['Workshop_Order_Normal_Bold_12']),
          Paragraph(workshop_order.complaints_suggestions, styles['Workshop_Order_Normal_12_Justify'])], '',
         [Paragraph('Descripción Materias primas y piezas:', styles['Workshop_Order_Normal_Bold_12']),
          Paragraph(workshop_order.description_raw_materials_parts, styles['Workshop_Order_Normal_12_Justify'])]])
    rows.append([Paragraph('Firma Cliente:', styles['Workshop_Order_Normal_Bold_12_Center']), '',
                 Paragraph('Importe en Piezas y Materias primas:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph('$ {:,.2f}'.format(workshop_order.amount), styles['Workshop_Order_Normal_12_Right'])])
    rows.append(['', '', Paragraph('Total a pagar:', styles['Workshop_Order_Normal_Bold_12_Right']),
                 Paragraph('$ {:,.2f}'.format(workshop_order.workforce_cost + workshop_order.amount),
                           styles['Workshop_Order_Normal_12_Right'])])
    rows.append([Paragraph('Garantia del Servicio:', styles['Workshop_Order_Normal_16']),
                 Paragraph(workshop_order.service_guarantee.description, styles['Workshop_Order_Normal_16_Justify'])])

    col_widths = [
        doc.width * 0.28,
        doc.width * 0.25,
        doc.width * 0.22,
        doc.width * 0.25
    ]

    style = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 6), (-1, 6)),
        ('SPAN', (0, 7), (-1, 7)),
        ('SPAN', (0, 8), (-1, 8)),
        ('SPAN', (1, 9), (-1, -7)),
        ('SPAN', (0, -4), (1, -4)),
        ('SPAN', (2, -4), (3, -4)),
        ('SPAN', (0, -3), (0, -2)),
        ('VALIGN', (0, -3), (0, -2), 'MIDDLE'),
        ('SPAN', (1, -3), (1, -2)),
        ('SPAN', (1, -1), (-1, -1))
    ])

    table = Table(rows, colWidths=col_widths, style=style)
    body.append(table)

    doc.build(body, canvasmaker=HeaderFooter)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Orden de trabajo.pdf')


def export_invoice_pdf(request, object_id):
    invoice = Invoice.objects.filter(pk=object_id).first()
    activities = Activity.objects.filter(invoice=invoice)

    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'CalibriB.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Invoice_Normal',
                              fontName='Calibri',
                              fontSize=11,
                              leading=13.2))
    styles.add(ParagraphStyle(name='Invoice_Normal_Center',
                              parent=styles['Invoice_Normal'],
                              alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Invoice_Normal_Right',
                              parent=styles['Invoice_Normal'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Invoice_Normal_Bold',
                              parent=styles['Invoice_Normal'],
                              fontName='Calibri-Bold'))
    styles.add(ParagraphStyle(name='Invoice_Normal_Bold_Right',
                              parent=styles['Invoice_Normal_Bold'],
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Invoice_Normal_Bold_Center',
                              parent=styles['Invoice_Normal_Bold'],
                              alignment=TA_CENTER))

    doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            topMargin=3.55 * cm,
                            bottomMargin=3.18 * cm,
                            leftMargin=1.27 * cm,
                            rightMargin=1.27 * cm,
                            title='Factura',
                            author='Taller Buen Vecino')

    body = list()

    rows = list()
    rows.append([Paragraph(invoice.type.title, styles['Invoice_Normal_Bold_Center'])])
    rows.append([Paragraph('Nombre:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.contact.name, styles['Invoice_Normal']),
                 Paragraph('TCP:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.contact.tcp, styles['Invoice_Normal'])])
    rows.append([Paragraph('Dirección:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.contact.address, styles['Invoice_Normal']),
                 Paragraph('Nit:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.contact.nit), styles['Invoice_Normal'])])
    rows.append([Paragraph('Email:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.contact.email, styles['Invoice_Normal']),
                 Paragraph('No.cuenta CUP:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.contact.no_check_cup), styles['Invoice_Normal'])])
    rows.append([Paragraph('Teléfono:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.contact.phone), styles['Invoice_Normal'])])

    col_widths = [
        doc.width * 0.11,
        doc.width * 0.39,
        doc.width * 0.16,
        doc.width * 0.34
    ]

    style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (-1, 0))
    ])

    table = Table(rows, colWidths=col_widths, style=style)
    body.append(table)
    body.append(Spacer(1, 11))

    rows = list()
    rows.append([Paragraph('Datos del Cliente', styles['Invoice_Normal_Bold_Center']), '',
                 Paragraph('Del Servicio', styles['Invoice_Normal_Bold_Center']), ''])
    rows.append([Paragraph('Nombre:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.workshop_order.enterprise.name, styles['Invoice_Normal']),
                 Paragraph('No. Factura:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.pk), styles['Invoice_Normal_Center'])])
    rows.append([Paragraph('Domicilio:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.workshop_order.enterprise.address, styles['Invoice_Normal']),
                 Paragraph('Referencia OT No:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.workshop_order.pk), styles['Invoice_Normal_Center'])])
    rows.append([Paragraph('Teléfono:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(str(invoice.workshop_order.enterprise.phone), styles['Invoice_Normal']),
                 Paragraph('No. Factura OT No:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('{} - {}'.format(invoice, invoice.workshop_order), styles['Invoice_Normal_Center'])])
    rows.append([Paragraph('Vehículo', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('{} / {}'.format(invoice.workshop_order.vehicle.mark, invoice.workshop_order.vehicle.model),
                           styles['Invoice_Normal']), Paragraph('Fecha:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.date.strftime('%d/%m/%Y'), styles['Invoice_Normal_Center'])])
    rows.append([Paragraph('Chapa:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph(invoice.workshop_order.vehicle.tag, styles['Invoice_Normal']),
                 Paragraph('Moneda:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('CUP', styles['Invoice_Normal_Center'])])

    col_widths = [
        doc.width * 0.11,
        doc.width * 0.39,
        doc.width * 0.19,
        doc.width * 0.31
    ]

    style = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (2, 0), (3, 0))
    ])

    table = Table(rows, colWidths=col_widths, style=style)
    body.append(table)
    body.append(Spacer(1, 11))
    body.append(Spacer(1, 11))

    rows = list()
    rows.append([Paragraph('No.', styles['Invoice_Normal_Bold']), Paragraph('Código', styles['Invoice_Normal_Bold']),
                 Paragraph('Descripción', styles['Invoice_Normal_Bold']),
                 Paragraph('u/m', styles['Invoice_Normal_Bold']),
                 Paragraph('Horas Trabajo', styles['Invoice_Normal_Bold']),
                 Paragraph('Proc.', styles['Invoice_Normal_Bold']), Paragraph('Precio', styles['Invoice_Normal_Bold']),
                 Paragraph('Cant.', styles['Invoice_Normal_Bold']),
                 Paragraph('Importe', styles['Invoice_Normal_Bold'])])
    pos = 1
    total = invoice.services_provided + invoice.expendable_material + invoice.workforce
    for activity in activities:
        rows.append(
            [Paragraph(str(pos), styles['Invoice_Normal_Right']),
             Paragraph(str(activity.code), styles['Invoice_Normal']),
             Paragraph(activity.description, styles['Invoice_Normal']),
             Paragraph(activity.unit_measurement.name, styles['Invoice_Normal']),
             Paragraph(str(activity.hours_worked), styles['Invoice_Normal_Right']),
             Paragraph(activity.provenance.provenance, styles['Invoice_Normal']),
             Paragraph('$ {:,.2f}'.format(activity.price), styles['Invoice_Normal_Right']),
             Paragraph(str(activity.amount), styles['Invoice_Normal_Right']),
             Paragraph('$ {:,.2f}'.format(activity.price * activity.amount), styles['Invoice_Normal_Right'])])
        pos += 1
        total += (activity.price * activity.amount)
    rows.append(['', '', '', '', '', '', '', '', ''])
    rows.append(['', '', '', '', '', '', '', '', ''])
    rows.append(['', Paragraph('Servicios Prestados en el Taller', styles['Invoice_Normal']), '', '', '', '', '', '',
                 Paragraph('$ {:,.2f}'.format(invoice.services_provided), styles['Invoice_Normal_Right'])])
    rows.append(['', Paragraph('Material Gastable', styles['Invoice_Normal']), '', '', '', '', '', '',
                 Paragraph('$ {:,.2f}'.format(invoice.expendable_material), styles['Invoice_Normal_Right'])])
    rows.append(['', Paragraph('Mano de Obra', styles['Invoice_Normal']), '', '', '', '', '', '',
                 Paragraph('$ {:,.2f}'.format(invoice.workforce), styles['Invoice_Normal_Right'])])
    rows.append(['', Paragraph('Total', styles['Invoice_Normal']), '', '', '', '', '', '',
                 Paragraph('$ {:,.2f}'.format(total), styles['Invoice_Normal_Right'])])

    col_widths = [
        doc.width * 0.06,
        doc.width * 0.13,
        doc.width * 0.26,
        doc.width * 0.06,
        doc.width * 0.09,
        doc.width * 0.08,
        doc.width * 0.12,
        doc.width * 0.07,
        doc.width * 0.13
    ]

    style = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (1, -6), (-1, -6)),
        ('SPAN', (1, -5), (-1, -5)),
        ('SPAN', (1, -4), (-2, -4)),
        ('SPAN', (1, -3), (-2, -3)),
        ('SPAN', (1, -2), (-2, -2)),
        ('SPAN', (1, -1), (-2, -1))
    ])

    table = Table(rows, colWidths=col_widths, style=style)
    body.append(table)
    body.append(Spacer(1, 11))
    body.append(Spacer(1, 11))
    body.append(Spacer(1, 11))
    body.append(Spacer(1, 11))

    rows = list()
    rows.append([Paragraph('Facturado por:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('Evelio Mojena Álvarez', styles['Invoice_Normal']),
                 Paragraph('Recibido por:', styles['Invoice_Normal_Bold_Right']), ''])
    rows.append([Paragraph('Cargo:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('Jefe de Taller', styles['Invoice_Normal']), '', ''])
    rows.append([Paragraph('Fecha:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('____/ ____/ 2021', styles['Invoice_Normal']),
                 Paragraph('Fecha:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('____/ ____/ 2021', styles['Invoice_Normal'])])
    rows.append([Paragraph('Firma:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('_____________________', styles['Invoice_Normal']),
                 Paragraph('Firma:', styles['Invoice_Normal_Bold_Right']),
                 Paragraph('_____________________', styles['Invoice_Normal'])])

    col_widths = [
        doc.width * 0.15,
        doc.width * 0.35,
        doc.width * 0.15,
        doc.width * 0.35
    ]

    table = Table(rows, colWidths=col_widths)
    body.append(table)

    doc.build(body, canvasmaker=HeaderFooter)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Orden de trabajo.pdf')


class HeaderFooter(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = list()

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer()
            self.Canvas.showPage(self)
        self.Canvas.save(self)

    def draw_header_footer(self):
        w, h = letter

        self.saveState()
        base_dir = os.path.dirname(__file__) + '/img/{}'

        # Header
        header = Image(base_dir.format('header.png'))
        header.drawHeight = 3.55 * cm
        header.drawWidth = w

        header.wrap(w, 3.55 * cm)
        header.drawOn(self, 0, h - 3.55 * cm)

        # Footer
        footer = Image(base_dir.format('footer.png'))
        footer.drawHeight = 3.18 * cm
        footer.drawWidth = w

        footer.wrap(w, 3.18 * cm)
        footer.drawOn(self, 0, 0 * cm)

        self.restoreState()
