from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from .models import Resolucion, DetalleResolucion, ResponsableObra, Zonificacion, LicenciaUso
from .forms import CustomUserCreationForm, ResolucionForm, DetalleResolucionForm, ResolucionFilterForm


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Contacte al administrador para asignar permisos.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required
def dashboard(request):
    user_groups = [group.name for group in request.user.groups.all()]
    
    if 'Obras' in user_groups:
        return render(request, 'resoluciones/dashboard_obras.html')
    elif 'Fiscalización' in user_groups:
        return redirect('lista_resoluciones')
    else:
        messages.warning(request, 'No tiene permisos asignados. Contacte al administrador.')
        return render(request, 'resoluciones/dashboard_obras.html')


class ResolucionListView(LoginRequiredMixin, ListView):
    model = Resolucion
    template_name = 'resoluciones/lista_resoluciones.html'
    context_object_name = 'resoluciones'
    paginate_by = 10

    def get_queryset(self):
        queryset = Resolucion.objects.all()
        user_groups = [group.name for group in self.request.user.groups.all()]
        
        # Si es usuario de Obras, solo sus resoluciones
        if 'Obras' in user_groups and 'Fiscalización' not in user_groups:
            queryset = queryset.filter(usuario=self.request.user)
        
        # Aplicar filtros
        form = ResolucionFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['num_resolucion']:
                queryset = queryset.filter(
                    num_resolucion__icontains=form.cleaned_data['num_resolucion']
                )
            if form.cleaned_data['num_expediente']:
                queryset = queryset.filter(
                    num_expediente__icontains=form.cleaned_data['num_expediente']
                )
            if form.cleaned_data['administrado']:
                queryset = queryset.filter(
                    administrado__icontains=form.cleaned_data['administrado']
                )
            if form.cleaned_data['nombre_licencia']:
                queryset = queryset.filter(
                    nombre_licencia=form.cleaned_data['nombre_licencia']
                )
        
        return queryset.order_by('-fecha_emision')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ResolucionFilterForm(self.request.GET)
        context['user_groups'] = [group.name for group in self.request.user.groups.all()]
        return context


class ResolucionDetailView(LoginRequiredMixin, DetailView):
    model = Resolucion
    template_name = 'resoluciones/detalle_resolucion.html'
    context_object_name = 'resolucion'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user_groups = [group.name for group in self.request.user.groups.all()]
        
        # Si es usuario de Obras y no es su resolución, no permitir acceso
        if 'Obras' in user_groups and 'Fiscalización' not in user_groups:
            if obj.usuario != self.request.user:
                messages.error(self.request, 'No tiene permisos para ver esta resolución.')
                return redirect('lista_resoluciones')
        
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups'] = [group.name for group in self.request.user.groups.all()]
        try:
            context['detalle'] = self.object.detalleresolucion
        except DetalleResolucion.DoesNotExist:
            context['detalle'] = None
        return context


@login_required
def crear_resolucion(request):
    user_groups = [group.name for group in request.user.groups.all()]
    
    # Solo usuarios de Obras pueden crear resoluciones
    if 'Obras' not in user_groups:
        messages.error(request, 'No tiene permisos para crear resoluciones.')
        return redirect('dashboard')

    if request.method == 'POST':
        resolucion_form = ResolucionForm(request.POST)
        detalle_form = DetalleResolucionForm(request.POST)
        
        if resolucion_form.is_valid() and detalle_form.is_valid():
            try:
                with transaction.atomic():
                    # Crear resolución
                    resolucion = resolucion_form.save(commit=False)
                    resolucion.usuario = request.user
                    resolucion.save()
                    
                    # Crear detalle
                    detalle = detalle_form.save(commit=False)
                    detalle.resolucion = resolucion
                    detalle.save()
                    
                    messages.success(request, 'Resolución creada exitosamente.')
                    return redirect('detalle_resolucion', pk=resolucion.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la resolución: {str(e)}')
    else:
        resolucion_form = ResolucionForm()
        detalle_form = DetalleResolucionForm()

    context = {
        'resolucion_form': resolucion_form,
        'detalle_form': detalle_form,
        'title': 'Nueva Resolución'
    }
    return render(request, 'resoluciones/form_resolucion.html', context)


@login_required
def editar_resolucion(request, pk):
    resolucion = get_object_or_404(Resolucion, pk=pk)
    user_groups = [group.name for group in request.user.groups.all()]
    
    # Solo usuarios de Obras pueden editar y solo sus propias resoluciones
    if 'Obras' not in user_groups or resolucion.usuario != request.user:
        messages.error(request, 'No tiene permisos para editar esta resolución.')
        return redirect('detalle_resolucion', pk=pk)

    try:
        detalle = resolucion.detalleresolucion
    except DetalleResolucion.DoesNotExist:
        detalle = None

    if request.method == 'POST':
        resolucion_form = ResolucionForm(request.POST, instance=resolucion)
        detalle_form = DetalleResolucionForm(request.POST, instance=detalle) if detalle else DetalleResolucionForm(request.POST)
        
        if resolucion_form.is_valid() and detalle_form.is_valid():
            try:
                with transaction.atomic():
                    resolucion_form.save()
                    
                    if detalle:
                        detalle_form.save()
                    else:
                        new_detalle = detalle_form.save(commit=False)
                        new_detalle.resolucion = resolucion
                        new_detalle.save()
                    
                    messages.success(request, 'Resolución actualizada exitosamente.')
                    return redirect('detalle_resolucion', pk=resolucion.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar la resolución: {str(e)}')
    else:
        resolucion_form = ResolucionForm(instance=resolucion)
        detalle_form = DetalleResolucionForm(instance=detalle) if detalle else DetalleResolucionForm()

    context = {
        'resolucion_form': resolucion_form,
        'detalle_form': detalle_form,
        'resolucion': resolucion,
        'title': 'Editar Resolución'
    }
    return render(request, 'resoluciones/form_resolucion.html', context)


@login_required
def mis_resoluciones(request):
    user_groups = [group.name for group in request.user.groups.all()]
    
    if 'Obras' not in user_groups:
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('dashboard')

    resoluciones = Resolucion.objects.filter(usuario=request.user).order_by('-fecha_emision')
    
    # Paginación
    paginator = Paginator(resoluciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'resoluciones': page_obj,
        'user_groups': user_groups,
        'title': 'Mis Resoluciones'
    }
    return render(request, 'resoluciones/lista_resoluciones.html', context)
