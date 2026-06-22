from django.db import models
from django.contrib.auth.models import User

# 1. The Football Turf (The Venue)
class Turf(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255) # e.g., Mira Road, Dahisar
    price_per_hour = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='turf_images/') 
    description = models.TextField()

    def __str__(self):
        return self.name

# 2. The Booking (When someone reserves a spot)
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bookings")
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    start_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.turf.name} ({self.date})"

# 3. The Match (The "Open Game" layer)
class Match(models.Model):
    # This links a match directly to a booking
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="match")
    title = models.CharField(max_length=100, default="Friendly Match")
    required_players = models.IntegerField(default=10)
    # This allows many users to join one match
    players = models.ManyToManyField(User, related_name="joined_matches", blank=True)

    def __str__(self):
        return f"Match: {self.title} at {self.booking.turf.name}"