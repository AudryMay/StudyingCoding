from django.contrib import admin
from .models import *

# Register your models here.
# Run: python manage.py makemigrations auctions
# Followed by: python manage.py migrate auctions
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bids)
