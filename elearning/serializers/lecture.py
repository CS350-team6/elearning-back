from rest_framework import serializers
from ..models.lecture import Lecture

class LectureSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Lecture
        fields = '__all__'
