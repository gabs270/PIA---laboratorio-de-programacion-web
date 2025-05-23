# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class articulos(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    ]
    id_articulo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    descripcion = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI')  # This field type is a guess.
    lugar = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)
    fecha_acontecimiento = models.DateField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    autor = models.ForeignKey('Usuarios', models.DO_NOTHING)
    categoria = models.ForeignKey('Categorias', on_delete=models.CASCADE, blank=True, null=True,choices=ESTADOS,default='borrador')
    estado = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)

    def obtener_imagen_principal(self):
        try:
            return self.imagenes.get(es_principal=True)
        except imagenes_articulos.DoesNotExist:
            # Devuelve la primera imagen si no hay marcada como principal
            return self.imagenes.first()
    def obtener_imagenes_secundarias(self):
        return self.imagenes.exclude(es_principal=True)
        
    class Meta:
        managed = False
        db_table = 'articulos'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1253_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    descripcion = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'categorias'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class favoritos(models.Model):
    usuario = models.OneToOneField('Usuarios',on_delete=models.CASCADE, primary_key=True ) 
    articulo = models.ForeignKey(articulos, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favoritos'
        unique_together = ['usuario', 'articulo']
        


class imagenes_articulos(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    articulo = models.ForeignKey(articulos, models.DO_NOTHING,related_name='imagenes')
    url_imagen = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    es_principal = models.BooleanField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagenes_articulos'


class reportes_articulos(models.Model):
    id = models.AutoField(primary_key=True)
    articulo = models.ForeignKey('articulos', models.DO_NOTHING) 
    usuario_reportador = models.ForeignKey('usuarios', models.DO_NOTHING)
    descripcion = models.TextField(db_collation='SQL_Latin1_General_CP1253_CI_AI') 
    fecha_reporte = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reportes_articulos'
        unique_together = ['articulo', 'usuario_reportador']


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'



class usuarios(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nombre_completo = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    nombre_usuario = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    direccion = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)
    telefono = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1253_CI_AI', blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, db_collation='SQL_Latin1_General_CP1253_CI_AI')
    avatar_url = models.ImageField(upload_to="avatares/", blank=True, null=True)
    es_administrador = models.BooleanField(blank=True, null=True)

  
    

    class Meta:
        managed = False
        db_table = 'usuarios'

