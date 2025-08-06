from django.db import models

from authentication_app.models import User

# Create your models here.
class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    area_of_control = models.CharField(max_length=255)
    reports_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Officer: {self.user.username}"
    
class OfficerRating(models.Model):
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='ratings')
    complaint = models.ForeignKey('complaints.Complaint', on_delete=models.CASCADE, unique=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.officer.user.username} - {self.rating}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        ratings = OfficerRating.objects.filter(officer=self.officer)
        average = sum(r.rating for r in ratings) / ratings.count() if ratings.exists() else 0.0
        
        self.officer.average_rating = average
        self.officer.save()
