from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resolucion, DetalleResolucion, ResponsableObra, Zonificacion, LicenciaUso


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
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'num_resolucion': forms.TextInput(attrs={'class': 'form-control'}),
            'num_expediente': forms.TextInput(attrs={'class': 'form-control'}),
            'num_recibo': forms.TextInput(attrs={'class': 'form-control'}),
            'administrado': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'propietario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nombre_licencia': forms.Select(attrs={'class': 'form-select'}),
        }


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

    class Meta:
        model = DetalleResolucion
        fields = [
            'zonificacion', 'areatechada_total', 'detalle_areatechada', 
            'num_pisos', 'altura', 'num_sotano', 'semisotano', 'responsable_obra'
        ]
        widgets = {
            'zonificacion': forms.Select(attrs={'class': 'form-select'}),
            'areatechada_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'detalle_areatechada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_pisos': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'num_sotano': forms.NumberInput(attrs={'class': 'form-control'}),
            'semisotano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'responsable_obra': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        responsable_obra = cleaned_data.get('responsable_obra')
        nuevo_responsable = cleaned_data.get('nuevo_responsable')
        nuevo_cip_cap = cleaned_data.get('nuevo_cip_cap')

        # Validar que al menos uno de los dos caminos esté completo
        if not responsable_obra and not nuevo_responsable:
            raise forms.ValidationError(
                "Debe seleccionar un responsable existente o registrar uno nuevo."
            )

        # Si se está registrando nuevo responsable, ambos campos son requeridos
        if nuevo_responsable and not nuevo_cip_cap:
            raise forms.ValidationError(
                "Si registra un nuevo responsable, debe completar también el CIP/CAP."
            )

        if nuevo_cip_cap and not nuevo_responsable:
            raise forms.ValidationError(
                "Si registra un CIP/CAP, debe completar también el nombre del responsable."
            )

        # Si ambos están completos, verificar que no exista ya
        if nuevo_responsable and nuevo_cip_cap:
            if ResponsableObra.objects.filter(nombre=nuevo_responsable).exists():
                raise forms.ValidationError(
                    f"Ya existe un responsable con el nombre '{nuevo_responsable}'."
                )

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