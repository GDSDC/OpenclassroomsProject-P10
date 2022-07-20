from django.contrib import admin
from core.users.models import User, Contributor

admin.site.register(User)
admin.site.register(Contributor)
