from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo')
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password):
        user=self.create_user(
                username=username,
                email=email,
                password=password
                )
        user.usuario_admin=True
        user.save()
        return user

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario',primary_key= True, max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=254,unique = True)
    nombres = models.CharField('Nombres', max_length=200, blank = True, null = True)
    apellido_paterno = models.CharField('Apellido Paterno', max_length=200,blank = True, null = True)
    apellido_materno = models.CharField('Apellido Materno', max_length=200,blank = True, null = True)
    telefono= models.CharField('Telefonos', max_length=20,blank = True, null = True)

    activo = models.BooleanField(default = True)
    usuario_admin = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_admin



'''
class Usuario(AbstractUser):
    username=models.CharField(max_length=50,primary_key=True)
    email = models.EmailField(blank=True,unique=True)
    #is_active = models.BooleanField(default=True)
    #verify_code=models.CharField(max_length=8,blank=True,null=True)
    #verify=models.BooleanField(default=True)
class Usuario(AbstractUser):
    #IdTipoUsuario=models.CharField(max_length=10,choices=choices,default=3)
    CodUsuario=models.CharField(max_length=50,null=True,blank=True)
    #Usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    #Contrasena=models.CharField(max_length=100)
    #Nombre=models.CharField(max_length=100)
    #ApellidoPaterno=models.CharField(max_length=100)
    #ApellidoMaterno=models.CharField(max_length=100)
    #Correo=models.EmailField(max_length=200,unique=True)
    Telefono=models.CharField(max_length=20,null=True,blank=True)
    Observacion=models.CharField(max_length=500,null=True,blank=True)
    #FechaCreacion=models.DateTimeField(auto_now_add=True)
    #UsuarioCreacion=models.CharField(max_length=100)
    #FechaModificacion=models.DateTimeField(auto_now=True)
    #UsuarioModificacion=models.CharField(max_length=100)
    #Eliminado=models.BooleanField(default=False)
'''
