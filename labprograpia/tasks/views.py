from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import usuarios 

# Create your views here.
def home(request):
    try:
        return render (request, 'home.html',{
            'usuarioactual': get_user_model().objects.get(username=request.user.username)
        })  
    except:
        return render (request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render (request, 'signup.html', {
            'form': UserCreationForm
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
                'form': UserCreationForm,
                'error':'Nombre de usuario ya usado'
            })  
        return render (request, 'signup.html', {
                'form': UserCreationForm,
                'error':'Las contraseñas no coinciden'
            })  
    

    
@login_required
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
            nuevo_registro = usuarios(
                nombre_completo=nombre,
                nombre_usuario=usuarioactual,
                direccion=direccion,
                telefono=telefono,
                email=correo,
                id_usuario=idusuario
                
            )
            nuevo_registro.save()
            
            mensaje = "Datos insertados correctamente"
            return redirect(home)
            
        except Exception as e:
            mensaje = f"Error al insertar: {str(e)}"
            print(mensaje)
            
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
    
    