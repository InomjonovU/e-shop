from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Enter)
admin.site.register(Out)
admin.site.register(EnterItem)
admin.site.register(OutItem)