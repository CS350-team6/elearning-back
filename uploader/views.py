from rest_framework import viewsets, parsers
from .models import Video
from .serializers import VideoSerializer
class VideoViewset(viewsets.ModelViewSet):
 
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']