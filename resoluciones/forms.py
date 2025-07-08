from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resolucion, DetalleResolucion, ResponsableObra, Zonificacion, LicenciaUso, SupervisorObra


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        fields = [
            'num_resolucion', 'num_expediente', 'num_recibo', 'fecha_emision', 
            'fecha_vencimiento', 'administrado', 'propietario', 'nombre_licencia', 
            'direccion', 'calle'
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control flatpickr'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control flatpickr'}),
            'num_resolucion': forms.TextInput(attrs={'class': 'form-control'}),
            'num_expediente': forms.TextInput(attrs={'class': 'form-control'}),
            'num_recibo': forms.TextInput(attrs={'class': 'form-control'}),
            'administrado': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'propietario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nombre_licencia': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean_fecha_vencimiento(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento <= fecha_emision:
                raise forms.ValidationError("La fecha de vencimiento debe ser posterior a la fecha de emisión.")
        
        return fecha_vencimiento


class DetalleResolucionForm(forms.ModelForm):
    # Campos adicionales para nuevo responsable
    nuevo_responsable = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="O registrar nuevo responsable"
    )
    nuevo_cip_cap = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="CIP/CAP del nuevo responsable"
    )

    # Campos adicionales para nuevo supervisor
    nuevo_supervisor = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="O registrar nuevo supervisor"
    )
    nuevo_supervisor_cip_cap = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="CIP/CAP del nuevo supervisor"
    )

    class Meta:
        model = DetalleResolucion
        fields = [
            'zonificacion', 'areatechada_total', 'detalle_areatechada', 
            'num_pisos', 'altura', 'num_sotano', 'semisotano', 'azotea','responsable_obra', 'supervisor_obra'
        ]
        widgets = {
            'zonificacion': forms.Select(attrs={'class': 'form-select'}),
            'areatechada_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'detalle_areatechada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_pisos': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'num_sotano': forms.NumberInput(attrs={'class': 'form-control'}),
            'semisotano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'azotea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'responsable_obra': forms.Select(attrs={'class': 'form-select'}),
            'supervisor_obra': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable_obra'].required = False
        self.fields['supervisor_obra'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        responsable_obra = cleaned_data.get('responsable_obra')
        nuevo_responsable = cleaned_data.get('nuevo_responsable')
        nuevo_cip_cap = cleaned_data.get('nuevo_cip_cap')

        supervisor_obra = cleaned_data.get('supervisor_obra')
        nuevo_supervisor = cleaned_data.get('nuevo_supervisor')
        nuevo_supervisor_cip_cap = cleaned_data.get('nuevo_supervisor_cip_cap')


        # Validar RESPONSABLE de obra
        if not responsable_obra and not nuevo_responsable:
            self.add_error('responsable_obra', "Debe seleccionar un responsable existente o registrar uno nuevo.")

        # Si se está registrando nuevo responsable, ambos campos son requeridos
        if nuevo_responsable and not nuevo_cip_cap:
            self.add_error('nuevo_cip_cap', "Si registra un nuevo responsable, debe completar también el CIP/CAP.")

        if nuevo_cip_cap and not nuevo_responsable:
            self.add_error('nuevo_responsable', "Si registra un CIP/CAP, debe completar también el nombre del responsable.")

        # Si ambos están completos, verificar que no exista ya
        if nuevo_responsable and nuevo_cip_cap:
            if ResponsableObra.objects.filter(nombre=nuevo_responsable).exists():
                self.add_error('nuevo_responsable', f"Ya existe un responsable con el nombre '{nuevo_responsable}'.")

        # Validar SUPERVISOR de obra
        if not supervisor_obra and not nuevo_supervisor:
            self.add_error('supervisor_obra', "Debe seleccionar un supervisor existente o registrar uno nuevo.")

        if nuevo_supervisor and not nuevo_supervisor_cip_cap:
            self.add_error('nuevo_supervisor_cip_cap', "Si registra un nuevo supervisor, debe completar también el CIP/CAP.")

        if nuevo_supervisor_cip_cap and not nuevo_supervisor:
            self.add_error('nuevo_supervisor', "Si registra un CIP/CAP del supervisor, debe completar también el nombre del supervisor.")

        if nuevo_supervisor and nuevo_supervisor_cip_cap:
            if SupervisorObra.objects.filter(nombre=nuevo_supervisor).exists():
                self.add_error('nuevo_supervisor', f"Ya existe un supervisor con el nombre '{nuevo_supervisor}'.")

        # Validaciones adicionales para campos requeridos
        areatechada_total = cleaned_data.get('areatechada_total')
        if areatechada_total and areatechada_total <= 0:
            self.add_error('areatechada_total', "El área techada debe ser mayor a 0.")

        num_pisos = cleaned_data.get('num_pisos')
        if num_pisos and num_pisos <= 0:
            self.add_error('num_pisos', "El número de pisos debe ser mayor a 0.")

        altura = cleaned_data.get('altura')
        if altura and altura <= 0:
            self.add_error('altura', "La altura debe ser mayor a 0.")

        num_sotano = cleaned_data.get('num_sotano')
        if num_sotano and num_sotano < 0:
            self.add_error('num_sotano', "El número de sótanos no puede ser negativo.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Si se proporcionó nuevo responsable, crearlo
        nuevo_responsable = self.cleaned_data.get('nuevo_responsable')
        nuevo_cip_cap = self.cleaned_data.get('nuevo_cip_cap')
        
        if nuevo_responsable and nuevo_cip_cap:
            responsable_obj, created = ResponsableObra.objects.get_or_create(
                nombre=nuevo_responsable,
                defaults={'cip_cap': nuevo_cip_cap}
            )
            instance.responsable_obra = responsable_obj

        # Si se proporcionó nuevo supervisor, crearlo
        nuevo_supervisor = self.cleaned_data.get('nuevo_supervisor')
        nuevo_supervisor_cip_cap = self.cleaned_data.get('nuevo_supervisor_cip_cap')
        
        if nuevo_supervisor and nuevo_supervisor_cip_cap:
            supervisor_obj, created = SupervisorObra.objects.get_or_create(
                nombre=nuevo_supervisor,
                defaults={'cip_cap': nuevo_supervisor_cip_cap}
            )
            instance.supervisor_obra = supervisor_obj

        if commit:
            instance.save()
        return instance


class ResolucionFilterForm(forms.Form):
    num_resolucion = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Resolución'})
    )
    num_expediente = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Expediente'})
    )
    administrado = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Administrado'})
    )
    nombre_licencia = forms.ModelChoiceField(
        queryset=LicenciaUso.objects.all(),
        required=False,
        empty_label="Todas las licencias",
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 