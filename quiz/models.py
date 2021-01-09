from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator

class Quiz(models.Model):
    title = models.CharField(max_length=120)
    desc  = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']

    def no_of_questions(self):
        return self.questions.count()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=200)
    

    def __str__(self):
        return self.question

    def is_multiselect(self):
        count = 0
        for answer in self.answers.all():
            if answer.is_true:
                count += 1
        
        if count > 1:
            return True
        else:
            return False

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Quiz)