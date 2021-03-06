from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

# third party
from multiselectfield import MultiSelectField

from ams.utils import get_random_string_generator

from billing.models import BillingProfile


class State(models.Model):

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class City(models.Model):

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class BookingPurpose(models.Model):
    image = models.ImageField(upload_to='booking_purpose', blank=True)
    name = models.CharField(max_length=20)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.name.capitalize()


class VenueQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def booking_purpose_items(self, pk):
        return self.filter(booking_purpose=pk)


class VenueManager(models.Manager):
    def get_queryset(self):
        return VenueQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def booking_purpose_items(self, pk):
        return self.get_queryset().booking_purpose_items(pk)


class Venue(models.Model):

    BOOKING_TYPE = (
        ('full_day', 'Full Day'),
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
    )

    # Model Field
    name = models.CharField(max_length=250)
    seating_capacity = models.PositiveIntegerField()
    standing_capacity = models.PositiveIntegerField()
    address = models.CharField(max_length=300)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.PositiveIntegerField()
    booking_type = MultiSelectField(choices=BOOKING_TYPE)
    booking_purpose = models.ManyToManyField(BookingPurpose)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, help_text='This price for per day')

    is_active = models.BooleanField(default=True)
    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue:venueDetailUrl', kwargs={'pk': self.pk})
