from datetime import date
from django import forms
from django.contrib.auth.models import User

# Create your forms here.

class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class NewUserForm(forms.Form):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CreateNewEvent(forms.Form):
    title = forms.CharField(max_length=20,help_text="# event title")
    location = forms.CharField(max_length=200, help_text="# event location (200 Charecters)")
    description = forms.CharField(max_length=200, required=False, help_text="# Event Description (200 Charecters)")
    eventstartdate = forms.DateField(label="Event Start Date", widget=DateInput(attrs={'type': 'date'}))
    eventenddate = forms.DateField(label="Event End Date", widget=DateInput(attrs={'type': 'date'}))
    starttime = forms.TimeField(label="Start Time", widget=forms.TimeInput(attrs={'type': 'time'}), help_text="# start time of the event")
    endtime = forms.TimeField(label="End Time", widget=forms.TimeInput(attrs={'type': 'time'}), help_text="# end time  of the event")
    
    def clean(self):
        super(CreateNewEvent, self).clean()
        
        Event_Start_Date = self.cleaned_data["eventstartdate"]
        Event_End_Date = self.cleaned_data["eventenddate"]
        Start_Time = self.cleaned_data["starttime"]
        End_Time = self.cleaned_data["endtime"]
        
        if Event_Start_Date <= date.today():
            self._errors['eventstartdate'] = self.error_class([
                'Event Start Date Can\'t be Lower Than or Equal to Today'])
            
        if Event_End_Date <= date.today():
            self._errors['eventenddate'] = self.error_class([
                'Event End Date Can\'t be Lower Than or Equal to Today'])
            
        if Event_Start_Date >= Event_End_Date:
            self._errors['eventstartdate'] = self.error_class([
                'Event Start Date Can\'t Equal or be Heigher Than Event End Date'])
            
        if Start_Time >= End_Time:
            self._errors['starttime'] = self.error_class([
                'Start Time Can\'t Equal or be Heigher Than End Time'])
            
        return self.cleaned_data
    
   
      
class AddEventStaff(forms.Form):
    secret_id = forms.CharField(label="User ID", help_text="User Account ID", max_length=10)
    
class CreateNewTicket(forms.Form):
    attended = forms.BooleanField(label="Attended", initial=False, help_text="if the user has attended the Event", required=False)
