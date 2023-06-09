from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from .models import Video, Lecture
from .serializers import VideoSerializer, LectureSerializer

class LectureViewset(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_video':
            return VideoSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='videos')
    def upload_video(self, request, pk=None):
        """Upload an video to a lecture"""
        lecture = self.get_object()
        serializer = self.get_serializer(
            lecture,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class VideoViewset(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        '''Retrieve the videos with year, semester, lecture_id'''
        year = self.request.query_params.get('year')
        semester = self.request.query_params.get('semester')
        lecture_id = self.request.query_params.get('lectureId')
        queryset = self.queryset
        if year:
            queryset = queryset.filter(year=year)
        if semester:
            queryset = queryset.filter(semester=semester)
        if lecture_id:
            queryset = queryset.filter(lecture=lecture_id)
        return queryset