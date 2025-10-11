from django.db import models
from ConferenceApp.models import CONFERENCE
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
class SESSION(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    tpic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()  

    room_validator = RegexValidator(
        regex=r'^[A-Za-z0-9\s]+$',
        message="Le nom de la salle ne doit contenir que des lettres, chiffres et espaces."
    )
    room = models.CharField(max_length=255, validators=[room_validator])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(CONFERENCE,on_delete=models.CASCADE,related_name="sessions")
    def clean(self):
        if self.conference:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    "La date de la session doit être comprise entre la date de début et la date de fin de la conférence."
                )
        if self.end_time <= self.start_time:
            raise ValidationError("L’heure de fin doit être supérieure à l’heure de début.")
    