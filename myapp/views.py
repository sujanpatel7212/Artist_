from django.shortcuts import render,redirect
from .models import Contact,User,Profile,Book_artist,TransactionPayment
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from django.core.mail import send_mail

# Create your views here.

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def initiate_payment(request):
	user=User.objects.get(email=request.session['email'])
	try:         
		amount = int(request.POST['amount'])
	except:
	 	return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = TransactionPayment.objects.create(made_by=user,amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY

	params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
        )
	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)
	transaction.checksum = checksum
	transaction.save()
	book_artist=Book_artist.objects.filter(user=user,status="accepted",payment_status="Not Paid")
	for i in book_artist:
		i.payment_status="paid"
		i.save()
	paytm_params['CHECKSUMHASH'] = checksum

	print('SENT: ', checksum)
	return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)
	

def index(request):
	return render(request,'index.html')

def about(request):
	profiles=Profile.objects.all()
	return render(request,'about.html',{'profiles':profiles})

def artist(request):
	profiles=Profile.objects.all()
	all=len(profiles)
	singer=len(Profile.objects.filter(artist_type="singer"))
	musician=len(Profile.objects.filter(artist_type="musician"))
	painter=len(Profile.objects.filter(artist_type="painter"))
	dancer=len(Profile.objects.filter(artist_type="dancer"))
	return render(request,'artist.html',{'all':all,'profiles':profiles,'singer':singer,'musician':musician,'painter':painter,'dancer':dancer})


def artist_singer(request):
	profiles=Profile.objects.all()
	all=len(profiles)
	profiles=Profile.objects.filter(artist_type="singer")
	singer=len(Profile.objects.filter(artist_type="singer"))
	musician=len(Profile.objects.filter(artist_type="musician"))
	painter=len(Profile.objects.filter(artist_type="painter"))
	dancer=len(Profile.objects.filter(artist_type="dancer"))
	return render(request,'artist.html',{'all':all,'profiles':profiles,'singer':singer,'musician':musician,'painter':painter,'dancer':dancer})

def artist_painter(request):
	profiles=Profile.objects.all()
	all=len(profiles)
	profiles=Profile.objects.filter(artist_type="painter")
	singer=len(Profile.objects.filter(artist_type="singer"))
	musician=len(Profile.objects.filter(artist_type="musician"))
	painter=len(Profile.objects.filter(artist_type="painter"))
	dancer=len(Profile.objects.filter(artist_type="dancer"))
	return render(request,'artist.html',{'all':all,'profiles':profiles,'singer':singer,'musician':musician,'painter':painter,'dancer':dancer})

def artist_musician(request):
	profiles=Profile.objects.all()
	all=len(profiles)
	profiles=Profile.objects.filter(artist_type="musician")
	singer=len(Profile.objects.filter(artist_type="singer"))
	musician=len(Profile.objects.filter(artist_type="musician"))
	painter=len(Profile.objects.filter(artist_type="painter"))
	dancer=len(Profile.objects.filter(artist_type="dancer"))
	return render(request,'artist.html',{'all':all,'profiles':profiles,'singer':singer,'musician':musician,'painter':painter,'dancer':dancer})

def artist_dancer(request):
	profiles=Profile.objects.all()
	all=len(profiles)
	profiles=Profile.objects.filter(artist_type="dancer")
	singer=len(Profile.objects.filter(artist_type="singer"))
	musician=len(Profile.objects.filter(artist_type="musician"))
	painter=len(Profile.objects.filter(artist_type="painter"))
	dancer=len(Profile.objects.filter(artist_type="dancer"))
	return render(request,'artist.html',{'all':all,'profiles':profiles,'singer':singer,'musician':musician,'painter':painter,'dancer':dancer})


