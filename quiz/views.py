from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.utils.html import escape
from .models import Quiz
from django.shortcuts import get_object_or_404

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/index.html', {
        'quizzes': quizzes
    })

def quiz(request, slug):
    slug = escape(escape_uri_path(slug))
    # query the db
    
    quiz = get_object_or_404(Quiz, slug=slug)
    questions = quiz.questions.all()

    if request.method == 'POST':
        data = request.POST
        print(data)
        return redirect('quiz:home')

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })