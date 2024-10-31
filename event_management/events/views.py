from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, EventForm
from .models import Event, Booking
from django.contrib import messages

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Event List and Search View (Homepage)
def event_list(request):
    events = Event.objects.all()
    query = request.GET.get('q')
    if query:
        events = events.filter(name__icontains=query)
    return render(request, 'event_list.html', {'events': events})

# Create Event
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

# Book Event
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Booking.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "You have already booked this event.")
    elif Booking.objects.filter(event=event).count() >= event.booking_limit:
        messages.warning(request, "This event is fully booked.")
    else:
        Booking.objects.create(event=event, user=request.user)
        messages.success(request, "Event booked successfully.")
    return redirect('home')

# View Booked Events
@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booked_events.html', {'bookings': bookings})

