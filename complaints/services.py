from django.db import transaction

from officers.serializers import OfficerRatingSerializer
from .models import Complaint
from officers.models import Officer, OfficerRating
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def create_complaint(user, title, description, area_name, location_link, image=None):
    with transaction.atomic():
        officer = Officer.objects.filter(area_of_control=area_name).first()
        
        if officer is None:
            print(f"No officer found for area '{area_name}'")
            return {"error": f"No officer found for area '{area_name}'"}
        
        admin = officer.reports_to if officer.reports_to else None

        print(f"Creating complaint for officer: {officer}, User: {user}")

        complaint = Complaint.objects.create(
            user=user,
            officer=officer.user,
            admin=admin,
            title=title,
            description=description,
            area_name=area_name,
            location_link=location_link,
            image=image
        )
        
        print(f"Complaint created: {complaint}")
        return {"complaint": complaint}
    
def get_complaints(admin_id=None, officer_id=None, user_id=None):
    with transaction.atomic():
        complaints = None
        
        if admin_id:
            complaints = Complaint.objects.filter(admin_id=admin_id).select_related('user', 'officer', 'admin')
        elif officer_id:
            complaints = Complaint.objects.filter(officer_id=officer_id).select_related('user', 'officer', 'admin')
        elif user_id:
            complaints = Complaint.objects.filter(user_id=user_id).select_related('user', 'officer', 'admin')
        else:
            return "No Complaints"

        if not complaints.exists():
            return "No Complaints"
        
        # Prepare the result with usernames
        result = []
        for complaint in complaints:
            result.append({
                "id": complaint.id,
                "user": complaint.user.username if complaint.user else None,
                "officer": complaint.officer.username if complaint.officer else None,
                "admin": complaint.admin.username if complaint.admin else None,
                "title": complaint.title,
                "description": complaint.description,
                "area_name": complaint.area_name,
                "location_link": complaint.location_link,
                "created_at": complaint.created_at,
                "status": complaint.status,
                "image":getattr(complaint.image, 'url', None)
            })
        
        return result
    
def get_complaint(id):
    with transaction.atomic():
        complaint = Complaint.objects.filter(id=id).select_related('user', 'officer', 'admin').first()
        
        if complaint is None:
            return {"error": f"No Complaint found with id '{id}'"}
        
        return {
            "complaint": {
                "id": complaint.id,
                "user": complaint.user.username if complaint.user else None,
                "officer": complaint.officer.username if complaint.officer else None,
                "admin": complaint.admin.username if complaint.admin else None,
                "title": complaint.title,
                "description": complaint.description,
                "area_name": complaint.area_name,
                "location_link": complaint.location_link,
                "created_at": complaint.created_at,
                "status": complaint.status,
                "image": getattr(complaint.image, 'url', None),
            }
        }

        
def edit_complaint(id,user, title, description, area_name, location_link, image=None):
    with transaction.atomic():
        complaint = Complaint.objects.filter(id=id).first()
        
        if(complaint is None):
            return {"error": f"No Complaint found with id '{id}'"}
        
        officer = Officer.objects.filter(area_of_control=area_name).first()
        
        if officer is None:
            print(f"No officer found for area '{area_name}'")
            return {"error": f"No officer found for area '{area_name}'"}
        
        admin = officer.reports_to if officer.reports_to else None

        print(f"Creating complaint for officer: {officer}, User: {user}")

        complaint.user = user
        complaint.officer = officer.user
        complaint.admin = admin
        complaint.title = title
        complaint.description = description
        complaint.area_name = area_name
        complaint.location_link = location_link
        if image:
            complaint.image = image
        complaint.save() 

        print(f"Complaint updated: {complaint}")
        return {"complaint": complaint}
    

