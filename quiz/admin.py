from django.contrib import admin
from .models import Quiz, Question

class QuestionInline(admin.StackedInline):
    model = Question

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'public']
    list_editable = ['public']

    class Meta:
        model = Quiz

admin.site.register(Quiz, QuizAdmin)