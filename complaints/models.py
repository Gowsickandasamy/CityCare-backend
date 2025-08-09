from django.db import models
from authentication_app.models import User
from officers.models import Officer

class Complaint(models.Model):
    STATUS = [
        ('PENDING', 'Pending'),
        ('WORK_ON_PROGRESS', 'Work on progress'),
        ('RESOLVED', 'Resolved')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_complaints')
    officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='officer_complaints')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_complaints', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    area_name = models.CharField(max_length=255)
    location_link = models.URLField()
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='PENDING')

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.title}"
