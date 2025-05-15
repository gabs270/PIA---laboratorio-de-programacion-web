from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import usuarios, categorias,articulos,imagenes_articulos,favoritos,reportes_articulos
from django.db import IntegrityError
from django.conf import settings
import os
from datetime import datetime
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def home(request):
    # Obtener todos los artículos ordenados por fecha (más recientes primero)
    articulos_list = articulos.objects.filter(estado='aceptado').order_by('-fecha_actualizacion')
    for articulo in articulos_list:
        articulo.imagen_principal = articulo.imagenes.filter(es_principal=True).first()
    return render(request, 'home.html', {
         'articulos': articulos_list
    })
    


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
        avatar_file = request.FILES['avatar']
        

        try:
            # Cambiar el nombre del archivo
            extension = avatar_file.name.split('.')[-1]
            nuevo_nombre = f"avatar_{request.user.id}.{extension}"
            avatar_file.name = nuevo_nombre
                    
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(upload_dir, exist_ok=True)
                    
            file_path = f'avatars/{avatar_file.name}'  # Ruta relativa (ej: 'avatars/foto.jpg')
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)
            
            
            # Crear y guardar el registro usando el ORM
            crear_usuario = usuarios(
                nombre_completo=nombre,
                nombre_usuario=usuarioactual,
                direccion=direccion,
                telefono=telefono,
                email=correo,
                id_usuario=idusuario,
                avatar_url=file_path
                
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
    try:
        registro = get_object_or_404(usuarios, id_usuario=request.user.id)
        return render(request,'perfil.html',{
        'usuarioactual':request.user.username,
        'nombrecompleto':registro.nombre_completo,
        'direccion':registro.direccion,
        'telefono':registro.telefono,
        'correo':registro.email,
        'foto':registro.avatar_url    
        })
    except:
        return render(request,'perfil.html')
    
    
def editardatos(request):
    registro = get_object_or_404(usuarios, id_usuario=request.user.id)
    usuarioactual = request.user.username
    idusuario = request.user.id
    
    if request.method=='POST':
                registro.nombre_completo = request.POST.get('nombrecompleto')
                registro.direccion = request.POST.get('direccion')
                registro.telefono = request.POST.get('telefono')
                registro.email = request.POST.get('correo')
                
                if request.method == 'POST' and request.FILES.get('avatar'):
                    avatar_file = request.FILES['avatar']
                    print(request.FILES)
                    
                    # Cambiar el nombre del archivo
                    extension = avatar_file.name.split('.')[-1]
                    nuevo_nombre = f"avatar_{request.user.username}.{extension}"
                    avatar_file.name = nuevo_nombre
                   
                    
                    upload_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    
                    file_path = f'avatars/{avatar_file.name}'  # Ruta relativa (ej: 'avatars/foto.jpg')
                    with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                        for chunk in avatar_file.chunks():
                            f.write(chunk)
                    registro.avatar_url = file_path
                        
                    
                    if registro.nombre_completo and registro.direccion and registro.telefono and registro.email:  
                        registro.save()
                        return redirect('perfil')
                    else:
                        return render(request, 'editardatos.html', {'error':'Todos los campos son obligatorios','foto':registro.avatar_url, 'registro': registro,'usuarioactual':usuarioactual,'idusuario':idusuario,'nombrecompleto':registro.nombre_completo,'direccion':registro.direccion,'telefono':registro.telefono,'correo':registro.email,})
                         
                else:            
                    
                    if registro.nombre_completo and registro.direccion and registro.telefono and registro.email:  
                        registro.save()
                        return redirect('perfil')
                    else:
                        return render(request, 'editardatos.html', {'error':'Todos los campos son obligatorios','foto':registro.avatar_url ,'registro': registro,'usuarioactual':usuarioactual,'idusuario':idusuario,'nombrecompleto':registro.nombre_completo,'direccion':registro.direccion,'telefono':registro.telefono,'correo':registro.email,})
                            
    else:   
                return render(request, 'editardatos.html', {'registro': registro,'foto':registro.avatar_url ,
                'usuarioactual':usuarioactual,
                'idusuario':idusuario,
                'nombrecompleto':registro.nombre_completo,
                'direccion':registro.direccion,
                'telefono':registro.telefono,
                'correo':registro.email,
                })

    
    
def nuevoarticulo(request):
    datos = categorias.objects.all().values_list('id_categoria', 'nombre')
    if request.method=='POST':
        
        titulo = request.POST.get('titulo')
        lugar = request.POST.get('lugar')
        fecha_acontecimient = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')
        lacategoria=request.POST.get('categoria')
        
        if request.method == 'POST' and titulo and lugar and fecha_acontecimient and descripcion and lacategoria:
            crear_articulo = articulos(
                autor_id=request.user.id,
                titulo=titulo,
                lugar=lugar,
                fecha_acontecimiento=fecha_acontecimient,
                descripcion=descripcion,
                fecha_actualizacion=datetime.now(),
                estado='borrador'
                )
            categoriaa = categorias.objects.get(id_categoria=lacategoria)
            crear_articulo.categoria_id = categoriaa.id_categoria
            crear_articulo.save()
        else:
            return render(request, 'nuevoarticulo.html', {'error':'Todos los campos son obligatorios', 'opciones': datos})   
            
        id_articulo = crear_articulo.id_articulo
        print(id_articulo)
        
        if request.method == 'POST' and request.FILES.get('imgprincipal'):
                    imgprincipal=request.FILES['imgprincipal']
                    
                    extension = imgprincipal.name.split('.')[-1]
                    nuevo_nombre = f"imagenprincipal_articulo{id_articulo}_Usuario{request.user.id}.{extension}"
                    imgprincipal.name = nuevo_nombre
                   
                    upload_dir = os.path.join(settings.MEDIA_ROOT, 'imagenesArticulos')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    file_path = f'imagenesArticulos/{imgprincipal.name}' 
                    with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                        for chunk in imgprincipal.chunks():
                            f.write(chunk)
                            
                    crear_imagen= imagenes_articulos(
                        articulo_id=id_articulo,
                        es_principal=1,
                        url_imagen=file_path,
                        fecha_creacion=datetime.now()
                    )
                    crear_imagen.save()
        else:
            return render(request, 'nuevoarticulo.html', {'error':'Todos los campos son obligatorios', 'opciones': datos}) 
                    
        if request.method == 'POST' and request.FILES.get('imgsarticulo'):
                    
                    for i, archivo in enumerate(request.FILES.getlist('imgsarticulo'), start=1):
                        
                        extension = archivo.name.split('.')[-1]
                        nuevo_nombre = f"imgsarticulo{i}_articulo{id_articulo}_Usuario{request.user.username}.{extension}"
                        archivo.name = nuevo_nombre
                    
                        upload_dir = os.path.join(settings.MEDIA_ROOT, 'imagenesArticulos')
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        file_path = f'imagenesArticulos/{archivo.name}' 
                        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                            for chunk in archivo.chunks():
                                f.write(chunk)
                                
                        crear_imagen= imagenes_articulos(
                            articulo_id=id_articulo,
                            es_principal=0,
                            url_imagen=file_path,
                            fecha_creacion=datetime.now()
                        )
                        crear_imagen.save()                    
                    return redirect('perfil')
        else:
            return render(request, 'nuevoarticulo.html', {'error':'Todos los campos son obligatorios', 'opciones': datos}) 
    
    else:
        return render(request, 'nuevoarticulo.html', {'opciones': datos})
   



def publicados(request):
    registros = articulos.objects.filter(autor_id=request.user.id)
    return render(request,'publicados.html', {'registros': registros})




def detalle_articulo(request, pk):
    articulo = get_object_or_404(articulos, pk=pk)
    registros = articulos.objects.get(id_articulo=articulo.id_articulo)
    imagenprincipal = articulos.objects.get(id_articulo=articulo.id_articulo)
    
    usuario = usuarios.objects.get(id_usuario=articulo.autor_id)
    avatar_url = usuario.avatar_url
    username=usuario.nombre_usuario
    
    articuloss = articulos.objects.filter(estado='aceptado')
    articulosordenados = articulos.objects.filter(estado='aceptado').order_by('-fecha_actualizacion')
    
    for articuloordenado in articulosordenados:
        articuloordenado.imagen_principal = articuloordenado.imagenes.filter(es_principal=True).first()
        

    
    try:
        if request.method == 'POST' and 'guardar_favorito' in request.POST:
            
            favoritos.objects.create(
            usuario_id=request.user.id,
            articulo_id=articulo.id_articulo,
            fecha_agregado=datetime.now()
            )
    except IntegrityError:  # Si ya existe (por unique_together)
        print('Ya se ha agregado anteriormente')
    except Exception as e:  # Para otros errores
        messages.error(request, f"❌ Error: {str(e)}")
        
        return render(request, 'detalle_articulo.html', {'articulo': articulo,
        'registros': registros,'imagenprincipal':imagenprincipal, 'foto':avatar_url,'username':username, 'articulos':articuloss, 'articulosordenados':articulosordenados})
    
    
    return render(request, 'detalle_articulo.html', {'articulo': articulo,
        'registros': registros,'imagenprincipal':imagenprincipal, 'foto':avatar_url,'username':username, 'articulos':articuloss, 'articulosordenados':articulosordenados})
    
    
    
    
def editararticulos(request):
    datos = categorias.objects.all().values_list('id_categoria', 'nombre')
    id_articulo = request.GET.get('id_articulo')
    articulo = articulos.objects.get(id_articulo=id_articulo)
    
    titulo = request.POST.get('titulo')
    lugar = request.POST.get('lugar')
    fecha_acontecimiento = request.POST.get('fecha')
    descripcion = request.POST.get('descripcion')
    lacategoria=request.POST.get('categoria')
    fecha_actualizacion=datetime.now()
        
    if request.method=='POST':
        if request.method=='POST' and titulo and lugar and fecha_acontecimiento and descripcion and lacategoria:
            articulo.titulo = titulo
            articulo.lugar = lugar
            articulo.fecha_acontecimiento = fecha_acontecimiento
            articulo.descripcion = descripcion
            articulo.fecha_actualizacion=fecha_actualizacion
        
        
            categoriaa = categorias.objects.get(id_categoria=lacategoria)
            articulo.categoria_id = categoriaa.id_categoria
            articulo.save()
        else:
            return render(request, 'editararticulos.html', {'error':'Todos los campos son obligatorios',
            'articulo': articulo,
            'opciones':datos, 
            'titulo':articulo.titulo,
            'lugar':articulo.lugar,
            'fecha':articulo.fecha_acontecimiento,
            'descripcion':articulo.descripcion                                          
            })
            
        id_articulo = articulo.id_articulo
            
        if request.method == 'POST' and request.FILES.get('imgprincipal'):
                        imgprincipal=request.FILES['imgprincipal']
                        
                        extension = imgprincipal.name.split('.')[-1]
                        nuevo_nombre = f"imagenprincipal_articulo{id_articulo}_Usuario{request.user.id}.{extension}"
                        imgprincipal.name = nuevo_nombre
                    
                        upload_dir = os.path.join(settings.MEDIA_ROOT, 'imagenesArticulos')
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        file_path = f'imagenesArticulos/{imgprincipal.name}' 
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        imagen_existente = imagenes_articulos.objects.get(url_imagen=file_path)
                        print(imagen_existente)
                        imagen_existente.delete()
                        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                            for chunk in imgprincipal.chunks():
                                f.write(chunk)
                                
                        crear_imagen= imagenes_articulos(
                            articulo_id=id_articulo,
                            es_principal=1,
                            url_imagen=file_path,
                            fecha_creacion=datetime.now()
                        )
                        crear_imagen.save()
        if request.method == 'POST' and request.FILES.get('imgsarticulo'):
                        
                        for i, archivo in enumerate(request.FILES.getlist('imgsarticulo'), start=1):
                            
                            extension = archivo.name.split('.')[-1]
                            nuevo_nombre = f"imgsarticulo{i}_articulo{id_articulo}_Usuario{request.user.username}.{extension}"
                            archivo.name = nuevo_nombre
                        
                            upload_dir = os.path.join(settings.MEDIA_ROOT, 'imagenesArticulos')
                            os.makedirs(upload_dir, exist_ok=True)
                            
                            file_path = f'imagenesArticulos/{archivo.name}' 
                            
                            imagen_existente = imagenes_articulos.objects.filter(url_imagen=file_path).first()
                            if imagen_existente:
                                imagen_existente.delete()
                            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as f:
                                for chunk in archivo.chunks():
                                    f.write(chunk)
                                    
                            crear_imagen= imagenes_articulos(
                                articulo_id=id_articulo,
                                es_principal=0,
                                url_imagen=file_path,
                                fecha_creacion=datetime.now()
                            )
                            crear_imagen.save()                    
                        
            

        return render(request, 'editararticulos.html', {'articulo': articulo,'opciones':datos, 
        'titulo':articulo.titulo,
        'lugar':articulo.lugar,
        'fecha':articulo.fecha_acontecimiento,
        'descripcion':articulo.descripcion                                          
        })  
    else:
        return render(request, 'editararticulos.html', {'articulo': articulo,'opciones':datos, 
        'titulo':articulo.titulo,
        'lugar':articulo.lugar,
        'fecha':articulo.fecha_acontecimiento,
        'descripcion':articulo.descripcion                                          
        }) 
        

    
def paginafavoritos(request):
    registros=favoritos.objects.filter(usuario_id=request.user.id).select_related('articulo')
    
    return render(request, 'paginafavoritos.html',{
        'registros':registros
    })
    


def reportar(request):
    id_articulo = request.GET.get('id_articulo')
    articulo= articulos.objects.get(id_articulo=id_articulo)
    
    descripcion = request.POST.get('descripcion')
    
    if request.method=='POST' and descripcion:
        crear_reporte=reportes_articulos(
            articulo_id=articulo.id_articulo,
            usuario_reportador_id=request.user.id,
            descripcion=descripcion,
            fecha_reporte=datetime.now()
        )
        crear_reporte.save()
        return redirect('home')    
    return render(request, 'reportar.html',{
        'articulo':articulo
    })
    
    
    
   
from django.db.models import CharField
from django.db.models.functions import Cast
    
def buscar(request):
    datos = categorias.objects.all().values_list('id_categoria', 'nombre')
    query = request.GET.get('q', '').strip()
    id_categoria = request.GET.get('categoria', '')
    resultados = articulos.objects.all()
    
    if id_categoria:
        resultados = resultados.filter(categoria_id=id_categoria)
    
    if query:
        resultados = resultados.annotate(
            descripcion_str=Cast('descripcion', CharField())
        ).filter(
            Q(titulo__icontains=query) | 
            Q(descripcion_str__icontains=query)
        )
    
    resultados = resultados.order_by('-fecha_actualizacion')
    
    return render(request, 'buscar.html', {
        'resultados': resultados,
        'query': query,
        'id_categoria': id_categoria,
        'opciones': datos
    })
    
    
def detalle_usuario(request, nombre_usuario):
    usuario = get_object_or_404(usuarios, nombre_usuario=nombre_usuario)
    articulo=articulos.objects.filter(autor_id=usuario.id_usuario)
    
    return render(request,'detalle_usuario.html',{
        'usuario':usuario,
        'articulos':articulo
    })