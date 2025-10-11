from django.contrib import admin
from .models import CONFERENCE,SUBMISSION
# Register your models here.
admin.site.site_title="gestion conferance 25/26"
admin.site.site_header="gestion conferance"
admin.site.site_index_title="Django app conferance"
# admin.site.register(CONFERENCE)
admin.site.register(SUBMISSION)

class SubmissionInline(admin.StackedInline): #TabularInline
    model = SUBMISSION
    extra = 1
    readonly_fields = ("submission_date",)


# pour afficher le tableau de conferance
@admin.register(CONFERENCE)
class AdminConferanceModel(admin.ModelAdmin):
    list_display=("name","Theme","location","start_date","end_date","a")
    ordering=("start_date",) #pour les organiser
    list_filter=("Theme",)
    search_fields=("name","description",)
    date_hierarchy="start_date"

    fieldsets = (
        ("Informations générales", {
            "fields": ("name", "Theme", "description")
        }),
        ("Informations logistiques", {
            "fields": ("location", "start_date", "end_date")
        }),
    )
    readonly_fields=("conference_id",)
    def a(self,objet):
        if objet.start_date and objet.end_date :
            return (objet.end_date-objet.start_date).days
        return "rien a signaler"
    a.short_description="Duration(Days)"
    inlines = [SubmissionInline]
