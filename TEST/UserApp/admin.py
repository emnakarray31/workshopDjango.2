# admin.site.register(USER)
# admin.site.register(ORGANIZINGCOMITEE)
from django.contrib import admin
from .models import USER, ORGANIZINGCOMITEE

@admin.register(USER)
class AdminUserModel(admin.ModelAdmin):
    list_display = ("user_id", "username", "first_name", "last_name", "email", "role", "affiliation", "nationality")
    ordering = ("created_at",)
    list_filter = ("role", "nationality")
    search_fields = ("first_name", "last_name", "email")
    readonly_fields = ("user_id", "date_joined", "last_login", "created_at", "updated_at")

    fieldsets = (
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email", "nationality")
        }),
        ("Informations professionnelles", {
            "fields": ("affiliation", "role")
        }),
        ("Infos système", {
            "fields": ("user_id", "username", "date_joined", "last_login", "created_at", "updated_at")
        }),
    )


@admin.register(ORGANIZINGCOMITEE)
class AdminCommitteeModel(admin.ModelAdmin):
    list_display = ("commitee_role", "user_name", "conference_name", "join_date")
    list_filter = ("commitee_role", "conference")
    search_fields = ("user__first_name", "user__last_name", "conference__name")
    date_hierarchy = "join_date"

    fieldsets = (
        ("Informations principales", {
            "fields": ("commitee_role", "user", "conference", "join_date")
        }),
    )

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_name.short_description = "Utilisateur"

    def conference_name(self, obj):
        return obj.conference.name
    conference_name.short_description = "Conférence"
