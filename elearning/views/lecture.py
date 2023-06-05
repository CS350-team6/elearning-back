from rest_framework.decorators import action
from rest_framework import viewsets
from ..models.lecture import Lecture
from ..serializers.lecture import LectureSerializer

class LectureViewset(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = Lecture.objects.all()
        year = self.request.query_params.get('year')
        semester = self.request.query_params.get('semester')
        instructor = self.request.query_params.get('instructor')
        if year is not None:
            queryset = queryset.filter(year=year)
        if semester is not None:
            queryset = queryset.filter(semester=semester)
        if instructor is not None:
            queryset = queryset.filter(instructor=instructor)
        return queryset