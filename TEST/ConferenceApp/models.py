from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator,FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils import timezone

def validate_keywords(value):
    mots = [mot.strip() for mot in value.split(',')]
    if len(mots) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")
        
# Create your models here.
class CONFERENCE(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[
        MinLengthValidator(30,"La description doit contenir au moins 30 caractères.")
    ]
    # description = models.TextField(validators=[
    #     MaxLengthValidator(30,"La description doit contenir au moins 30 caractères.")
    # ]
    )
    Theme_list = [
        ('CSAI', 'Computer Science & Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    Theme = models.CharField(max_length=225,choices=Theme_list)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("La date de début de la conférence doit être antérieure à la date de fin.")
    def __str__ (self):
            return f"la conférance a comme titre {self.name} , cree le {self.created_at}"



class SUBMISSION(models.Model):
    submission_id = models.CharField(max_length=255,primary_key=True,unique=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    # keywords = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    # papers = models.FileField(upload_to='paper/')
    papers = models.FileField(upload_to='paper/', validators=[FileExtensionValidator(['pdf'], "Le fichier doit être un .pdf")])
    STATUS =[
        ('submitted','submitted'),
        ('under review', 'under review'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    ]
    status = models.CharField(max_length=50,choices=STATUS)
    payed = models.BooleanField(default=False)
    submission_date= models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('UserApp.USER',on_delete=models.CASCADE,related_name='submissions')
    conference = models.ForeignKey(CONFERENCE,on_delete=models.CASCADE,related_name='submissions')  
    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = "SUB" + get_random_string(8).upper()
        super().save(*args, **kwargs)

    def clean(self):
        #Vérifier que la soumission est faite avant le début de la conférence
        today = timezone.now().date()
        if self.conference.start_date <= today:
            raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")
        #Limiter à 3 soumissions par jour par utilisateur
        same_day_submissions = SUBMISSION.objects.filter(
            user=self.user,
            submission_date=today
        ).exclude(pk=self.pk).count()
        if same_day_submissions >= 3:
            raise ValidationError("Vous ne pouvez pas soumettre à plus de 3 conférences par jour.")
   