from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.utils.html import escape
from .models import Quiz, Answer
from django.shortcuts import get_object_or_404
import collections

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
        score = 0

        for question in questions:
            question_id = str(question.id)
            if data.get(question_id):
                # check if the answers are correct
                correct_answers = [answer.answer for answer in Answer.objects.filter(question=question, is_true=True)]
                selected_answers = data.getlist(question_id)

                if collections.Counter(selected_answers) == collections.Counter(correct_answers):
                    score += 1
                else:
                    print('wrong')          
            else:
                print('you didnt attended this question')
        return render(request, 'quiz/result.html', {
            'score': score,
            'total': questions.count
        })

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })