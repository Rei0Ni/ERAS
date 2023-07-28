from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model as User
from django.contrib.auth.forms import UserCreationForm
from Main.variables import HostName
from .forms import NewUserForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Account Activation Request'
            message = render_to_string('email_template.html', {
                'heading': Email_Heading(user),
                'message': f'{HostName}/activate/{user.secret_id}',
            })
            from_email = 'abdelrahman.hamdy.hashim@gmail.com'
            recipient_list = [Email_Recipient(user),]

            send_mail(subject, None, from_email, recipient_list, html_message=message)
            login(request, user)
            if user.role == User().Attendee:
                messages.success(request, "Registration successful.\nPlease Go to Your Email to Activate Your Account")
            else:
                messages.success(request, "Registration successful.\nPlease Wait for Your Account to be Activated")
            return redirect("/")
        return render(request=request, template_name="Users/register.html", context={"form":form})
    else:
        form = NewUserForm()
        return render (request=request, template_name="Users/register.html", context={"form":form})

def ActivateUser(request, u):
    try:
        user = User().objects.get(secret_id = u)
    except:
        messages.error(request, "User was not found!")
        return redirect('/')
    if user.role == User().Attendee:
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, f"Hey {user.username} Your Account is now Activated")
            return redirect('/')
        messages.info(request, 'User is Already Activated')
        return redirect('/')
    elif user.role == User().Organizer or user.role == User().Event_Staff:
        messages.error(request, 'Please Contact the Site Admin to Activate your Account')
        return redirect('/')
    
def Email_Heading(user):
    if user.role == User().Attendee:
        return f"Hello {user.username}, \nPlease Activate Your Account by Clicking the Link bellow"
    else:
        return f'{user.username} is Requesting for You to Activate his Account'
    
def Email_Recipient(user):
    if user.role == User().Attendee:
        return user.email
    else:
        return "the.inspector.2000@gmail.com"