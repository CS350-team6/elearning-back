from django.db import models

# TODO: Move models to their respective apps
# class Topic(models.Model):
#     topic_id = models.AutoField(primary_key=True)
#     instructor_id = models.ForeignKey('user_account.Instructor', on_delete=models.CASCADE, related_name='instructor')
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     level = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'topics'
 
#     def __str__(self):
#         return self.title

# class Question(models.Model):
#     question_id = models.AutoField(primary_key=True)
#     topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic')
#     student_id = models.ForeignKey('user_account.Student', on_delete=models.CASCADE, related_name='student')
#     question = models.TextField()
#     answer = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'questions'

# class Answer(models.Model):
#     answer_id = models.AutoField(primary_key=True)
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
#     instructor_id = models.ForeignKey('user_account.Instructor', on_delete=models.CASCADE, related_name='instructor')
#     answer = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'answers'

# class Feedback(models.Model):
#     feedback_id = models.AutoField(primary_key=True)
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
#     student_id = models.ForeignKey('user_account.Student', on_delete=models.CASCADE, related_name='student')
#     video_id = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='video')
#     rating = models.IntegerField()
#     question = models.TextField()
#     comment = models.TextField()
#     feedback = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'feedbacks'

# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     video_id = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='video')
#     student_id = models.ForeignKey('user_account.Student', on_delete=models.CASCADE, related_name='student')
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'comments'

# class Watchlist(models.Model):
#     watchlist_id = models.AutoField(primary_key=True)
#     student_id = models.ForeignKey('user_account.Student', on_delete=models.CASCADE, related_name='student')
#     video_id = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='video')
#     watched_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         verbose_name_plural = 'watchlists'

class Video(models.Model):
    # topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic')
    # instructor_id = models.ForeignKey('user_account.Instructor', on_delete=models.CASCADE, related_name='instructor')
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    play_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    video_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name_plural = 'videos'