from rest_framework import serializers
from .models import Video, Lecture, Comment, Watchlist, Like, Understand, NotUnderstand

class CommentSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Comment
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
         
    class Meta:
        model = Watchlist
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
                 
    class Meta:
        model = Like
        fields = '__all__'

class UnderstandSerializer(serializers.ModelSerializer):
                         
    class Meta:
        model = Understand
        fields = '__all__'

class NotUnderstandSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotUnderstand
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False, allow_null=True, default=None)
    likes = LikeSerializer(many=True, required=False, allow_null=True, default=None)
    understands = UnderstandSerializer(many=True, required=False, allow_null=True, default=None)
    notunderstands = NotUnderstandSerializer(many=True, required=False, allow_null=True, default=None)

    class Meta:
        model = Video
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, required=False, allow_null=True, default=None)
    
    class Meta:
        model = Lecture
        fields = '__all__'

