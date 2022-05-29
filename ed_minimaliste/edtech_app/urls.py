from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home_student,name='home_student'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.Logout_view,name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="student/accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="student/accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="student/accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="student/accounts/password_reset_done.html"),name="password_reset_complete"),
    path('student/', views.student_dashbord, name='student_dash'),
    path('profil_update/',views.teacher_signup, name='update_profil'),
    path('add_annonce/',views.Add_annonce, name='add_annonce'),
    path('annonce/',views.List_annonce, name='annonce'),
    path('blog/',views.List_blogs, name='blog'),
    path('blog_comment/<int:pk>',views.comment_blog, name='blog_comment'),
    path('student/vid/<str:id>',views.student_vid, name='student_vid'),
    path('add_blog/',views.Add_blog, name='add_blog'),
    path('detail_blog/<int:pk>',views.detail_blog, name='detail_blog'),
    path('question/',views.List_questions, name='question'),
    path('add_question/',views.Add_question, name='add_question'),
    path('add_sujet/',views.add_subject, name='add_sujet'),
    path('sujet_follow/',views.add_subject_follow, name='subject_follow'),
    path('sujet/',views.subject_list, name='subject'),
    path('detail_subject/<int:pk>',views.detail_subject, name='detail_subject'),
    path('teacher/dashboard',views.teacher_dashboard, name='teacher'),
    path('student/videos/<int:pk>',views.student_learn, name='student_videos'),
    path('student/Cours',views.student_cours, name='student_cours'),
    path('teacher/videos',views.teacher_video, name='teachers_videos'),
    path('teacher/cours',views.teacher_cours_page, name='teachers_cours'),
    path('teacher/annonces',views.teacher_annonce, name='teachers_annonce'),
    path('teacher/students',views.teacher_student_page, name='teachers_students'),
    path('like_videos',views.like_video, name='like_videos'),
    path('list_videos',views.student_list_vids, name='list_videos'),
    path('video_content/<int:pk>',views.student_vid_content, name='video_content'),
    path('payement_complete',views.paymentComplete, name='payement'),
    path('edAdmin/dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('edAdmin/list_etudiant',views.admin_etudiant, name='admin_etudiant'),
    path('edAdmin/list_cours',views.admin_cours, name='admin_cours'),
    path('edAdmin/list_formateurs',views.admin_formateur, name='admin_formateur'),
    path('edAdmin/notifications',views.admin_notifications, name='admin_notif'),
    path('edAdmin/list_annonces',views.admin_annonce, name='admin_annonces'),
    ]