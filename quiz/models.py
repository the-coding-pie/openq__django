from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager

class Quiz(models.Model):
    title = models.CharField(max_length=120)
    desc  = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    public = models.BooleanField(default=False)
    tags = TaggableManager()

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

    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100, blank=True)
    option_four = models.CharField(max_length=100, blank=True)

    answer = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])

    def __str__(self):
        return self.question

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Quiz)