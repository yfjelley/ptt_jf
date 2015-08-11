from django.contrib import admin

from bbs.account.models import profile, social

# Register your models here.
admin.site.register(profile)
admin.site.register(social)
