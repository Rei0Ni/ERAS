from django.shortcuts import render, redirect
from .forms import CreateNewEvent, CreateNewTicket, AddEventStaff
from .models import Event, Ticket
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404
from django.views.decorators import csrf
from django.http import JsonResponse
from datetime import date

# Create your views here.
def ticket_counter(Events, tickets):
    for event in Events:
            if tickets:
                tickets = tickets | event.ticket_set.all()
            else:
                tickets = event.ticket_set.all()
    return tickets

def page_not_found(request, exception):
    return render(request, "errors/404.html", {})

def home(request):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin/")
    return render(request, 'Main/home.html', {})
    
@login_required(redirect_field_name='/')
def dashboard(request):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        Events = request.user.event_set.all()
        paginator = Paginator(Events, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = CreateNewEvent()
        context = {
            "events":Events,
            "page_obj":page_obj,
            "form":form
        }
        return render(request, 'Main/Dashboard.html', context)
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def CreateEvent(request):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    
    if request.user.role == User().Organizer:
        if request.method == "POST":
            form = CreateNewEvent(request.POST)
            if form.is_valid():
                t = form.cleaned_data["title"]
                l = form.cleaned_data["location"]
                d = form.cleaned_data["description"]
                esd = form.cleaned_data["eventstartdate"]
                eed = form.cleaned_data["eventenddate"]
                st = form.cleaned_data["starttime"]
                et = form.cleaned_data["endtime"]
                request.user.event_set.create(title=t, location=l, description=d, eventstartdate=esd, eventenddate=eed, starttime=st, endtime=et)
                return redirect("/dashboard")
            for error in form.errors:
                messages.error(request, form.errors[error])
            return redirect("/dashboard")
        return redirect("/dashboard")
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def ViewEvent(request, id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        if get_object_or_404(Event, event_id=id).user_id == request.user.id:
            E = get_object_or_404(Event, event_id=id)
            T = Ticket.objects.filter(Event_id=E.id)
            attended = 0
            for ticket in T:
                if ticket.attended:
                    attended += 1
            Ticket_Form = CreateNewTicket()
            Staff_Form = AddEventStaff()
            data = {
                "Event": E,
                "Staff_List":eval(E.staff),
                "Ticket": T,
                "attended": attended,
                "Ticket_Form":Ticket_Form,
                "Staff_Form":Staff_Form
            }
            return render(request, 'Main/EventView.html', data)
        return redirect('/dashboard')
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')   
def UpdateEvent(request, id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:    
        if get_object_or_404(Event, event_id=id).user_id == request.user.id:
            if request.method == "POST":
                form = CreateNewEvent(request.POST)
                if form.is_valid():
                    if form.cleaned_data["eventstartdate"] >= form.cleaned_data["eventenddate"]:
                        messages.error(request, "Event Start Date Can't Equal or be Heigher Than Event End Date")
                        E = get_object_or_404(Event, event_id=id)
                        return render(request, 'Main/UpdateEvent.html', {"Event": E})
                    if form.cleaned_data["starttime"] >= form.cleaned_data["endtime"]:
                        messages.error(request, "Start Time Can't Equal or be Heigher Than End Time")
                        E = get_object_or_404(Event, event_id=id)
                        return render(request, 'Main/UpdateEvent.html', {"Event": E})
                    E = get_object_or_404(Event, event_id=id)
                    t = form.cleaned_data["title"]
                    E.title = t
                    l = form.cleaned_data["location"]
                    E.location = l
                    d = form.cleaned_data["description"]
                    E.description = d
                    esd = form.cleaned_data["eventstartdate"]
                    E.eventstartdate = esd
                    eed = form.cleaned_data["eventenddate"]
                    E.eventenddate = eed
                    st = form.cleaned_data["starttime"]
                    E.starttime = st
                    et = form.cleaned_data["endtime"]
                    E.endtime = et
                    E.qr_code.delete()
                    E.save()
                    return redirect("/dashboard/")
                return redirect('/')
            E = get_object_or_404(Event, event_id=id)
            
            return render(request, 'Main/UpdateEvent.html', {"Event": E})
        return redirect('/dashboard')
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def DeleteEvent(request, id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        if get_object_or_404(Event, event_id=id).user_id == request.user.id:
            if request.method == "GET":
                try:
                    E = get_object_or_404(Event, event_id=id)
                except:
                    messages.error(request, "Event Doesn't Exist!")
                    return redirect("/dashboard/")
                E.qr_code.delete()
                E.delete()
            return redirect("/dashboard/")
        return redirect("/dashboard")
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def CreateTicketUI(request, event_id,):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        try:
            E = Event.objects.get(event_id=event_id)
        except:
            return redirect("/dashboard")
        if E.user_id == request.user.id:
            if request.method == "POST":
                form = CreateNewTicket(request.POST)
                if form.is_valid():
                    attend = form.cleaned_data["attended"]
                    T = Ticket()
                    T.attended = attend
                    T.Event = E
                    T.user_id = request.user.id
                    T.save()
                    
                    return redirect(f"/event/{E.event_id}") 
            else:
                return redirect(f"/event/${E.event_id}")
        return redirect("/dashboard")
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def ViewTicket(request, event_id, ticket_id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        if get_object_or_404(Event, event_id=event_id).user_id == request.user.id:
            E = Event.objects.get(event_id=event_id)
            T = Ticket.objects.get(ticket_id=ticket_id)
            data = {
                "Event": E,
                "Ticket": T,
            }
            return render(request, 'Main/TicketView.html', data)
        return redirect('/dashboard')
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")

@login_required(redirect_field_name='/')
def AddStaffToEvent(request, event_id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        if get_object_or_404(Event, event_id=event_id).user_id == request.user.id:
            try:
                user_secret_id = request.POST['secret_id']
            except:
                return redirect(f"/event/{event_id}")
            E = Event.objects.get(event_id=event_id)
            staff_list = eval(E.staff)
            user = get_object_or_404(User(), secret_id=user_secret_id)
            if user_secret_id in staff_list:
                messages.info(request, "Staff Already Exists in This Event")
                messages.info(request, "User Was Staff in this Event Already.")
                return redirect(f"/event/{event_id}")
            else:
                if not user.role == User().Event_Staff:
                    user.role = User().Event_Staff
                    user.save()
                staff_list.append(user_secret_id)
                E.staff = str(staff_list)
                E.save()
                messages.success(request, "Staff Added Successfully.")
                return redirect(f'/event/{event_id}/')
    else:
        messages.error(request, "You should be an Organizer to access this location.")
        return redirect("/")

def RemoveEventStaff(request, event_id):
    if request.user.is_staff and request.user.is_superuser:
        return redirect("/admin")
    if request.user.role == User().Organizer:
        if get_object_or_404(Event, event_id=event_id).user_id == request.user.id:
            try:
                Staff_ID = request.POST['Staff_ID']
            except:
                return redirect(f"/event/{event_id}")
            E = Event.objects.get(event_id=event_id)
            staff_list = eval(E.staff)
            if Staff_ID in staff_list:
                staff_list.remove(Staff_ID)
                E.staff = str(staff_list)
                E.save()
                return JsonResponse({"status":"success"})
            return JsonResponse({"status":"Error"},)
        messages.error(request, "You Don't have Access To This Event.")
        return redirect(f"/event/{event_id}")
    messages.error(request, "You should be an Organizer to access this location.")
    return redirect("/")
            
            
