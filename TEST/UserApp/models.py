from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#new 
import uuid
from django.core.exceptions import ValidationError #email
from django.core.validators import RegexValidator #nom prenom


def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","centrale.tn"]
    email_domaine=email.split("@")[1]
    if email_domaine not in domaine:
        raise ValidationError("l'email est invalide et doit appartenir a un domaine universitaire")

name_validator=RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="ce champs ne doit contenir que des lettres et des espaces"
)

class USER(AbstractUser):
    user_id = models.CharField(max_length=8,primary_key=True,editable=False,unique=True)
    first_name = models.CharField(max_length=255,validators=[name_validator])
    last_name = models.CharField(max_length=255,validators=[name_validator])
    affiliation = models.CharField(max_length=255)
    ROLE = [
        ("participant", "participant"),
        ("comitee","organizing comitee member")
    ]
    role = models.CharField(max_length=255,choices= ROLE,default="participant")
    email = models.EmailField(unique=True , validators=[verify_email])
    nationality = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not self.user_id:
            newid=generate_user_id()
            while USER.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
            self.user_id=newid
        super().save(*args,**kwargs)




class ORGANIZINGCOMITEE(models.Model):
    chair = [
        ('chair','chair'),
        ('co-chair','co-chair'),
        ('member','member')
    ]
    commitee_role = models.CharField(max_length=255,choices=chair)
    join_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name='committees')
    user = models.ForeignKey("UserApp.USER", on_delete=models.CASCADE, related_name='committees')
    conference = models.ForeignKey('ConferenceApp.CONFERENCE',on_delete=models.CASCADE,related_name='committees')