def blog(request):
	return render(request,'blog.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			message=request.POST['message'],)			
		msg="Contact Saved Succesfully"
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def elements(request):
	return render(request,'elements.html')

def single_blog(request):
	return render(request,'single-blog.html')

def track(request):
	return render(request,'track.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg' :msg})
		except: 
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					usertype=request.POST['usertype'],
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],)			
				msg="User Signup Succesfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password and confirm password does not matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password']
				)
			if user.usertype=="customer":
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'artist_index.html')				
		except Exception as e:
			print(e)
			msg="Email or Password is incorrect"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html') 

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=="customer":
		if request.method=="POST":
			user.usertype=request.POST['usertype']
			user.fname=request.POST['fname']
			user.lname=request.POST['lname']
			user.email=request.POST['email']
			user.mobile=request.POST['mobile']
			user.address=request.POST['address']
			user.save()
			msg="User Update Succesfully"
			return render(request,'profile.html',{'msg' :msg, 'user':user})	
		else:
			return render(request,'profile.html',{'user':user})
	else:
		if request.method=="POST":
			user.usertype=request.POST['usertype']
			user.fname=request.POST['fname']
			user.lname=request.POST['lname']
			user.email=request.POST['email']
			user.mobile=request.POST['mobile']
			user.address=request.POST['address']
			user.save()
			msg="User Update Succesfully"
			return render(request,'artist_profile.html',{'msg' :msg, 'user':user})	
		else:
			return render(request,'artist_profile.html',{'user':user})			

		
		
def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=="customer":
		if request.method=="POST":			 
			 if user.password==request.POST['old_password']:
			 	if request.POST['new_password']==request.POST['cnew_password']:
			 		user.password=request.POST['new_password']
			 		user.save()
			 		return redirect('logout')
			 	else:
			 		msg="New Password and Confirm New Password does not matched"
			 		return render(request,'change_password.html',{'msg' :msg})
			 else:
			 	msg="Old password is incorrect"
			 	return render(request,'change_password.html',{'msg' :msg})
		else:
			return render(request,'change_password.html')
	else:
		if request.method=="POST":	 
			 if user.password==request.POST['old_password']:
			 	if request.POST['new_password']==request.POST['cnew_password']:
			 		user.password=request.POST['new_password']
			 		user.save()
			 		return redirect('logout')
			 	else:
			 		msg="New Password and Confirm New Password does not matched"
			 		return render(request,'artist_change_password.html',{'msg' :msg})
			 else:
			 	msg="Old password is incorrect"
			 	return render(request,'artist_change_password.html',{'msg' :msg})
		else:
			return render(request,'artist_change_password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP for Forgot Password'
			message = 'Hello, '+user.fname+" Your OTP For Forget Password Is "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp,'email':user.email})
		except:
			msg="Email Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})			
	else:	
		return render(request,'forgot_password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']
	if otp==uotp:
		return render(request,'new_password.html',{'email':email})

	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})

def new_password(request):
	email=request.POST['email']
	p=request.POST['new_password']
	cp=request.POST['cnew_password']

	if p==cp:
		user=User.objects.get(email=email)
		user.password=p
		user.save()
		return redirect('login')
	else:
		msg="Password and Confirm Password Does Not Matched"
		return render(request,'new_password.html',{'email':email,'msg':msg})

def artist_index(request):
	return render(request,'artist_index.html')

def artist_add_profile(request):
	if request.method=="POST":
		artist_artist=User.objects.get(email=request.session['email'])
		Profile.objects.create(
			artist_artist=artist_artist,
			artist_type=request.POST['artist_type'],
			artist_name=request.POST['artist_name'],
			artist_desc=request.POST['artist_desc'],
			artist_price=request.POST['artist_price'],
			artist_image=request.FILES['artist_image'],
			)

		msg="Artist Added Succesfully"
		return render(request,'artist_add_profile.html',{'msg' :msg})
	else:
		return render(request,'artist_add_profile.html')

def artist_view_profile(request):
	artist_artist=User.objects.get(email=request.session['email'])
	profiles=Profile.objects.filter(artist_artist=artist_artist)
	return render(request,'artist_view_profile.html',{'profiles' :profiles})

def artist_edit_profile(request,pk):
	profile=Profile.objects.get(pk=pk)
	if request.method=="POST":
		profile.artist_type=request.POST['artist_type']
		profile.artist_name=request.POST['artist_name']
		profile.artist_desc=request.POST['artist_desc']
		profile.artist_price=request.POST['artist_price']
		try:
			profile.artist_image=request.FILES['artist_image']
		except:
			pass
		profile.save()	
		return render(request,'artist_edit_profile.html',{'profile' :profile})	
	else:
		return render(request,'artist_edit_profile.html',{'profile' :profile})


