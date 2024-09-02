from django.contrib import admin

from system.models import LegalUser, SocialUser

# Register your models here.
admin.site.register(SocialUser)
admin.site.register(LegalUser)
