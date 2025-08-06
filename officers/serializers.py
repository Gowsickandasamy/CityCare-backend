from rest_framework import serializers

from .models import Officer, OfficerRating

class OfficerSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Officer
        fields = ['userId','username','email', 'area_of_control','average_rating', 'reports_to']

class OfficerCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=255)
    area_of_control = serializers.CharField(max_length=255)
    reports_to = serializers.IntegerField(required=False) 


class OfficerRatingSerializer(serializers.ModelSerializer):
    rated_by = serializers.ReadOnlyField(source='rated_by.username')
    
    class Meta:
        model = OfficerRating
        fields = [ 'rating', 'comment', 'rated_by']
    
    def create(self, validated_data):
        complaint = self.context['complaint']
        rated_by = self.context['request'].user
        
        if not complaint.officer:
            raise serializers.ValidationError("Complaint must be assigned to an officer.")
        officer_user = complaint.officer
        officer = Officer.objects.filter(user=officer_user).first()
        print("Complaint Officer (User instance):", complaint.officer)
        print("Officer instance:", Officer.objects.filter(user=complaint.officer).first())

        
        if not officer:
            raise serializers.ValidationError("No Officer found for this User.")

        officer_rating = OfficerRating.objects.create(
            officer=officer,
            complaint=complaint,
            rating=validated_data['rating'],
            comment=validated_data.get('comment', ""),
            rated_by=rated_by
        )

        return officer_rating