# Standard Library imports

# Core Django imports
from django.forms.models import model_to_dict
from django.db import transaction

# Third-party imports

# App imports
from ..models.lecture_model import Lecture, Video

def create_lecture_with_videos(title, description, instructor, year, semester, videos):
    if Lecture.objects.filter(title=title, instructor=instructor, year=year, semester=semester).exists():
        raise Exception("A lecture with this title, and instructor already exists!")
    
    with transaction.atomic():
        lecture_model = Lecture.objects.create(
            title=title,
            description=description,
            instructor=instructor,
            year=year,
            semester=semester,
        )
        lecture_model.full_clean()
        lecture_model.save()
        for video in videos:
            video_model = Video.objects.create(
                lecture=lecture_model,
                title=video["title"],
                description=video["description"],
                # TODO: upload video to S3 and store the url here
                url=video["url"],
            )
            video_model.full_clean()
            video_model.save()
    return lecture_model

def get_lecture_info_from_lecture_model(lecture_model):
    lecture_model = lecture_model.select_related('videos').all()
    lecture_model_dict = model_to_dict(lecture_model)

    allowlisted_keys = ['title', 'description', 'instructor', 'year', 'semester', 'videos']

    for key in list(lecture_model_dict.keys()):
        if not key in allowlisted_keys:
            lecture_model_dict.pop(key)

    return lecture_model_dict


def create_video(lecture_id, title, description, url):
    lecture_model = Lecture.objects.get(id=lecture_id)
    with transaction.atomic():
        video_model = Video.objects.create(
            lecture=lecture_model,
            title=title,
            description=description,
            # TODO: upload video to S3 and store the url here
            url=url,
        )
        video_model.full_clean()
        video_model.save()
    return video_model