from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from resoluciones.models import LicenciaUso, Zonificacion, ResponsableObra


class Command(BaseCommand):
    help = 'Configura el sistema creando grupos de usuarios y datos de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Configurando el sistema...'))
        
        # Crear grupos de usuarios
        self.create_groups()
        
        # Crear datos de ejemplo
        self.create_sample_data()
        
        self.stdout.write(self.style.SUCCESS('Sistema configurado exitosamente!'))

    def create_groups(self):
        """Crea los grupos de usuarios Obras y Fiscalización"""
        self.stdout.write('Creando grupos de usuarios...')
        
        obras_group, created = Group.objects.get_or_create(name='Obras')
        if created:
            self.stdout.write(f'  ✓ Grupo "Obras" creado')
        else:
            self.stdout.write(f'  - Grupo "Obras" ya existe')
            
        fiscalizacion_group, created = Group.objects.get_or_create(name='Fiscalización')
        if created:
            self.stdout.write(f'  ✓ Grupo "Fiscalización" creado')
        else:
            self.stdout.write(f'  - Grupo "Fiscalización" ya existe')

    def create_sample_data(self):
        """Crea datos de ejemplo para licencias, zonificaciones y responsables"""
        self.stdout.write('Creando datos de ejemplo...')
        
        # Crear licencias de uso
        licencias = [
            ('Licencia de Construcción Común', 'Uso residencial'),
            ('Licencia de Construcción Especial', 'Uso comercial'),
            ('Licencia de Construcción de Densidad Media', 'Uso mixto'),
            ('Licencia de Construcción Multifamiliar', 'Uso residencial múltiple'),
            ('Licencia de Remodelación', 'Modificación de estructura'),
        ]
        
        for nombre, uso in licencias:
            licencia, created = LicenciaUso.objects.get_or_create(
                nombre_licencia=nombre,
                defaults={'uso_licencia': uso}
            )
            if created:
                self.stdout.write(f'  ✓ Licencia "{nombre}" creada')

        # Crear zonificaciones
        zonificaciones = [
            ('RDM', 'Lima', 'Lima', 'Miraflores'),
            ('RDB', 'Lima', 'Lima', 'San Isidro'),
            ('CZ', 'Lima', 'Lima', 'Lima'),
            ('I1', 'Lima', 'Lima', 'San Luis'),
            ('RDM', 'Lima', 'Lima', 'Surco'),
            ('CV', 'Callao', 'Callao', 'Callao'),
        ]
        
        for zona, depto, prov, dist in zonificaciones:
            zonificacion, created = Zonificacion.objects.get_or_create(
                zonificacion=zona,
                departamento=depto,
                provincia=prov,
                distrito=dist
            )
            if created:
                self.stdout.write(f'  ✓ Zonificación "{zona} - {dist}" creada')

        # Crear responsables de obra
        responsables = [
            ('Ing. Juan Carlos Pérez García', 'CIP 12345'),
            ('Arq. María Elena Rodríguez López', 'CAP 67890'),
            ('Ing. Carlos Alberto Mendoza Silva', 'CIP 23456'),
            ('Arq. Ana Sofía Vásquez Torres', 'CAP 78901'),
            ('Ing. Roberto Miguel Fernández Cruz', 'CIP 34567'),
        ]
        
        for nombre, cip in responsables:
            responsable, created = ResponsableObra.objects.get_or_create(
                nombre=nombre,
                defaults={'cip_cap': cip}
            )
            if created:
                self.stdout.write(f'  ✓ Responsable "{nombre}" creado')

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados exitosamente!'))
        
        # Instrucciones adicionales
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.WARNING('INSTRUCCIONES ADICIONALES:'))
        self.stdout.write('1. Crear un superusuario: python manage.py createsuperuser')
        self.stdout.write('2. Acceder al admin: http://localhost:8000/admin/')
        self.stdout.write('3. Asignar usuarios a grupos desde el admin')
        self.stdout.write('4. El sistema está listo para usar!')
        self.stdout.write('='*60) 