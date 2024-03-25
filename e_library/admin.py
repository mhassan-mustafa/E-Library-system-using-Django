from django.contrib import admin
from admins.models import Books, Admins
from members.models import Members

admin.site.register(Books)
admin.site.register(Admins)
admin.site.register(Members)
