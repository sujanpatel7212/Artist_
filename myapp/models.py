from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.name

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	password=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100,default="customer")

	def __str__(self):
		return self.fname


class Profile(models.Model):
	CHOICE1=(
			('singer','singer'),
			('musician','musician'),
			('painter','painter'),
			('dancer','dancer'),
		)
	CHOICE2=(
			('Michael Jackson','Michael Jackson'),
			('Arijit Singh','Arijit Singh'),
			('Justin Bieber','Justin Bieber'),
			('Guru Randhava','Guru Randhava'),
			('Zakir Hussain','Zakir Hussain'),
			('Amjad Ali Khan','Amjad Ali Khan'),
			('Shipla Gupta','Shipla Gupta'),
			('Paresh Maity','Paresh Maity'),
			('Parbhu Deva','Parbhu Deva'),
		)
	artist_artist=models.ForeignKey(User,on_delete=models.CASCADE)
	artist_type=models.CharField(max_length=100,choices=CHOICE1)
	artist_name=models.CharField(max_length=100,choices=CHOICE2)
	artist_desc=models.TextField()
	artist_image=models.ImageField(upload_to="artist_image/")
	artist_price=models.PositiveIntegerField()
	'''
	artist_performance_desc=models.TextField()
	artist_performance_image=models.ImageField(upload_to="artist_performance_image/")
	'''

	def __str__(self):
		return self.artist_artist.fname+" - "+self.artist_type+" - "+self.artist_name



class Book_artist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
	artist_type=models.CharField(max_length=100,blank=True,null=True)
	artist_name=models.CharField(max_length=100,blank=True,null=True)
	event_name=models.CharField(max_length=100,blank=True,null=True)
	event_date=models.DateField(blank=True,null=True)
	event_start_time=models.TimeField(blank=True,null=True)
	event_end_time=models.TimeField(blank=True,null=True)
	event_venue=models.TextField(blank=True,null=True)
	remarks=models.TextField(blank=True,null=True)
	booking_date=models.DateTimeField(default=timezone.now)
	status=models.CharField(max_length=100,default="pending")
	payment_status=models.CharField(max_length=100,default="Not Paid")

	def __str__(self):
		return self.user.fname+" - "+self.profile.artist_name

class Artist_payment(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
	aritst_price=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField()

	def __str__(self):
		return self.user.fname



class TransactionPayment(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE,blank=True,null=True)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)		