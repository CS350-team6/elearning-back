from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, parsers, filters
from .models import Video
from .serializers import VideoSerializer

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', ['title', 'description'])

class VideoViewset(viewsets.ModelViewSet):
    filter_backends = (DynamicSearchFilter,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get'])
    def get_video(self, request):
        video = Video.objects.all()
        serializer = VideoSerializer(video, many=True)
        return Response(serializer.data)