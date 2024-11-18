import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager
from django.db import models
from django.utils import timezone
from PIL import Image




class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)
    


def user_avatar_path(instance, filename):
    # Get the user's email or use a default value
    user_email = instance.email or 'default'
    # Construct the upload path: 'avatars/{user_email}/{filename}'
    return f'avatars/{user_email}/{filename}'


class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.CharField(max_length=200,null = True)

    def __str__(self):
        return self.body




ABIA = 'Abia'
ADAMAWA = 'Adamawa'
AKWA_IBOM = 'Akwa Ibom'
ANAMBRA = 'Anambra'
BAUCHI = 'Bauchi'
BAYELSA = 'Bayelsa'
BENUE = 'Benue'
BORNO = 'Borno'
CROSS_RIVER = 'Cross River'
DELTA = 'Delta'
EBONYI = 'Ebonyi'
EDO = 'Edo'
EKITI = 'Ekiti'
ENUGU = 'Enugu'
GOMBE = 'Gombe'
IMO = 'Imo'
JIGAWA = 'Jigawa'
KADUNA = 'Kaduna'
KANO = 'Kano'
KATSINA = 'Katsina'
KEBBI = 'Kebbi'
KOGI = 'Kogi'
KWARA = 'Kwara'
LAGOS = 'Lagos'
NASARAWA = 'Nasarawa'
NIGER = 'Niger'
OGUN = 'Ogun'
ONDO = 'Ondo'
OSUN = 'Osun'
OYO = 'Oyo'
PLATEAU = 'Plateau'
RIVERS = 'Rivers'
SOKOTO = 'Sokoto'
TARABA = 'Taraba'
YOBE = 'Yobe'
ZAMFARA = 'Zamfara'
FCT_ABUJA = 'FCT Abuja'

STATE_CHOICES = (
    (ABIA, 'Abia'),
    (ADAMAWA, 'Adamawa'),
    (AKWA_IBOM, 'Akwa Ibom'),
    (ANAMBRA, 'Anambra'),
    (BAUCHI, 'Bauchi'),
    (BAYELSA, 'Bayelsa'),
    (BENUE, 'Benue'),
    (BORNO, 'Borno'),
    (CROSS_RIVER, 'Cross River'),
    (DELTA, 'Delta'),
    (EBONYI, 'Ebonyi'),
    (EDO, 'Edo'),
    (EKITI, 'Ekiti'),
    (ENUGU, 'Enugu'),
    (GOMBE, 'Gombe'),
    (IMO, 'Imo'),
    (JIGAWA, 'Jigawa'),
    (KADUNA, 'Kaduna'),
    (KANO, 'Kano'),
    (KATSINA, 'Katsina'),
    (KEBBI, 'Kebbi'),
    (KOGI, 'Kogi'),
    (KWARA, 'Kwara'),
    (LAGOS, 'Lagos'),
    (NASARAWA, 'Nasarawa'),
    (NIGER, 'Niger'),
    (OGUN, 'Ogun'),
    (ONDO, 'Ondo'),
    (OSUN, 'Osun'),
    (OYO, 'Oyo'),
    (PLATEAU, 'Plateau'),
    (RIVERS, 'Rivers'),
    (SOKOTO, 'Sokoto'),
    (TARABA, 'Taraba'),
    (YOBE, 'Yobe'),
    (ZAMFARA, 'Zamfara'),
    (FCT_ABUJA, 'FCT Abuja'),
)


MALE = 'Male' 
FEMALE = 'Female'

GENDER_CHOICES = (
    (MALE,'Male'),
    (FEMALE,'Female')
)



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    bio = models.TextField(max_length=200, blank=True,null=True)
    hobbies = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    categories = models.ForeignKey(Categories,related_name='cat', on_delete=models.CASCADE,null=True)
    locations = models.CharField(max_length=200, choices = STATE_CHOICES, null=True)
    friends = models.ManyToManyField('self',blank=True)

    age = models.PositiveBigIntegerField(null=True)

    age_preference = models.PositiveBigIntegerField(null=True)
    
    friends_count = models.IntegerField(default=0)

    #people_you_may_know = models.ManyToManyField('self')

    posts_count = models.IntegerField(default=0)
    
    gender = models.CharField(max_length=30,choices=GENDER_CHOICES,null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def save(self, *args, **kwargs):
        if self.avatar:
            super().save(*args, **kwargs)  # Call the original save method to ensure other fields are saved first
            img = Image.open(self.avatar.path)
            img = img.resize((300, 300))  # Resize the image to 300x300 pixels
            img.save(self.avatar.path)  # Save the resized image
        else:
            super().save(*args, **kwargs)  # Call the original save method if no avatar is provided

    def get_avatar(self):
         if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url
         else:
             return 'http://127.0.0.1:8000/media/avatars/profile.png'
         

class FriendRequest(models.Model):
        

        SENT = 'sent'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'

        STATUS_CHIOCES = (
             (SENT,'Sent'),
             (ACCEPTED,'Accepted'),
             (REJECTED, 'Rejected'),
        )

        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        created_for = models.ForeignKey(User, related_name='received_friendrequest', on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User, related_name='created_friendrequest', on_delete=models.CASCADE)
        status = models.CharField(max_length=20, choices= STATUS_CHIOCES, default= SENT)

        def __str__(self):
            return f"From {self.created_by.name} to {self.created_for.name}"



