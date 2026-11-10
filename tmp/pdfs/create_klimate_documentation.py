from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'output' / 'pdf' / 'klimate-documentacion-tecnica.pdf'

INK = colors.HexColor('#193127')
GREEN = colors.HexColor('#234C3B')
LIME = colors.HexColor('#D1E980')
MIST = colors.HexColor('#EEF0E8')
SURFACE = colors.HexColor('#FAFBF6')
LINE = colors.HexColor('#D7DCD2')
MUTED = colors.HexColor('#617069')
ORANGE = colors.HexColor('#E7A748')


def paragraph(text, style):
    return Paragraph(text, style)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Kicker',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=GREEN,
        spaceAfter=8,
        tracking=1.5,
    ))
    styles.add(ParagraphStyle(
        name='TitleLarge',
        parent=styles['Title'],
        fontName='Times-Bold',
        fontSize=39,
        leading=42,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=15,
    ))
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=19,
        textColor=MUTED,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name='H1K',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=25,
        leading=29,
        textColor=INK,
        spaceBefore=0,
        spaceAfter=11,
    ))
    styles.add(ParagraphStyle(
        name='H2K',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=INK,
        spaceBefore=10,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name='BodyK',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=INK,
        spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name='SmallK',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=MUTED,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='CardTitle',
        parent=styles['BodyText'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=INK,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name='CardBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=INK,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='Mono',
        parent=styles['BodyText'],
        fontName='Courier',
        fontSize=7.6,
        leading=10,
        textColor=GREEN,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9,
        textColor=MUTED,
        alignment=TA_CENTER,
    ))
    return styles


def card(title, body, styles, width):
    content = [
        paragraph(title, styles['CardTitle']),
        paragraph(body, styles['CardBody']),
    ]
    table = Table([[content]], colWidths=[width])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SURFACE),
        ('BOX', (0, 0), (-1, -1), 0.6, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 13),
        ('RIGHTPADDING', (0, 0), (-1, -1), 13),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    return table


