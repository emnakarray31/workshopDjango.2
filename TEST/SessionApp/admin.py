from django.contrib import admin
from .models import SESSION

@admin.register(SESSION)
class AdminSessionModel(admin.ModelAdmin):
    list_display = ("title", "tpic", "session_day", "start_time", "end_time", "room", "conference_name")
    ordering = ("session_day",)
    list_filter = ("conference", "room")
    search_fields = ("title", "tpic", "room")
    date_hierarchy = "session_day"

    fieldsets = (
        ("Informations générales", {
            "fields": ("title", "tpic", "conference")
        }),
        ("Détails de la session", {
            "fields": ("session_day", "start_time", "end_time", "room")
        }),
    )

    readonly_fields = ("session_id",)

    def conference_name(self, obj):
        return obj.conference.name
    conference_name.short_description = "Conférence"


#ce que jai ajouté:
# Tableau clair avec la conférence liée affichée.
# Filtres par conférence ou salle.
# Date hiérarchique sur le jour de session.
# Champs bien groupés par thème.