def current_complaints(admin_id=None, officer_id=None, user_id=None):
    with transaction.atomic():
        complaints = Complaint.objects.exclude(status="RESOLVED")

        if admin_id:
            complaints = complaints.filter(admin_id=admin_id)
        elif officer_id:
            complaints = complaints.filter(officer_id=officer_id)
        elif user_id:
            complaints = complaints.filter(user_id=user_id)
        else:
            return "No Complaints"

        if not complaints.exists():
            return "No Complaints"

        return [
            {
                "id": complaint.id,
                "user": complaint.user.username if complaint.user else None,
                "officer": complaint.officer.username if complaint.officer else None,
                "admin": complaint.admin.username if complaint.admin else None,
                "title": complaint.title,
                "description": complaint.description,
                "area_name": complaint.area_name,
                "location_link": complaint.location_link,
                "created_at": complaint.created_at,
                "status": complaint.status,
                "image":complaint.image.url if complaint.image else None,
            }
            for complaint in complaints
        ]
        

def resolved_complaints(admin_id=None, officer_id=None, user_id=None):
    with transaction.atomic():
        query = Q(status="RESOLVED")
        
        if admin_id:
            query &= Q(admin_id=admin_id)
        elif officer_id:
            query &= Q(officer_id=officer_id)
        elif user_id:
            query &= Q(user_id=user_id)
        else:
            return "No Complaints"

        complaints = Complaint.objects.filter(query).select_related('user', 'officer', 'admin')

        if not complaints.exists():
            return "No Complaints"

        return [
            {
                "id": complaint.id,
                "user": complaint.user.username if complaint.user else None,
                "officer": complaint.officer.username if complaint.officer else None,
                "admin": complaint.admin.username if complaint.admin else None,
                "title": complaint.title,
                "description": complaint.description,
                "area_name": complaint.area_name,
                "location_link": complaint.location_link,
                "created_at": complaint.created_at,
                "status": complaint.status,
                "image": getattr(complaint.image, 'url', None),
            }
            for complaint in complaints
        ]
    
def change_status(id, status):
    with transaction.atomic():
        complaint = Complaint.objects.filter(id=id).first()
        
        if(complaint is None):
            return {"error": f"No Complaint found with id '{id}'"}
        
        complaint.status = status
        complaint.save()
        return {'Success':'Status was changed'}
    
def delete_complaint(id):
    with transaction.atomic():
        complaint = Complaint.objects.filter(id=id).first()
        
        if(complaint is None):
            return {"error": f"No Complaint found with id '{id}'"}
        
        complaint.delete()
        return {'Success':'Complaint was changed'}


def detail_complaint(id):
    with transaction.atomic():
        complaint = Complaint.objects.filter(id=id).select_related('user', 'officer', 'admin').first()
        
        if complaint is None:
            return {"error": f"No Complaint found with id '{id}'"}

        officer_ratings = OfficerRating.objects.filter(complaint=complaint)
        ratings_data = OfficerRatingSerializer(officer_ratings, many=True).data

        return {
            "complaint": {
                "id": complaint.id,
                "user": complaint.user.username if complaint.user else None,
                "officer": complaint.officer.username if complaint.officer else None,
                "admin": complaint.admin.username if complaint.admin else None,
                "title": complaint.title,
                "description": complaint.description,
                "area_name": complaint.area_name,
                "location_link": complaint.location_link,
                "created_at": complaint.created_at,
                "status": complaint.status,
                "officer_ratings": ratings_data,
                "image": getattr(complaint.image, 'url', None),
            }
        }

    
def get_complaint_count(admin_id=None, officer_id=None, user_id=None):
    with transaction.atomic():
        filter_kwargs = {}

        if admin_id:
            filter_kwargs['admin_id'] = admin_id
        elif officer_id:
            filter_kwargs['officer_id'] = officer_id
        elif user_id:
            filter_kwargs['user_id'] = user_id
        else:
            return {
                "result": {
                    "total": 0,
                    "resolved": 0,
                    "pending": 0
                }
            }

        complaints = Complaint.objects.filter(**filter_kwargs).select_related('user', 'officer', 'admin')

        total = complaints.count()
        resolved = complaints.filter(status="RESOLVED").count()
        pending = complaints.filter(status="PENDING").count()

        return {
            
                "total": total,
                "resolved": resolved,
                "pending": pending
            
        }
