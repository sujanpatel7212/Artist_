from django.contrib import admin
from .models import Contact,User,Profile,Book_artist,TransactionPayment
# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Book_artist)
admin.site.register(TransactionPayment)

