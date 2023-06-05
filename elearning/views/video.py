from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, parsers, filters
from ..models.video import Video
from ..serializers.video import VideoSerializer

class VideoViewset(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = Video.objects.all()
        year = self.request.query_params.get('year')
        semester = self.request.query_params.get('semester')
        lecture = self.request.query_params.get('lecture')
        if year is not None:
            queryset = queryset.filter(year=year)
        if semester is not None:
            queryset = queryset.filter(semester=semester)
        if lecture is not None:
            queryset = queryset.filter(lecture=lecture)
        return queryset