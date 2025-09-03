from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ComplaintCreateSerializer, ComplaintEditSerializer, ComplaintSerializer
from .services import change_status, create_complaint, current_complaints, delete_complaint, detail_complaint, edit_complaint, get_complaint, get_complaints, resolved_complaints, get_complaint_count
from .models import Complaint
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class ComplaintCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
        
    def post(self, request):
        serializer = ComplaintCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = create_complaint(
                user=request.user,
                title=data['title'],
                description=data['description'],
                area_name=data['area_name'],
                location_link=data['location_link'],
                image = request.FILES.get("image")
            )
            
            if 'error' in result:
                return Response({"error": result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Complaint created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ComplaintListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'ADMIN':
            complaints = Complaint.objects.filter(admin_id=user.id)
        elif user.role == 'OFFICER':
            complaints = Complaint.objects.filter(officer_id=user.id)
        elif user.role == 'USER':
            complaints = Complaint.objects.filter(user_id=user.id)
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_403_FORBIDDEN)

        if not complaints.exists():
            return Response({"message": "No Complaints found"}, status=status.HTTP_200_OK)

        serializer = ComplaintSerializer(complaints, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
class ComplaintView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        result = get_complaint(id)
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)
    
class ComplaintEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 
    
    def put(self, request,id):
        serializer = ComplaintEditSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            result = edit_complaint(
                id=id,
                user=request.user,
                title=data["title"],
                description=data["description"],
                area_name=data["area_name"],
                location_link=data["location_link"],
                image = request.FILES.get("image")
            )
            
            if "error" in result:
                return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Complaint updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplaintStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        status_value = request.data.get("status")

        if not status_value:
            return Response({"error": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        result = change_status(id, status_value)

        if "error" in result:
            return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Complaint status updated successfully."}, status=status.HTTP_200_OK)

class ComplaintDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request,id):
        result = delete_complaint(id)
        
        if "error" in result:
            return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Complaint was deleted successfully."}, status=status.HTTP_200_OK)
    
class CurrentComplaintView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        user = request.user

        if user.role == 'ADMIN':
            complaints = current_complaints(admin_id=user.id)
        elif user.role == 'OFFICER':
            complaints = current_complaints(officer_id=user.id)
        elif user.role == 'USER':
            complaints = current_complaints(user_id=user.id)
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_403_FORBIDDEN)

        if complaints == "No Complaints":
            return Response({"message": "No Complaints found"}, status=status.HTTP_200_OK)
       
        return Response(complaints, status=status.HTTP_200_OK)
        
        
class ResolvedComplaintView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        if user.role == 'ADMIN':
            complaints = resolved_complaints(admin_id=user.id)
        elif user.role == 'OFFICER':
            complaints = resolved_complaints(officer_id=user.id)
        elif user.role == 'USER':
            complaints = resolved_complaints(user_id=user.id)
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_403_FORBIDDEN)

        if complaints == "No Complaints":
            return Response({"message": "No Complaints found"}, status=status.HTTP_200_OK)
       
        return Response(complaints, status=status.HTTP_200_OK)
    

class ComplaintDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        result = detail_complaint(id)

        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)
    
class ComplaintStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'ADMIN':
            result = get_complaint_count(admin_id=user.id)
        elif user.role == 'OFFICER':
            result = get_complaint_count(officer_id=user.id)
        elif user.role == 'USER':
            result = get_complaint_count(user_id=user.id)
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_403_FORBIDDEN)

        return Response(result, status=status.HTTP_200_OK)
