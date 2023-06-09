from rest_framework import serializers
from .models import Video, Lecture

class LectureSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Video.objects.all()
    )
    
    class Meta:
        model = Lecture
        fields = '__all__'
class VideoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Video
        fields = '__all__'
