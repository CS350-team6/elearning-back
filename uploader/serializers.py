from rest_framework import serializers
from .models import Video, Lecture

class VideoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Video
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(
        many=True,
        # queryset=Video.objects.all()
    )
    
    class Meta:
        model = Lecture
        fields = '__all__'
