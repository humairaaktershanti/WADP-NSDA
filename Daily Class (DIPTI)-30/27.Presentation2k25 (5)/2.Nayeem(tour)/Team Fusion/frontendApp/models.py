from django.db import models
from backendApp.models import Package,Tour,GuideProfile,TravelerProfileModel



class Booking(models.Model):
    traveler = models.ForeignKey(TravelerProfileModel, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    guide = models.ForeignKey(GuideProfile, on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    num_persons = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        if self.tour:
            price_per_person = self.tour.offer_price or self.tour.regular_price
            days = self.tour.duration_days or 1
            return price_per_person * days * self.num_persons

        elif self.package:
            return self.package.offer_price or self.package.package_price

        elif self.guide:
            days = 1
            if self.end_date:
                days = (self.end_date - self.start_date).days + 1
            return (self.guide.price_per_day or 0) * days * self.num_persons

        return 0

    def __str__(self):
        if self.tour:
            return f"Booking by {self.traveler} for Tour: {self.tour.title}"
        if self.package:
            return f"Booking by {self.traveler} for Package: {self.package.name}"
        if self.guide:
            return f"Booking by {self.traveler} for Guide: {self.guide.full_name}"
        return f"Booking by {self.traveler}"
