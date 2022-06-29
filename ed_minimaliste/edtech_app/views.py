import json
from multiprocessing import context
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .utils import *
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import *
from django.urls import reverse
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from .models import *
from django.contrib.auth.models import Group
# Create your views here.
def home_student(request):
    categories = Category.objects.all()
    subcategories = subcat.objects.all()
    context = {
        'categories':categories,
        'subcat': subcategories, 
    }
    return render(request,'./Landing_Pages/EdTech_landing.html',context)
def login_view(request):
    if request.method == "GET":
        form = Studentloginform(request.GET or None)
    elif request.method == "POST":
        form = Studentloginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            messages.info(request, f"You are now logged in as {username}.")
            return HttpResponseRedirect(reverse("student_dash"))
        
    context= {'form':form}
    return render(request,"student/accounts/login.html",context)

def Logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_student"))

def signup_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        resume_form = resumeForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        resume_form = resumeForm(request.POST)
        if form.is_valid() and resume_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            resume_form.save()
            current_site = get_current_site(request)
            message = render_to_string('student/accounts/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            mail_subject = 'Activer votre Minimaliste compte.'
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject,message,email_from,[to_email])
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    
        
    return render(request, './student/accounts/register.html', {'form': form,'resumeForm':resume_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
######################signup_pour_les_enseignant#################################
def teacher_signup(request):
    form = SignUpForm()
    form_teacher = resumeForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        form_teacher = resumeForm(request.POST or None)
        if form.is_valid():
            user_teacher = form.save(commit=False)
            user_teacher.is_active = False
            user_teacher.save()
            resume=form_teacher.save(commit=False)
            resume.user=user_teacher
            resume.save()
            email_from = settings.EMAIL_HOST_USER
            mail_subject = 'Activer votre Enseignant Minimaliste compte.'
            message=' Votre demande a vérifie vous avez réussie la date rdv'
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject,message,email_from,[to_email])
            teacher_group = Group.objects.get_or_create(name='Teacher')
            teacher_group[0].user_set.add(user_teacher)
            return HttpResponseRedirect(reverse("teacher_login"))

    return render(request, './teachers/accounts/register.html',{'form': form,'resumeForm':resume})
############-----end register enseignant-------###########################
############-----Login enseignant-------###########################
def Login_Teacher(request):
    if request.method == "GET":
        form = TeacherLoginForm(request.GET or None)
    elif request.method == "POST":
        form = TeacherLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("student_dash"))
    context= {'form':form}
    return render(request,"teachers/accounts/login.html",context) 


############-----end Login enseignant-------###########################
#student_dash_view
def student_list_vids(request):
    list_cours = cours.objects.all()
    context= {'cours':list_cours}
    return render(request,'./student/home/student-list-vids.html',context)

#student_dash_view
def student_vid_content(request,pk):
    student_cour = cours.objects.get(id=pk)
    context = {'cours':student_cour}
    return render(request,'./student/home/video_content.html',context)
# payement methode
def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:',body)
    course = cours.objects.get(id=body['courseId'])
    Order.objects.create(
        course=course,
        user =request.user,
        ordred=True
    )
    return JsonResponse('Payement successful',safe=False)


def student_dashbord(request):

    
    return render(request,'./student/home/student_dashboard.html')
    
def student_cours(request):
    studentCourOrder =  Order.objects.filter(user__pk=request.user.id)
    context = {"student_cour":studentCourOrder}
    return render (request,'./student/home/student_cours.html',context)

def student_learn(request,pk):
    ordred = Order.objects.filter(user__pk=request.user.id,course__pk=pk)
    if not ordred:
        return HttpResponseRedirect(reverse("student_dash"))
    progVideo = VideoCours.objects.filter(cour__id=pk).order_by('id')
    if request.method == 'GET':
        Noteform=Note_Form(request.GET)
    video=VideoCours.objects.filter(cour__id=pk).first()
    context = {'videos':video,'list_vid':progVideo,'form':Noteform}
    return render(request,'./student/home/student_videos.html',context)

def student_vid(request,pk):
    Video = VideoCours.objects.get(id=pk)
    ordred = Order.objects.filter(user__pk=request.user.id,course__pk=Video.cour.id)
    if not ordred:
        return HttpResponseRedirect(reverse("student_dash"))
    if request.method == 'GET':
        Noteform=Note_Form(request.GET)

    progVideo=VideoCours.objects.filter(cour__id=Video.cour.id)
    context = {'videos':Video,'list_vid':progVideo,'form':Noteform}
    return render(request,'./student/home/student_videos.html',context)

def student_notes(request):
    data=dict()
    form = Note_Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        t=request.POST['notechapitre']
       
        text=request.POST["note"]
        
        vid=VideoCours.objects.get(id=t)
        notes(chapitre = vid,student = request.user, text_note=text).save()
    else:
        form = Note_Form()
    data={'success':1}
    return JsonResponse(data)
