from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import usuarios 
from django.db import IntegrityError

# Create your views here.
def home(request):
        return render (request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render (request, 'signup.html', {
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save
                login(request, user)
                return redirect('datosdeusuario')
                
            except:
                return render (request, 'signup.html', {
                'error':'Nombre de usuario ya usado'
            })  
        return render (request, 'signup.html', {
                'error':'Las contraseñas no coinciden'
            })  
    

    
def datosdeusuario(request):
    usuarioactual = request.user.username
    idusuario = request.user.id
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombrecompleto')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')

        try:
            # Crear y guardar el registro usando el ORM
            crear_usuario = usuarios(
                nombre_completo=nombre,
                nombre_usuario=usuarioactual,
                direccion=direccion,
                telefono=telefono,
                email=correo,
                id_usuario=idusuario
                
            )
            crear_usuario.save()
            
            mensaje = "Datos insertados correctamente"
            return redirect(home)
            
        except Exception as e:
            return render(request, 'datosdeusuario.html', {
            'usuarioactual': usuarioactual,
            'mensaje': 'Hubo un error en el registro',
            'idusuario': idusuario
        })
            
    return render(request, 'datosdeusuario.html', {
        'usuarioactual': usuarioactual
    })
    
    
    
def signout(request):
    logout(request)
    return redirect('home')



def signin(request):
    if request.method == 'GET':
        return render (request, 'signin.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
                return render(request, 'signin.html',{
                    'error': 'El usuario o la contraseña son inconrrectos'
                })
        else:
                login(request, user)
                return redirect('home')
    
    
def perfil(request):
    registro = get_object_or_404(usuarios, id_usuario=request.user.id)
    return render(request,'perfil.html',{
        'usuarioactual':request.user.username,
        'nombrecompleto':registro.nombre_completo,
        'direccion':registro.direccion,
        'telefono':registro.telefono,
        'correo':registro.email
        
    })
    
def editardatos(request):
    registro = get_object_or_404(usuarios, id_usuario=request.user.id)
    usuarioactual = request.user.username
    idusuario = request.user.id
    
    if request.method=='POST':
        try:
            registro.nombre_completo = request.POST.get('nombrecompleto')
            registro.direccion = request.POST.get('direccion')
            registro.telefono = request.POST.get('telefono')
            registro.email = request.POST.get('correo')
            if registro.nombre_completo and registro.direccion and registro.telefono and registro.email:  # Ejemplo de validación simple
                registro.save()
                return redirect('perfil')
            else:
                return render(request, 'editardatos.html', {
                'error':'Todos los campos son obligatorios',
                'registro': registro,
                'usuarioactual':usuarioactual,
                'idusuario':idusuario,
                'nombrecompleto':registro.nombre_completo,
                'direccion':registro.direccion,
                'telefono':registro.telefono,
                'correo':registro.email})
                
        except IntegrityError:
            return render(request, 'editardatos.html',{
                'error':'Error de integridad (Pruebe cambiando su email)',
                'usuarioactual':usuarioactual,
                'idusuario':idusuario,
                'nombrecompleto':registro.nombre_completo,
                'direccion':registro.direccion,
                'telefono':registro.telefono,
                'correo':registro.email
            })
    else:
            
            return render(request, 'editardatos.html', {'registro': registro,
        'usuarioactual':usuarioactual,
        'idusuario':idusuario,
        'nombrecompleto':registro.nombre_completo,
        'direccion':registro.direccion,
        'telefono':registro.telefono,
        'correo':registro.email})
    
        
    return render(request, 'editardatos.html',{
        'usuarioactual':usuarioactual,
        'idusuario':idusuario,
        'nombrecompleto':registro.nombre_completo,
        'direccion':registro.direccion,
        'telefono':registro.telefono,
        'correo':registro.email
    })
    