# pdf.py
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    Image
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak
from reportlab.platypus import Frame
from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.lib.utils import ImageReader
from datetime import datetime

def generar_pdf(cliente, cuentas, mensual, grafica_buffer):

    doc = SimpleDocTemplate(
        "perfil_laft.pdf",
        pagesize=A4
    )

    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph(
        "PERFIL DE CLIENTE — REPORTE LA/FT",
        styles["Title"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # Metadata
    elements.append(Paragraph(
        f"Fecha generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"DPI: {cliente['identificacion']}",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"ClienteId: {cliente['ClienteId']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.5 * inch))

    # Sección A - Identificación
    elements.append(Paragraph("A) Identificación", styles["Heading2"]))
    elements.append(Paragraph(f"Nombre: {cliente['nombre_completo']}", styles["Normal"]))
    elements.append(Paragraph(f"NIT: {cliente['nit']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Sección B - KYC
    elements.append(Paragraph("B) Información KYC", styles["Heading2"]))
    elements.append(Paragraph(f"Actividad económica: {cliente['actividad_economica']}", styles["Normal"]))
    elements.append(Paragraph(f"Ingresos reportados: {cliente['ingresos_reportados']}", styles["Normal"]))
    elements.append(Paragraph(f"PEP: {cliente['es_cliente_pep']}", styles["Normal"]))
    elements.append(Paragraph(f"CPE: {cliente['es_cliente_cpe']}", styles["Normal"]))
    elements.append(Paragraph(f"RIC: {cliente['ric']}", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    # Sección C - Cuentas
    elements.append(Paragraph("C) Productos / Cuentas", styles["Heading2"]))

    if not cuentas.empty:
        data = [["Cuenta", "Producto", "Moneda", "Estado"]]

        for _, row in cuentas.iterrows():
            data.append([
                row["CuentaId"],
                row["ProductoPasivo"],
                row["MonedaCuenta"],
                row["EstadoCuenta"]
            ])

        table = Table(data, repeatRows=1)
        table.setStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ])

        elements.append(table)
    else:
        elements.append(Paragraph("Sin productos pasivos.", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # Sección D - Resumen Transaccional
    elements.append(Paragraph("D) Resumen Transaccional", styles["Heading2"]))

    if not mensual.empty:
        total_creditos = mensual["MontoCreditos"].sum()
        total_debitos = mensual["MontoDebitos"].sum()

        elements.append(Paragraph(f"Total Créditos: {total_creditos:,.2f}", styles["Normal"]))
        elements.append(Paragraph(f"Total Débitos: {total_debitos:,.2f}", styles["Normal"]))
    else:
        elements.append(Paragraph("Sin movimientos en el periodo.", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # Sección E - Gráfica
    elements.append(Paragraph("E) Créditos vs Débitos", styles["Heading2"]))

    if grafica_buffer:
        img = Image(grafica_buffer, width=6*inch, height=3*inch)
        elements.append(img)
    else:
        elements.append(Paragraph("No hay datos para graficar.", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # Disclaimer
    elements.append(Paragraph(
        "Documento generado automáticamente para fines de investigación interna LA/FT.",
        styles["Normal"]
    ))

    doc.build(elements)
