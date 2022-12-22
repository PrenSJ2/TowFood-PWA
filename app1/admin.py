import imp
from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Product)
admin.site.register(ProductOut)
admin.site.register(Member)
admin.site.register(Volunteer)
admin.site.register(Supplier)
admin.site.register(Larder)
admin.site.register(Update)
admin.site.register(Collection)
admin.site.register(Pickup)



