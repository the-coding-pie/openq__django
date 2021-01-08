from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerTabularInline(admin.TabularInline):
    model = Answer
    min_num = 2
    max_num = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabularInline]

    class Meta:
        model = Question

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)