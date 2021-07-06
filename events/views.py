from django.http.response import HttpResponseRedirect,FileResponse,HttpResponse
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import date, datetime
from .models import Event,Venue
from .forms import VenueForm,EventForm
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator

def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    # Convert month from name to number
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    # creating calendar
    cal =HTMLCalendar().formatmonth(year,month_number)
    #Get current year
    now  = datetime.now()
    curr_yr = now.year

    return render(request,'events/home.html',{
        "title":"Home",
        "year":year,
        "month":month,
        "mon_num":month_number,
        "cal":cal,
        "curr_yr":curr_yr
        })

def all_events(request):
    event_list= Event.objects.all().order_by('event_date')
    return render(request,'events/event_list.html',{'event_list':event_list})

def add_venue(request):
    submitted  =False
    if request.method=="POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'events/add_venue.html',{'form':form,'submitted':submitted})
 

def list_venues(request):
    # venue_list= Venue.objects.all()
    p = Paginator(Venue.objects.all(),2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums =  'a'*venues.paginator.num_pages
    return render(request,'events/venue.html',{'venues':venues,'nums':nums})

def show_venue(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request,'events/show_venue.html',{'venue':venue})

def search_venues(request):
    if request.method =="POST":
        search  = request.POST.get('searched')
        venues = Venue.objects.filter(name__contains = search)
        return render(request,'events/search_venues.html',{'search':search,'venues':venues})
    else:
        return render(request,'events/search_venues.html',{})

def update_venue(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    return render(request,'events/update_venue.html',{'venue':venue,'form':form})

def add_event(request):
    submitted  =False
    if request.method=="POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'events/add_event.html',{'form':form,'submitted':submitted})

def update_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None,instance=event)
    if form.is_valid():
        form.save()
        return redirect('all_events')
    return render(request,'events/update_event.html',{'event':event,'form':form})

# delete Event
def delete_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('all_events')

# delete venue
def delete_venue(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')

# Generate Text file venue list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    lines =[]
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.pincode}\n{venue.phone}\n{venue.web}\n{venue.email_address}')
    # lines = ["\nThis is line 1",
    # "This is line 2\n",
    # "This is line 3\n"]
    # print(lines)
    # #write to txt file
    response.writelines(lines)
    return response

# Generate csv file venue list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    #create a csv writer
    writer = csv.writer(response)
    venues = Venue.objects.all()
    #add column headings to csv files
    writer.writerow(['Venue Name','Address','Pincode','Phone','Web address','Email Address'])
    
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.pincode,venue.phone,venue.web,venue.email_address])
    
    return response

def venue_pdf(request):
    #create Bytestream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    venues = Venue.objects.all()
    lines =[]
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.pincode)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='venues.pdf')