def numbered_step(number, title, body, styles, width):
    number_cell = Table([[paragraph(number, ParagraphStyle(
        'StepNumber',
        parent=styles['CardTitle'],
        alignment=TA_CENTER,
        textColor=GREEN,
        fontSize=13,
        leading=15,
    ))]], colWidths=[9 * mm], rowHeights=[9 * mm])
    number_cell.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIME),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0, colors.white),
    ]))
    text = [paragraph(title, styles['CardTitle']), paragraph(body, styles['CardBody'])]
    step = Table([[number_cell, text]], colWidths=[13 * mm, width - 13 * mm])
    step.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SURFACE),
        ('BOX', (0, 0), (-1, -1), 0.6, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 8),
        ('RIGHTPADDING', (0, 0), (0, 0), 5),
        ('TOPPADDING', (0, 0), (0, 0), 10),
        ('BOTTOMPADDING', (0, 0), (0, 0), 10),
        ('LEFTPADDING', (1, 0), (1, 0), 6),
        ('RIGHTPADDING', (1, 0), (1, 0), 12),
        ('TOPPADDING', (1, 0), (1, 0), 10),
        ('BOTTOMPADDING', (1, 0), (1, 0), 10),
    ]))
    return step


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(document.leftMargin, 14 * mm, A4[0] - document.rightMargin, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(document.leftMargin, 9 * mm, 'KLIMATE - Documentación técnica del MVP')
    canvas.drawRightString(A4[0] - document.rightMargin, 9 * mm, f'Página {document.page}')
    canvas.restoreState()


def build_document():
    styles = build_styles()
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=21 * mm,
        title='Klimate - Documentación técnica del MVP',
        author='Klimate',
    )
    width = A4[0] - document.leftMargin - document.rightMargin
    story = []

    story.extend([
        Spacer(1, 21 * mm),
        paragraph('DOCUMENTACIÓN DEL MVP', styles['Kicker']),
        paragraph('Klimate', styles['TitleLarge']),
        paragraph('Mapa interactivo y consulta de condiciones meteorológicas por ubicación.', styles['Subtitle']),
        Spacer(1, 12 * mm),
    ])
    cover_card = Table([[
        [
            paragraph('Resultado actual', styles['CardTitle']),
            paragraph('El usuario puede seleccionar un punto en el mapa o usar la ubicación de su dispositivo. La aplicación consulta Open-Meteo y muestra las condiciones actuales en un panel simple.', styles['CardBody']),
        ],
        [
            paragraph('Tecnologías', styles['CardTitle']),
            paragraph('React, TypeScript, Vite, Leaflet, OpenStreetMap y Open-Meteo.', styles['CardBody']),
        ],
    ]], colWidths=[width * 0.60, width * 0.40])
    cover_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), MIST),
        ('BOX', (0, 0), (-1, -1), 0.6, LINE),
        ('INNERGRID', (0, 0), (-1, -1), 0.6, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.extend([
        cover_card,
        Spacer(1, 17 * mm),
        paragraph('Alcance del documento', styles['H2K']),
        paragraph('Describe el funcionamiento visible del prototipo, la separación técnica de responsabilidades, los patrones implementados y una propuesta de evolución para completar el catálogo de patrones del proyecto.', styles['BodyK']),
        Spacer(1, 49 * mm),
        paragraph('Versión MVP 1.0', styles['Kicker']),
        paragraph('Proyecto académico de clima y recomendaciones por actividad.', styles['SmallK']),
        PageBreak(),
    ])

    story.extend([
        paragraph('Cómo funciona', styles['H1K']),
        paragraph('El MVP trabaja con coordenadas. Todo el flujo se inicia con una ubicación y termina con datos normalizados, listos para que la interfaz los muestre.', styles['BodyK']),
        Spacer(1, 3 * mm),
    ])
    steps = [
        ('1', 'Seleccionar ubicación', 'El usuario hace clic en el mapa o pulsa “Usar mi ubicación”. Ambas acciones producen latitud y longitud.'),
        ('2', 'Actualizar el estado', 'useSelectedLocation guarda el punto elegido. React actualiza el marcador, el panel y activa la consulta.'),
        ('3', 'Consultar condiciones', 'useClimate usa ClimateFacade. La fachada delega la consulta al adaptador de Open-Meteo.'),
        ('4', 'Normalizar la respuesta', 'OpenMeteoAdapter convierte la respuesta externa en ClimateData: temperatura, sensación térmica, humedad, viento, precipitación y condición.'),
        ('5', 'Mostrar resultado', 'WeatherPanel representa el estado de carga, posibles errores y los datos actuales. Si cambia el punto, se cancela la solicitud anterior.'),
    ]
    for number, title, body in steps:
        story.append(numbered_step(number, title, body, styles, width))
        story.append(Spacer(1, 4 * mm))
    story.extend([
        Spacer(1, 3 * mm),
        paragraph('Arquitectura actual', styles['H2K']),
        paragraph('<b>domain</b> contiene modelos y contratos. <b>application</b> concentra las operaciones de negocio. <b>infrastructure</b> integra APIs externas. <b>presentation</b> contiene React, estado y componentes.', styles['BodyK']),
        Table([
            [paragraph('Capa', styles['SmallK']), paragraph('Responsabilidad', styles['SmallK']), paragraph('Ejemplos', styles['SmallK'])],
            [paragraph('Domain', styles['CardBody']), paragraph('Contratos y modelos independientes.', styles['CardBody']), paragraph('Location, ClimateData, ClimateProvider.', styles['Mono'])],
            [paragraph('Application', styles['CardBody']), paragraph('Orquesta casos de uso.', styles['CardBody']), paragraph('ClimateFacade, LocateUserCommand.', styles['Mono'])],
            [paragraph('Infrastructure', styles['CardBody']), paragraph('Conecta proveedores reales.', styles['CardBody']), paragraph('OpenMeteoAdapter, BrowserLocationProvider.', styles['Mono'])],
            [paragraph('Presentation', styles['CardBody']), paragraph('Muestra e interactúa con el usuario.', styles['CardBody']), paragraph('MapExplorer, WeatherPanel, hooks.', styles['Mono'])],
        ], colWidths=[27 * mm, 65 * mm, width - 92 * mm], style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), MIST),
            ('BOX', (0, 0), (-1, -1), 0.6, LINE),
            ('INNERGRID', (0, 0), (-1, -1), 0.4, LINE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ])),
        PageBreak(),
    ])

    story.extend([
        paragraph('Patrones implementados', styles['H1K']),
        paragraph('Los patrones existentes separan los detalles de React y de los proveedores externos. No se añadieron solo para cumplir una lista: cada uno resuelve una dependencia concreta del MVP.', styles['BodyK']),
        Spacer(1, 3 * mm),
    ])
    pattern_cards = [
        ('Observer', '<b>Qué resuelve:</b> sincronizar la interfaz con la ubicación seleccionada.<br/><br/><b>Implementación:</b> useSelectedLocation conserva el estado. MapExplorer publica el punto y App, useClimate, WeatherPanel y el marcador reaccionan a ese cambio.<br/><br/><b>Archivos:</b><br/><font name="Courier">presentation/hooks/useSelectedLocation.ts</font>'),
        ('Adapter', '<b>Qué resuelve:</b> evitar que la aplicación dependa del formato de Open-Meteo.<br/><br/><b>Implementación:</b> OpenMeteoAdapter pide los campos actuales y los traduce al modelo ClimateData. Además convierte los códigos WMO en descripciones legibles.<br/><br/><b>Archivos:</b><br/><font name="Courier">infrastructure/open-meteo/OpenMeteoAdapter.ts</font>'),
        ('Facade', '<b>Qué resuelve:</b> exponer una única operación para pedir clima.<br/><br/><b>Implementación:</b> ClimateFacade recibe un ClimateProvider y ofrece getCurrentClimate. La interfaz no conoce el proveedor de clima ni los parámetros HTTP.<br/><br/><b>Archivos:</b><br/><font name="Courier">application/services/ClimateFacade.ts</font>'),
        ('Command', '<b>Qué resuelve:</b> encapsular una acción de usuario que puede variar por plataforma.<br/><br/><b>Implementación:</b> LocateUserCommand solicita una ubicación mediante un contrato. BrowserLocationProvider adapta navigator.geolocation y devuelve Location.<br/><br/><b>Archivos:</b><br/><font name="Courier">application/commands/LocateUserCommand.ts</font>'),
    ]
    for index in range(0, len(pattern_cards), 2):
        row = []
        for title, body in pattern_cards[index:index + 2]:
            row.append(card(title, body, styles, (width - 5 * mm) / 2))
        story.append(Table([row], colWidths=[(width - 5 * mm) / 2, (width - 5 * mm) / 2], style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('COLSPACE', (0, 0), (-1, -1), 5 * mm),
        ])))
        story.append(Spacer(1, 5 * mm))
    story.extend([
        Spacer(1, 3 * mm),
        paragraph('Comportamientos de calidad ya presentes', styles['H2K']),
        paragraph('Las solicitudes de clima usan AbortController para cancelar una consulta anterior cuando el usuario elige otro punto. La ubicación del navegador tiene estados de carga y mensajes para permiso denegado, ubicación no disponible o tiempo agotado.', styles['BodyK']),
        PageBreak(),
    ])

    story.extend([
        Spacer(1, 8 * mm),
        paragraph('Patrones por implementar', styles['H1K']),
        paragraph('La siguiente lista permite crecer hacia el requisito de diez patrones sin crear abstracciones artificiales. Cada patrón se propone para una capacidad real del producto.', styles['BodyK']),
        Spacer(1, 3 * mm),
    ])
    roadmap_rows = [
        ['Patrón', 'Cuándo aplicarlo', 'Posible implementación'],
        ['Strategy', 'Cuando existan recomendaciones por actividad.', 'Una estrategia por actividad: correr, ciclismo, picnic o caminata. Cada una interpreta clima y contaminación con sus propios umbrales.'],
        ['Factory Method', 'Al añadir más fuentes de datos.', 'Una fábrica crea ClimateProvider o AirQualityProvider según configuración: Open-Meteo, proveedor alterno o datos simulados para pruebas.'],
        ['Repository', 'Al incorporar caché e historial.', 'ClimateRepository centraliza consultas, expiración de datos y almacenamiento local por coordenadas, sin exponer detalles a la interfaz.'],
        ['Decorator', 'Al enriquecer una recomendación.', 'Decoradores agregan alertas por lluvia, calor, UV o contaminación a una recomendación base sin modificar la regla original.'],
        ['Builder', 'Al crear un reporte compartible.', 'RecommendationReportBuilder arma un resumen con punto, actividad, clima, aire, alertas y sugerencias opcionales.'],
        ['Singleton', 'Al configurar recursos compartidos.', 'Una sola instancia de caché, configuración de proveedores o cliente HTTP. Debe usarse solo si se necesita estado global controlado.'],
    ]
    table_rows = []
    for row_index, row in enumerate(roadmap_rows):
        style = styles['SmallK'] if row_index == 0 else styles['CardBody']
        table_rows.append([paragraph(value, style) for value in row])
    roadmap = Table(table_rows, colWidths=[27 * mm, 53 * mm, width - 80 * mm], repeatRows=1)
    roadmap.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.6, LINE),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), SURFACE),
    ]))
    story.extend([
        roadmap,
        Spacer(1, 10 * mm),
        KeepTogether([
            card('Criterio para añadir un patrón', 'Cada patrón debe responder a un cambio previsto, una variación de comportamiento o una responsabilidad que necesite aislamiento. Si no reduce acoplamiento ni mejora pruebas o extensibilidad, es mejor no añadirlo.', styles, width),
            Spacer(1, 8 * mm),
            paragraph('Próximo incremento recomendado', styles['H2K']),
            paragraph('Añadir calidad del aire desde Open-Meteo y un Strategy por actividad. Esa evolución activa una necesidad concreta de reglas intercambiables y abre el camino a Decorator para las alertas.', styles['BodyK']),
        ]),
    ])

    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == '__main__':
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    build_document()
