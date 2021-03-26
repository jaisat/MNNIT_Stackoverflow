from django.shortcuts import render
from .models import Question,Answer,Comment,Upvote,Downvote
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import AnswerForm,QuestionForm
from django.contrib import messages
from django.db.models import Count
# Create your views here.
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    paginator=Paginator(quests,3)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'home.html',{'quests':quests})

def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    answers=Answer.objects.filter(question=quest)
    answerform=AnswerForm    
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user
            answer.save()
            messages.success(request, 'Answer has been submitted.')
    return render(request,'detail.html',
                  {'quest':quest,
                   'tags':tags,
                   'answers':answers,
                   'answerform':answerform
    })

def save_comment(request): 
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        return JsonResponse({'bool':True})

def save_upvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Upvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
             
            Upvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})




def save_downvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Downvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Downvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

def ask_form(request):
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            messages.success(request,'Question has been added.')
    return render(request,'ask-question.html',{'form':form})


# Questions Acording to tags
def tag(request, tag):
    quests = Question.objects.filter(tags__icontains=tag).order_by('-id')
    paginator = Paginator(quests, 10)
    page_num = request.GET.get('page', 1)
    quests = paginator.page(page_num)
    return render(request, 'tag.html', {'quests': quests, 'tag': tag})


def tags(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})