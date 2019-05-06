from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question

def filter_question_queryset():
    return Question.objects.filter(pub_date__lte=timezone.now())

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return filter_question_queryset().order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return filter_question_queryset()

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return filter_question_queryset()

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
             'question': question,
             'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save() 
        #must .refresh_from_db() in order to use values saved/updated like so
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
