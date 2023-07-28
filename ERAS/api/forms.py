from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model as User



CHOICES =(
    ("organizer", "Organizer"),
    ("attendee", "Attendee"),
)

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	account_type = forms.ChoiceField(choices=CHOICES)


	class Meta:
		model = User()
		fields = ("username", "first_name", "last_name", "email", "password1", "password2",)

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')

		if User().objects.filter(email=email).exists():
			msg = 'A user with that email already exists.'
			self.add_error('email', msg)           
    
		return self.cleaned_data

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		if self.cleaned_data['account_type'] == "organizer":
			user.role = User().Organizer
		elif self.cleaned_data['account_type'] == "attendee":
			user.role = User().Attendee
		user.is_active = False
		if commit:
			user.save()
		return user