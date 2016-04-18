# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from cStringIO import StringIO
from django.http import HttpResponse
import os


def genWord(vals):
    if os.name == 'posix':
        #Linux
        path = '/home/nati/Escritorio/intiSoft/Plantillas/'
    else:
        #Windows
        path = 'C:/xampp/htdocs/intiSoft/Plantillas/'

    document = Document(path + vals['plantilla'])

    # Documento temporal para la tabla de OTs
    tmp_doc = Document()
    ot_table = tmp_doc.add_table(0, 10)
    ot_table.alignment = 0

    # Estilo para formatear el texto de la tabla de OTs
    obj_styles_tmp = tmp_doc.styles
    obj_paragstyle_tmp = obj_styles_tmp.add_style('OT_TableStyle', WD_STYLE_TYPE.CHARACTER)
    obj_font_tmp = obj_paragstyle_tmp.font
    obj_font_tmp.size = Pt(10)
    obj_font_tmp.name = 'Calibri'

    obj_styles_doc = document.styles
    obj_paragstyle_doc = obj_styles_doc.add_style('OT_TableStyle', WD_STYLE_TYPE.CHARACTER)
    obj_font_doc = obj_paragstyle_doc.font
    obj_font_doc.size = Pt(10)
    obj_font_doc.name = 'Calibri'

    table = document.tables[0]
    table_xml = document._part._element.body[0]

    # Necesario para ajustar el ancho de las columnas
    #table.autofit = False
    ot_table.autofit = False

    #=======================================
    #======= DATOS DEL PRESUPUESTO =========
    #=======================================
    # Area
    table.column_cells(2)[0].paragraphs[0].runs[0].add_text(vals['area'] or '')
    # Presupuesto
    table.column_cells(3)[0].paragraphs[0].runs[0].add_text(vals['codigo'] or '')
    # Fecha
    table.column_cells(8)[0].paragraphs[0].runs[0].add_text(vals['fecha'] or '')
    # Solicitante
    table.column_cells(2)[2].paragraphs[0].runs[0].text = vals['solicitante'] or ''
    # Contacto
    table.column_cells(7)[2].paragraphs[0].runs[0].text = vals['contacto'] or ''
    # Email
    table.column_cells(2)[3].paragraphs[0].runs[0].text = vals['email'] or ''

    if vals['plantilla'] == 'Presupuesto Calibracion.docx':
        table.column_cells(0)[10].paragraphs[0].add_run(vals['fecha_inicio'], 'OT_TableStyle')
        table.column_cells(0)[10].paragraphs[3].add_run(vals['fecha_fin'], 'OT_TableStyle')
    if vals['plantilla'] == 'Presupuesto In Situ.docx':
        table.column_cells(0)[10].paragraphs[0].add_run(vals['fecha_inicio'], 'OT_TableStyle')
        table.column_cells(0)[10].paragraphs[2].add_run(vals['fecha_fin'], 'OT_TableStyle')
    if vals['plantilla'] == 'Presupuesto LIA.docx':
        table.column_cells(0)[10].paragraphs[0].add_run(vals['fecha_inicio'], 'OT_TableStyle')
        table.column_cells(0)[10].paragraphs[3].add_run(vals['fecha_fin'], 'OT_TableStyle')

    # OT's
    if vals['ofertatec']:
        cod, det, precio = vals['ofertatec'][0]
        table.column_cells(1)[7].paragraphs[0].add_run(det or '', 'OT_TableStyle')
        table.column_cells(1)[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        table.column_cells(5)[7].paragraphs[0].add_run(cod or '', 'OT_TableStyle')
        table.column_cells(9)[7].paragraphs[0].add_run(str(precio) or '', 'OT_TableStyle')

        for n, (cod, det, precio) in enumerate(vals['ofertatec'][1:]):
            # Creo y completo una fila en el documento temporal
            nrow = ot_table.add_row()
            # Ajusto el width
            nrow.cells[0].width = table.column_cells(0)[7].width
            nrow.cells[1].width = table.column_cells(1)[7].width
            nrow.cells[2].width = table.column_cells(2)[7].width
            nrow.cells[3].width = table.column_cells(3)[7].width
            nrow.cells[4].width = table.column_cells(4)[7].width
            nrow.cells[5].width = table.column_cells(5)[7].width
            nrow.cells[6].width = table.column_cells(6)[7].width
            nrow.cells[7].width = table.column_cells(7)[7].width
            nrow.cells[8].width = table.column_cells(8)[7].width
            nrow.cells[9].width = table.column_cells(9)[7].width
            # Mergeo las celdas
            nrow.cells[1].merge(nrow.cells[4])
            nrow.cells[5].merge(nrow.cells[8])
            # Completo las columnas
            nrow.cells[0].paragraphs[0].add_run(str(n + 2), 'OT_TableStyle')
            nrow.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            nrow.cells[1].paragraphs[0].add_run(det or '', 'OT_TableStyle')
            nrow.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
            nrow.cells[5].paragraphs[0].add_run(cod or '', 'OT_TableStyle')
            nrow.cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            nrow.cells[9].paragraphs[0].add_run(str(precio) or '', 'OT_TableStyle')
            nrow.cells[9].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Inserto la fila en el documento original
            table_xml.insert(n + 10, nrow._tr)

    f = StringIO()
    document.save(f)
    f.seek(0)

    response = HttpResponse(f.getvalue(), content_type='text/docx')
    response['Content-Disposition'] = "attachment; filename=%s.docx" % (vals['codigo'] or 'Presupuesto')

    #document.save(response)

    return response
