from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from app_resolucion.models import LicenciaUso, ResponsableObra, Zonificacion, SupervisorObra

class Command(BaseCommand):
    help = 'Inicializa datos base del sistema'

    def handle(self, *args, **kwargs):
        self.crear_grupos()
        self.crear_licencias()
        self.crear_responsables()
        self.crear_supervisores()
        self.crear_zonificaciones()

    def crear_grupos(self):
        for nombre in ['Obras', 'Fiscalización']:
            grupo, creado = Group.objects.get_or_create(name=nombre)
            mensaje = '✓ Grupo creado' if creado else '- Grupo ya existía'
            self.stdout.write(f'{mensaje}: {nombre}')

    def crear_licencias(self):
        licencias = [
            ('DEMOLICIÓN TOTAL - MODALIDAD "A"', 'VIVIENDA'),
            ('EDIFICACIÓN MODALIDAD "B"', 'VIVIENDA MULTIFAMILIAR'),
            ('EDIFICACIÓN MODALIDAD "A" - TECHO PROPIO', 'VIVIENDA'),
        ]
        for nombre, uso in licencias:
            obj, creado = LicenciaUso.objects.get_or_create(nombre_licencia=nombre, defaults={'uso_licencia': uso})
            self.stdout.write(f'{"✓" if creado else "-"} Licencia: {nombre}')

    def crear_responsables(self):
        responsables = [
            ("ING. RICHARD FRANKLIN LLONTOP PUICON", "CIP. 162464"),
            ("ARQ. MARIANELA PALACIOS MEDINA", "CAP. 5733"),
            ("ING. SANTOS CRISTOBAL CASTILLO FARROÑAN", "CIP. 27862"),
        ]
        for nombre, cip in responsables:
            obj, creado = ResponsableObra.objects.get_or_create(nombre=nombre, defaults={'cip_cap': cip})
            self.stdout.write(f'{"✓" if creado else "-"} Responsable: {nombre}')

    def crear_supervisores(self):
        supervisores = [
            ("ARQ. DEL CARPIO GABRIELLI CARLA SOFIA", "CAP. 13560"),
            ("ARQ. SALAZAR GARNIQUE JUAN ALEJANDRO", "CAP. 5596"),
            ("ARQ. REAÑO ALVITEZ JACQUELINE IVETTE", "CAP. 6582"),
            ("ARQ. HERRERA WESTTER SYLVIA CONSUELO", "CAP. 5409"),
            ("ARQ. BARTRA GROSSO FERNANDO", "CAP. 5634"),
            ("ARQ. WONG DIAZ JORGE JAMES", "CAP. 6580"),
            ("ARQ. ARRIBASPLATA PIZARRO HENRY ALBERTO", "CAP. 8448"),
            ("ARQ. ALVAREZ GARCIA VICTOR HUGO", "CAP. 6530"),
            ("ARQ. QUINTANA ACUÑA MARIA GUMERCINDA", "CAP. 6525"),
            ("ARQ. GARCIA ARRASCUE MARIETTA", "CAP. 7330"),
            ("ARQ. LARREA ALVARADO MAGALLY AGUSTINA", "CAP. 5471"),
            ("ARQ. CHALIQUE CASTRO WILDER ENRIQUE", "CAP. 3673"),
            ("ARQ. RUBIO SÁNCHEZ GRETTY", "CAP. 7162"),
            ("ARQ. MORALES LOPEZ JUAN GUILLERMO", "CAP. 6816"),
            ("ARQ. LEON JERI IRENE AMALIA", "CAP. 6019"),
            ("ARQ. VARGAS MACHUCA ACEVEDO JALMAR ISAAC", "CAP. 7275"),
            ("ARQ. REATEGUI OSORES EDGARDO", "CAP. 4599"),
            ("ARQ. OLORTE GARCIA LUIS HUMBERTO", "CAP. 5334"),
            ("ARQ. AITKEN GUTIERREZ JENIFFER HILDA", "CAP. 5581"),
            ("ARQ. NIZAMA VASQUEZ LUIS ENRIQUE", "CAP. 12948"),
            ("ARQ. IBAÑEZ BARCA CHRISTIAN ANTONIO", "CAP. 7382"),
            ("ARQ. DIAZ CASTILLO ILIAN ANGELICA", "CAP. 6785"),
            ("ARQ. GARBOZA SANCHEZ CARLOS ALBERTO", "CAP. 12922"),
            ("ARQ. LUNA VARGAS MILTON CESAR AUGUSTO", "CAP. 6102"),
            ("ARQ. PAIRAZAMAN ZULOETA OSWALDO MARTIN", "CAP. 9736"),
            ("ARQ. JIMENEZ NUÑEZ BENJAMIN", "CAP. 12227"),
            ("ARQ. FLORES TABOADA ERIKA LISSET ROSSYMERY DE AMERICA", "CAP. 26493"),
            ("ARQ. BARTUREN CARRASCO YULIANA CECILIA", "CAP. 19216"),
        ]
        for nombre, cip in supervisores:
            obj, creado = SupervisorObra.objects.get_or_create(nombre=nombre, defaults={'cip_cap': cip})
            self.stdout.write(f'{"✓" if creado else "-"} Supervisor: {nombre}')

    def crear_zonificaciones(self):
        zonificaciones = [
            ("ZPA", "ZONA DE PROTECCIÓN ARQUEOLÓGICA"),
            ("ZPE", "ZONA DE PROTECCIÓN ECOLÓGICA"),
            ("ZM", "ZONA MONUMENTAL"),
            ("ZA", "ZONA AGRÍCOLA"),
            ("I2", "INDUSTRIA LIVIANA"),
            ("OU", "USOS ESPECIALES"),
            ("ZRP", "RECREACIÓN"),
            ("H", "SALUD"),
            ("E", "EDUCACIÓN"),
            ("CE", "COMERCIO ESPECIALIZADO"),
            ("RDA", "ZONA RESIDENCIAL DENSIDAD ALTA"),
            ("RDB", "ZONA RESIDENCIAL DENSIDAD BAJA"),
            ("RDM", "ZONA RESIDENCIAL DENSIDAD MEDIA"),
        ]

        for codigo, descripcion in zonificaciones:
            obj, creado = Zonificacion.objects.get_or_create(
                zonificacion=codigo,
                defaults={
                    'descripcion': descripcion,
                    'departamento': 'Lambayeque',
                    'provincia': 'Lambayeque',
                    'distrito': 'Lambayeque'
                }
            )
            self.stdout.write(f'{"✓" if creado else "-"} Zonificación: {codigo}')
