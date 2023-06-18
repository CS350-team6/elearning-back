from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from .models import Video, Lecture, Comment, Watchlist, Like, Understand, NotUnderstand
from .serializers import VideoSerializer, LectureSerializer, CommentSerializer, WatchlistSerializer, LikeSerializer, UnderstandSerializer, NotUnderstandSerializer

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
        serializer = VideoSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(lecture=lecture)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'message': 'Invalid data'},
            status=status.HTTP_400_BAD_REQUEST
        )

class VideoViewset(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        if self.action == 'search':
            return Lecture.objects.all()
        return self.queryset

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request):
        queryset = self.get_queryset()
        year = request.query_params.get('year')
        semester = request.query_params.get('semester')
        title = request.query_params.get('title')
        if year:
            queryset = queryset.filter(year=year)
        if semester:
            queryset = queryset.filter(semester=semester)
        if title:
            queryset = queryset.filter(title=title)
        serializer = LectureSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=True, url_path='comments')
    def upload_comment(self, request, pk=None):
        """Upload an comment to a video"""
        video = self.get_object()
        serializer = CommentSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(video=video, user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'message': 'Invalid data'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(methods=['POST'], detail=True, url_path='understands')
    def click_understand(self, request, pk=None):
        """Click an understand to a video"""
        video = self.get_object(pk=pk)
        serializer = UnderstandSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(video=video, user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'message': 'Invalid data'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(methods=['POST'], detail=True, url_path='not-understands')
    def click_notunderstand(self, request, pk=None):
        """Click an notunderstand to a video"""
        video = self.get_object()
        serializer = NotUnderstandSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(video=video, user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'message': 'Invalid data'},
            status=status.HTTP_400_BAD_REQUEST
        )

class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']