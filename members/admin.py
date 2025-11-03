from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone", "address")
    search_fields = ("name", "phone", "user__username")
    list_filter = ("gender", "membership_type")  # optional if you have these fields

