from django.contrib import admin
from .models import User, Category, Listing, Bidding, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bidding)
admin.site.register(Bid)
