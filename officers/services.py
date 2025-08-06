from django.db import transaction
from django.forms import ValidationError

from authentication_app.models import User
from officers.models import Officer, OfficerRating

def create_officer(username, email, phone_number, area_of_control, created_by):
    with transaction.atomic():
        user = User.objects.create_user(
            username = username,
            email = email,
            phone_number = phone_number,
            password = "password",
            role = 'OFFICER'
        )
        
        officer = Officer.objects.create(
            user = user,
            area_of_control = area_of_control,
            reports_to = created_by
        )
        
        return officer
    
def get_all_officer(admin_id):
    with transaction.atomic():
        officers = Officer.objects.filter(reports_to = admin_id)
        return officers
    
def delete_officer(officer_id):
    with transaction.atomic():
        officer = User.objects.get(id=officer_id)
        officer.delete()
        

def create_review(officer, complaint, rated_by, rating, comment):
    with transaction.atomic():
        if not complaint.officer:
            raise ValidationError("Complaint must be assigned to an officer.")

        review = OfficerRating.objects.create(
            officer=officer,
            complaint=complaint,
            rating=rating,
            comment=comment,
            rated_by=rated_by
        )
        
        ratings = OfficerRating.objects.filter(officer=officer)
        average = sum(r.rating for r in ratings) / ratings.count() if ratings.exists() else 0.0

        officer.average_rating = average
        officer.save()
        
        return review
        
        