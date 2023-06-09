import os
import uuid
from django.http import JsonResponse
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Event, Photo
from django import forms
from django.contrib.auth.forms import AuthenticationForm



from django.shortcuts import redirect
def events_all(request):
    events = Event.objects.all().order_by('-event_date_time')
    return render(request, 'home.html', {'events': events})

def login_redirect(request):
    return redirect('path/to/your/styled/login.html')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'type', 'description', 'location', 'event_date_time', 'capacity', 'restrictions', 'notes', 'zipcode']
        widgets = {
            'event_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

from django.contrib.auth.mixins import UserPassesTestMixin

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def get_queryset(self):
        """Only let the user update their own events unless they are an admin."""
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def test_func(self):
        """Only allow the event owner or an admin to update the event."""
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser

class EventDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'

    def get_queryset(self):
        """Only let the user delete their own events unless they are an admin."""
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def test_func(self):
        """Only allow the event owner or an admin to delete the event."""
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser


from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

@csrf_exempt
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'redirect': '/'})
    
    return JsonResponse({'error': 'Invalid request'})



def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', { 'event': event })

def index(request):
    return HttpResponse("Hello, world. You're at the main_app index.")

# def events_index(request):
#     return render(request, 'events/index.html', {
#         'events': events
#     })

def events_by_type(request, type):
    events = Event.objects.filter(type=type)
    return render(request, 'home.html', {'events': events})


def login_view(request):
    error_message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the actual URL name or path of your home page
        else:
            error_message = 'Invalid username or password'
    else:
        form = AuthenticationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'nightowl/login.html', context)

@login_required
def add_photo(request, event_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try: 
            bucket = os.environ['S3_BUCKET_NAME']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            event = Event.objects.get(id=event_id)
            event.photo_url = url
            event.save()
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', event_id=event_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'nightowl/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('signup')



@login_required
def profile(request):
    return render(request, 'nightowl/profile.html', {'user': request.user})

@login_required(login_url='/signup')
def home(request):
    events = Event.objects.all().order_by('-event_date_time')
    print('events', events)
    return render(request, 'home.html', { 'events': events })

