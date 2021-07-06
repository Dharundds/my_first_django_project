from django import forms
from django.forms import ModelForm, widgets
from .models  import Venue,Event

# Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name','address','pincode','phone','web','email_address')
        labels ={
             'name': "",
            'address': "",
            'pincode':"",
            'phone':"",
            'web':"",
            'email_address':"",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Address'}),
            'pincode':forms.TextInput(attrs={'class':'form-control','placeholder':'Pincode'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number if any'}),
            'web':forms.TextInput(attrs={'class':'form-control','placeholder':'Website if any'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address if any'}),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','manager','attendees','description')
        labels ={
            'name': "",
            'event_date': "YYYY-MM-DD HH:MM:SS",
            'venue':"Venue",
            'manager':"Manager",
            'attendees':"Attendees",
            'description':"",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control','placeholder':'Event date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Event venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'Event Manager'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Event attendee '}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Event description if any'}),

        }