def like_video(request):
    data=dict()
    user = request.user
    Like =  False
    if request.method == 'POST':
        video_id = request.POST['video_id']
        get_video = cours.objects.get(id=video_id)
        if user in get_video.likes.all():
            get_video.likes.remove(user)
            Like = False
        else:
            get_video.likes.add(user)
            Like = True
        data = {'liked':Like,"likes_count":get_video.likes.all().count()}
    return JsonResponse(data)

def teacher_dashboard(request):
    return render(request,'./teachers/teacher_dashboard.html')

def teacher_student_page(request):
    return render(request,'./teachers/teacher_student.html')

def teacher_cours_page(request):
    return render(request,'./teachers/teacher_cours.html')

def teacher_annonce(request):
    return render(request,'./teachers/teacher_annonce.html')

def teacher_video(request):
    if request.method == 'GET':
        Cour_Form = Cours_Form(request.GET or None)
        Video_Form = Formset_vid(request.GET or None)
    elif request.method == 'POST':
        Cour_Form = Cours_Form(request.POST,request.FILES)
        Video_Form =Formset_vid(request.POST,request.FILES)
        if Cour_Form.is_valid():
            cour = Cour_Form.save()
            cour.teacher = request.user.username
            cour.save()
        if Video_Form.is_valid():
            for form in Video_Form:
                video = form.save(commit=False)
                video.cour = cour
                video.save()
        return HttpResponseRedirect(reverse("teachers_videos"))
    context = {'Cour_Form':Cour_Form,'Video_form':Video_Form}
    return render(request,'./teachers/teacher_video.html',context)
def admin_dashboard(request):
    return render(request, "administrateur/admin_dashboard.html")

def admin_annonce(request):
    return render(request, "administrateur/admin_annonce.html")

def admin_chat(request):
    return render(request, "administrateur/admin_chat.html")

def admin_etudiant(request):
    return render(request, "administrateur/admin_etudiant.html")

def admin_live(request):
    return render(request, "administrateur/admin_live.html")

def admin_programme(request):
    return render(request, "administrateur/admin_programme.html")

def admin_transaction(request):
    return render(request, "administrateur/admin_transaction.html")

def admin_cours(request):
    return render(request, "administrateur/admin_cours.html")


def admin_formateur(request):
    return render(request, "administrateur/admin_formateur.html")

def acceuil(request):
    return render(request, "acceuil/acceuil.html")

def admin_notifications(request):
    return render(request, "administrateur/admin_formateur.html")

############communité_minimaliste######################################

def List_annonce(request):
    list_annonce = annonce.objects.all()
    context = {'list_ann':list_annonce}
    return render(request,'./communiterMini/annonce/annonces.html',context)

def save_annonce_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            annonces = annonce.objects.all()
            data['html_annonce_list'] = render_to_string('./communiterMini/annonce/list_annonces.html', {
                'list_ann': annonces
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def Add_annonce(request):
    if request.method == "POST":
        annonce_form = Annonce_Form(request.POST)
    else:
        annonce_form = Annonce_Form()

    return save_annonce_form(request,annonce_form,'./communiterMini/annonce/annonces_form.html')
#question
def List_questions(request):
    list_question= question.objects.all()
    context={'questions':list_question}
    return render(request,'./communiterMini/question/questions.html',context)
   
def Add_question(request):
    list_question= question.objects.all()
    context={'questions':list_question}
    return render(request,'./communiterMini/question/questions.html',context)

def add_subject(request):
    SubForm = Subject_form()
    if request.method == 'POST':
        SubForm = Subject_form(request.POST)
        if SubForm.is_valid():
            Sub=SubForm.save()
            Sub.author = request.user
            Sub.save()
            return HttpResponseRedirect(reverse('subject'))
    return render(request,'./communiterMini/question/questions.html')
    
def add_subject_follow(request):
    return render(request,'./communiterMini/blog/blog.html')

def subject_list(request):
    return render(request,'./communiterMini/blog/blog.html')
def detail_subject(request,pk):
    return render(request,'./communiterMini/blog/blog.html')
    
def List_blogs(request):
    list_blogs= blog.objects.all()
    context={'questions':list_blogs}
    return render(request,'./communiterMini/blog/blog.html',context)

def Add_blog(request):
    form= Blog_Form()
    if request.method == 'POST':
        form = Blog_Form(request.POST)
        if form.is_valid():
            blog=form.save()
            blog.author = request.user
            blog.save()
            return HttpResponseRedirect(reverse('blog'))
    context={'form':form}
    return render(request,'./communiterMini/blog/add_blog.html',context)

def comment_blog(request):
    return render(request,'./communiterMini/blog/add_blog.html')

def detail_blog(request):
    return render(request,'./communiterMini/blog/add_blog.html',context)