from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Booking, Turf, Match
import json
from django.http import JsonResponse
from datetime import datetime, time
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    # Get all turfs from the database
    all_turfs = Turf.objects.all()
    # Send them to the 'index.html' page
    return render(request, 'pitch_app/index.html', {
        'turfs': all_turfs
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # CHECK FOR 'next' PARAMETER
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'pitch_app/login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately after they sign up
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'pitch_app/register.html', {'form': form})

def turf_detail(request, turf_id):
    # Try to find the turf by ID, or show a 404 error if it doesn't exist
    turf = get_object_or_404(Turf, pk=turf_id)
    return render(request, 'pitch_app/turf_detail.html', {
        'turf': turf 
    })

def check_availability(request):
    turf_id = request.GET.get('turf_id')
    selected_date = request.GET.get('date')
    
    if not selected_date:
        return JsonResponse({'slots': []})

    # Get bookings and strip them down to just HH:MM
    existing_bookings = Booking.objects.filter(
        turf_id=turf_id, 
        date=selected_date
    )
    
    # We use .strftime('%H:%M') to ensure "07:00:00" becomes "07:00"
    booked_strings = [b.start_time.strftime('%H:%M') for b in existing_bookings]
    
    available_slots = []
    for hour in range(7, 23):
        slot_time = f"{hour:02d}:00"
        # Now the comparison will be "07:00" == "07:00"
        is_booked = slot_time in booked_strings
        available_slots.append({'time': slot_time, 'booked': is_booked})
        
    return JsonResponse({'slots': available_slots})

@login_required
def save_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        turf_id = data.get('turf_id')
        date = data.get('date')
        time_str = data.get('time')
        make_public = data.get('make_public', False)    

        # Create the booking
        turf = Turf.objects.get(id=turf_id)
        booking = Booking.objects.create(
            user=request.user,
            turf=turf,
            date=date,
            start_time=time_str
        )

        if make_public:
            Match.objects.create(
                booking=booking,
                required_players=10 
            )
        
        return JsonResponse({'status': 'success', 'booking_id': booking.id})
    
def match_list(request):
    # Only show matches that still need players 
    open_matches = Match.objects.all()
    return render(request, 'pitch_app/matches.html', {
        'matches': open_matches
    })

@login_required
def join_match(request, match_id):
    if request.method == "POST":
        match = get_object_or_404(Match, id=match_id)
        
        # Check if the match is already full
        if match.players.count() >= match.required_players:
            return JsonResponse({'status': 'error', 'message': 'Match is full!'})
            
        # Check if the user is already in the match
        if request.user in match.players.all():
            return JsonResponse({'status': 'error', 'message': 'You already joined!'})

        # Add the user to the Many-to-Many field
        match.players.add(request.user)
        
        return JsonResponse({
            'status': 'success', 
            'current_count': match.players.count()
        })

@login_required
def profile(request):
    # Get matches the user has joined
    joined_matches = request.user.joined_matches.all()
    # Get bookings the user has made
    my_bookings = request.user.my_bookings.all()
    
    return render(request, 'pitch_app/profile.html', {
        'joined_matches': joined_matches,
        'my_bookings': my_bookings
    })

def logout_view(request):
    logout(request)
    return redirect('index')