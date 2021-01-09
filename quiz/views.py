from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.utils.html import escape
from .models import Quiz, Question
from django.shortcuts import get_object_or_404
from .forms import QuizForm, QuestionFormSet
from django.contrib import messages
from taggit.models import Tag

def home(request):
    quizzes = Quiz.objects.filter(public=True)
    return render(request, 'quiz/index.html', {
        'quizzes': quizzes
    })

def tag(request, slug):
    tags = Tag.objects.all()
    if request.method == 'GET':
        if slug:
            slug = escape(slug).lower()
            quizzes = Quiz.objects.filter(public=True).filter(tags__slug__in=[slug]).distinct()

        return render(request, 'quiz/tag_search.html', {
            'quizzes': quizzes
        })
    return redirect('quiz:home')

def quiz(request, slug):
    slug = escape(escape_uri_path(slug))
    # query the db
    
    quiz = get_object_or_404(Quiz, slug=slug)
    questions = quiz.questions.all()

    if request.method == 'POST':
        data = request.POST
        score = 0

        for question in questions:
            question_id = str(question.id)
            selected_answer = data.get(question_id)

            if selected_answer:
                # check if the answer is correct
                if question.answer == 1:
                    correct_answer = question.option_one
                elif question.answer == 2:
                    correct_answer = question.option_two
                elif question.answer == 3:
                    correct_answer = question.option_three
                else:
                    correct_answer = question.option_four

                if selected_answer == correct_answer:
                    score += 1

        percentage = (score / questions.count()) * 100
        
        return render(request, 'quiz/result.html', {
            'score': score,
            'total': questions.count,
            'percentage': percentage,
            'questions': questions
        })

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

def create(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if all([quiz_form.is_valid(), question_formset.is_valid()]):
            quiz = quiz_form.save()
            for inline_form in question_formset:
                if inline_form.cleaned_data:
                    question = inline_form.save(commit=False)
                    question.quiz = quiz
                    question.save()
            messages.success(request, 'Your Quiz will be visible once it has been approved by the admin...')
            return redirect('quiz:home')
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none())

    return render(request, 'quiz/create.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset
    })

# 404
def handler404(request, exception):
  return render(request, '404.html', status=404)

# 500
def handler500(request):
  return render(request, '500.html', status=500)