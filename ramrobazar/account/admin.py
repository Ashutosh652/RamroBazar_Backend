from django.contrib import admin
from .models import User, Thread, Message


admin.site.register(User)
admin.site.register(Thread)
admin.site.register(Message)