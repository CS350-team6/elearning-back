import json
from django.urls import reverse
from django.test import TestCase

from uploader.models import Video

class VideoAPITest(TestCase):
    def setUp(self):
        Video.objects.create(title='test video', description='test description')
        Video.objects.create(title='test video2', description='test description2')
        self.create_read_url = reverse('video_rest_api')
        self.read_update_delete_url = reverse('video_rest_api', kwargs={'description': 'test description'})
    
    def test_list(self):
        response = self.client.get(self.create_read_url)
        self.assertContains(response, 'test video')
        self.assertContains(response, 'test video2')

    def test_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = json.loads(response.content)
        content = {
            'title': 'test video',
            'description': 'test description'
        }
        self.assertEqual(data, content)

    def test_create(self):
        video = {
            'title': 'test video3',
            'description': 'test description3'
        }
        response = self.client.post(self.create_read_url, video)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        content = {
            'title': 'test video3',
            'description': 'test description3'
        }
        self.assertEqual(data, content)
        self.assertEqual(Video.objects.count(), 3)
    
    def test_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Video.objects.count(), 1)

    