# Standard Library imports

# Core Django imports
from django.urls import path
from django.shortcuts import get_object_or_404

# Third-party imports
from rest_framework.views import APIView
from rest_framework.response import Response

# App imports
from ..models.lecture_model import Lecture, Video
from ..services import lecture_service

class LectureDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Lecture, pk=pk)
    
    def get(self, request, pk, format=None):
        lecture_model = self.get_object(pk)
        lecture_info_dict = lecture_service.get_lecture_info_from_lecture_model(lecture_model)
        resp = { "data": { "lecture_info": lecture_info_dict }}

        return Response(data=resp, status=200)
    
    def put(self, request, pk):
        lecture_model = self.get_object(pk)
        pass

    def delete(self, request, pk):
        lecture_model = self.get_object(pk)
        pass


class Lecture(APIView):
    def get(self, request):
        # TODO: AttributeError: type object 'Lecture' has no attribute 'objects'
        queryset = Lecture.objects.all()

        title = request.GET.get("title")
        year = request.GET.get("year")
        semester = request.GET.get("semester")
        if title is not None:
            queryset = queryset.filter(title=title)
        if year is not None:
            queryset = queryset.filter(year=year)
        if semester is not None:
            queryset = queryset.filter(semester=semester)

        lecture_models = queryset
        lecture_info_dict = []
        for lecture_model in lecture_models:
            lecture_info_dict.append(lecture_service.get_lecture_info_from_lecture_model(lecture_model))

        resp = { "data": { "lecture_info": lecture_info_dict }}
        return Response(data=resp, status=200)
    
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        instructor = request.data.get("instructor")
        year = request.data.get("year")
        semester = request.data.get("semester")
        videos = request.data.get("videos")
        lecture_model = lecture_service.create_lecture_with_videos(title, description, instructor, year, semester, videos)
        return Response(status=200)
