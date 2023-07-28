from Main.models import Event, Ticket
from django.http import JsonResponse
from django.contrib.auth import get_user_model as User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf
from django.contrib.auth import authenticate, login, logout
from Users.models import CustomUser
from .forms import NewUserForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from ERAS.configs import *
from django.shortcuts import get_object_or_404
from datetime import date
from django.conf import settings


# Create your views here.
@csrf.csrf_exempt
def api_register(request):
    if request.user.is_authenticated:
        if not request.user.has_perm('event.organizer'):
            return JsonResponse({"Error":"You Are Already Logged in!"},)
        else:
            return JsonResponse({"Info":"You Are Already Logged in!"},)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Account Activation Request'
            message = render_to_string('email_template.html', {
                'heading': Email_Heading(user),
                'message': f'{HOSTNAME}/activate/{user.secret_id}',
            })
            from_email = EMAIL_SENDER
            recipient_list = [Email_Recipient(user),]

            send_mail(subject, None, from_email, recipient_list, html_message=message)
            login(request, user)
            if user.role == User().Attendee:
                return JsonResponse({"Info":"Registration Successful. \nPlease Go to Your Email to Activate Your Account."})        
            else:
                return JsonResponse({"Info":"Registration Successful. \nPlease Wait for Your Account to be Activated."})        
        elif form.has_error:
            errors = form.errors.get_json_data()
            return JsonResponse(errors, safe=False)
        return JsonResponse({"Error":"Unsuccessful registration. Invalid information."})
    else:
        return JsonResponse({"Error":"Method Not Allowed!"})
    
def Email_Heading(user):
    if user.role == User().Attendee:
        return f"Hello {user.username},\nPlease Activate Your Account by Clicking the Link bellow"
    else:
        return f'{user.username} is Requesting for You to Activate his Account'
    
def Email_Recipient(user):
    if user.role == User().Attendee:
        return user.email
    else:
        
        return EMAIL_RECIEVER_ADMIN
    
@csrf.csrf_exempt
def api_login(request):
    if request.user.is_authenticated:
        if request.user.role == User().Attendee or request.user.role == User().Event_Staff:
            json = {"Info":"Success",
                    "User":{
                        "Username":request.user.username,
                        "Secret_ID":request.user.secret_id,
                        "Email":request.user.email,
                        "Role":request.user.role
                    }}
            return JsonResponse(json)
        else:
            return JsonResponse({"Error":"You Are not Allowed Here!"},)
    if request.method == "POST":
        try:
            
            username = request.POST["username"]
            password = request.POST["password"]
        except json.JSONDecodeError:
            return JsonResponse({"Error":"Bad Request!"},)
        except MultiValueDictKeyError:
            return JsonResponse({"Error":"DicktKeyError!"},)
        try:
            user = User().objects.get(username=username)
        except:
            return JsonResponse({"Error":"Wrong Credentials!"})  
        if user.role == User().Organizer:
            return JsonResponse({"Error":"Forbidden"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            json = {"Info":"Success",
                    "User":{
                        "Username":user.username,
                        "Secret_ID":user.secret_id,
                        "Email":user.email,
                        "Role":user.role
                    }}
            return JsonResponse(json, status=200)
        return JsonResponse({"Error":"Wrong Credentials!"})   
    else:
        return JsonResponse({"Error":"Method Not Allowed!"},)

@csrf.csrf_exempt
@login_required(redirect_field_name='/')
def api_logout(request):
    if request.user.role == User().Attendee or request.user.role == User().Event_Staff:
        logout(request)
        return JsonResponse({"Info":"Logout Successful"}, status=200)
    return JsonResponse({"Error":"You Are not Allowed Here!"},)

@csrf.csrf_exempt
@login_required(redirect_field_name='/')      
def CreateTicketAPI(request, event_id,):
    if not request.user.role == User().Attendee and not request.user.role == User().Event_Staff:
        return JsonResponse({"Error":"You Are not Allowed Here!"},)
    if request.method == "POST":
        try:
            E = Event.objects.get(event_id=event_id)
        except:
            return JsonResponse({"Error":"Bad Request"},)
        valid = Ticket.objects.filter(user_id=request.user.id, Event_id= E.id)
        if (valid.count() > 0):
            return JsonResponse({"Error":"You Have A Ticket Already!"})
        T = Ticket()
        T.user = CustomUser.objects.get(id=request.user.id)
        T.Event = E
        T.save()
        return  JsonResponse({"Info":"Success",}, content_type="application/json", safe=False)
    else:
        return JsonResponse({"Error":"Bad Request"},)
                
@login_required(redirect_field_name='/')
def get_tickets(request):
    if request.user.role == User().Attendee or request.user.role == User().Event_Staff:
        if request.method == "GET":
            tickets = []
            query = Ticket.objects.filter(user_id = request.user.id)
            today = date.today()
            for ticket in query:
                if ticket.expiry_date >= today:
                    tickets.append({"User":ticket.user.username,
                                    "Serial":ticket.ticket_id,
                                    "QR-Code":ticket.qr_code.url,
                                    "Expiry":ticket.expiry_date,
                                    "Attended":ticket.attended,
                                    "Event":{"Title":ticket.Event.title,
                                            "location":ticket.Event.location,
                                            "Start_Date":ticket.Event.eventstartdate,
                                            "End_Date":ticket.Event.eventenddate,
                                            "Start_Time":datetime.strptime(str(ticket.Event.starttime)[:-3], "%H:%M").strftime("%I:%M %p"),
                                            "End_Time":datetime.strptime(str(ticket.Event.endtime)[:-3], "%H:%M").strftime("%I:%M %p")}})
            return JsonResponse(tickets, safe=False)
        return JsonResponse({"Error":"Method Not Allowed!"},)
    return JsonResponse({"Error":"You Are not Allowed Here!"},)

@csrf.csrf_exempt
@login_required(redirect_field_name='/')
def record_Attendance(request,):
    if request.user.role == User().Event_Staff:
        try:
            ticket_id = request.POST["ticket_id"]
        except MultiValueDictKeyError:
            return JsonResponse({"Error":"DicktKeyError!"},)
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
        ESS = ticket.Event.staff
        ESL = eval(ESS)
        if request.user.secret_id in ESL:
            if not ticket.attended:
                ticket.attended = True
                ticket.save()
                return JsonResponse({"Success":"Success"})
            return JsonResponse({"Success":"Success"})
        return JsonResponse({"Error":"You Are Not Staff in This Event,\nPlease Contact Event Organizer First."})
    return JsonResponse({"Error":"Forbidden"})