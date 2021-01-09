from django import forms
from .models import Question, Quiz
from django.forms import modelformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'desc', 'tags'] 

QuestionFormSet = modelformset_factory(Question, fields=['question', 'option_one', 'option_two', 'option_three', 'option_four', 'answer'], extra=0, min_num=1, validate_min=True)
