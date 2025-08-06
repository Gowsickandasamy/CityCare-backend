from rest_framework import serializers

from officers.serializers import OfficerRatingSerializer
from .models import Complaint
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model=Complaint
        fields=['id', 'user', 'officer', 'admin', 'title', 'description', 'area_name', 'location_link', 'created_at', 'status']
        
class ComplaintCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    area_name = serializers.CharField(max_length=255)
    location_link = serializers.URLField()
    
class ComplaintEditSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    area_name = serializers.CharField(max_length=255)
    location_link = serializers.URLField()
    
class ComplaintDetailSerializer(serializers.ModelSerializer):
    officer_ratings = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField() 

    class Meta:
        model = Complaint
        fields = [
            'id', 'user', 'officer', 'admin', 'title', 'description',
            'area_name', 'location_link', 'created_at', 'status',
            'officer_ratings', 'image', 'image_url'
        ]

    def get_officer_ratings(self, obj):
        from officers.models import OfficerRating
        ratings = OfficerRating.objects.filter(complaint=obj)
        return OfficerRatingSerializer(ratings, many=True).data
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None