from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question,Choice

# Create your views here.
#Introduction of generic views

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions(not including
        those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


    def get_queryset(self):
        """
        Excludes any questions that arent published yet
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"You didnt select a choice."})
        # Redisplay the question voting form
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after dealing with Post Data
        # This prevents data fro  being posted twice if a user the hits back button .
        return HttpResponseRedirect(reverse('polls:result',args=(question_id)))







# Old controllers and views
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template(('polls/index.html'))
#     context = {'latest_question_list':latest_question_list}
#
#     return render(request,'polls/index.html',context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request,'polls/detail.html',{'question': question})
#
# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})
#
#







# def vote(request,question_id):
#     return HttpResponse("Your Voting on question %s."% question_id)
