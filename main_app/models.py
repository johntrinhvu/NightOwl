from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    EVENT_TYPES = [
        ('Party', 'Party'),
        ('Game', 'Game'),
        ('Club', 'Club'),
        ('House Party', 'House Party'),
        ('Bar', 'Bar'),
    ]
    zipcode_validator = RegexValidator(
        regex=r'^\d{5}(?:-\d{4})?$',
        message="Enter a valid zipcode."
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=EVENT_TYPES, default='Party')
    description = models.TextField(max_length=250)
    event_date_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    restrictions = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    photo_url = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=10, validators=[zipcode_validator])


    def __str__(self):
        return f'{self.name} ({ self.id })'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})


    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment {self.id} by {self.user.username}'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"
