from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("blogs/", views.BlogListView.as_view(), name="blog_list"),
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("course/<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    # path("enroll/", views.EnrollmentView.as_view(), name="enroll"),
    path("about/", views.AboutView.as_view(), name="about"),
]