def artist_delete_profile(request,pk):
	profile=Profile.objects.get(pk=pk)
	profile.delete()
	return redirect('artist_view_profile')


def artist_detail(request,pk):
	profile=Profile.objects.get(pk=pk)
	return render(request,'artist_detail.html',{'profile' :profile})

def book_artist(request,pk):
	profile=Profile.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Book_artist.objects.create(
			user=user,
			profile=profile,
			artist_type=request.POST['artist_type'],
			artist_name=request.POST['artist_name'],
			event_name=request.POST['event_name'],
			event_date=request.POST['event_date'],
			event_start_time=request.POST['event_start_time'],
			event_end_time=request.POST['event_end_time'],
			event_venue=request.POST['event_venue'],
			remarks=request.POST['remarks'],
			)
		msg="Booking request sent Succesfully"
		booking=Book_artist.objects.filter(user=user)
		print(booking)
		return render(request,'customer_pending_booking.html',{'booking':booking})
	else:
		return render(request,'book_artist.html',{'profile':profile})

def view_booking(request):
	user=User.objects.get(email=request.session['email'])
	booking=Book_artist.objects.filter(user=user)
	return render(request,'view_booking.html',{'booking':booking})

def bookings(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	print("Profile : ",profile[0].artist_artist)
	booking=Book_artist.objects.all()
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	
	return render(request,'bookings.html',{'booking':book_artist})

def accept_booking(request,pk):
	booking=Book_artist.objects.get(pk=pk)
	booking.status="accepted"
	booking.save()
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	booking=Book_artist.objects.filter(status="accepted")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	return render(request,'accepted_booking.html',{'booking':book_artist})

def reject_booking(request,pk):
	booking=Book_artist.objects.get(pk=pk)
	booking.status="rejected"
	booking.save()
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	booking=Book_artist.objects.filter(status="rejected")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	return render(request,'rejected_booking.html',{'booking':book_artist})

def pending_booking(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)	
	booking=Book_artist.objects.filter(status="pending")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)	
	return render(request,'pending_booking.html',{'booking':book_artist})


def confirmed_booking(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)	
	booking=Book_artist.objects.filter(payment_status="paid")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)	
	return render(request,'confirmed_booking.html',{'booking':book_artist})


def accepted_booking(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	booking=Book_artist.objects.filter(status="accepted")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	return render(request,'accepted_booking.html',{'booking':book_artist})

def rejected_booking(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	booking=Book_artist.objects.filter(status="rejected")
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	return render(request,'rejected_booking.html',{'booking':book_artist})


def customer_pending_booking(request):
	user=User.objects.get(email=request.session['email'])	
	booking=Book_artist.objects.filter(user=user, status="pending")	
	return render(request,'customer_pending_booking.html',{'booking':booking})

def customer_accepted_booking(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])	
	booking=Book_artist.objects.filter(user=user, status="accepted", payment_status="Not Paid")	
	for i in booking:
		net_price=net_price+i.profile.artist_price

	return render(request,'customer_accepted_booking.html',{'booking':booking,'net_price':net_price})

def customer_rejected_booking(request):
	user=User.objects.get(email=request.session['email'])	
	booking=Book_artist.objects.filter(user=user, status="rejected")	
	return render(request,'customer_rejected_booking.html',{'booking':booking})

def customer_confirmed_booking(request):
	user=User.objects.get(email=request.session['email'])	
	booking=Book_artist.objects.filter(user=user, payment_status="paid")	
	return render(request,'customer_confirmed_booking.html',{'booking':booking})

def all_bookings(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)
	print("Profile : ",profile[0].artist_artist)
	booking=Book_artist.objects.all()
	book_artist=[]
	for i in booking:
		if i.profile.artist_artist==profile[0].artist_artist:
			book_artist.append(i)
	
	return render(request,'bookings.html',{'booking':book_artist})		


def artist_payment(request):
	user=User.objects.get(email=request.session['email'])
	profile=Profile.objects.filter(artist_artist=user)

def search(request):
	artist_artist=User.objects.get(email=request.session['email'])
	profiles=Profile.objects.filter(artist_artist=artist_artist,artist_name__contains=request.POST["search"])
	return render(request,'search.html',{'profiles':profiles})












			


