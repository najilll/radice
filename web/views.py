from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Banner, Blog,Course

# Create your views here.
class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the first banner and prefetch its courses
        banner = Banner.objects.prefetch_related('courses').first()
        courses = Course.objects.all()
        blogs = Blog.objects.filter(is_home=True)[:3]
        context['courses'] = courses
        context['banner'] = banner
        context['blogs'] = blogs
        return context


# Paginated blog list
class BlogListView(ListView):
    model = Blog
    template_name = "web/blog_list.html"
    context_object_name = "blogs"  # what template uses
    ordering = ['-published_date']  # newest first


class BlogDetailView(DetailView):
    model = Blog
    template_name = "web/blog_detail.html"
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CourseListView(ListView):
    model = Course
    template_name = "web/course_list.html"
    context_object_name = "courses"
    ordering = ['-id']  # newest first


class CourseDetailView(DetailView):
    model = Course
    template_name = "web/course_detail.html"
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_courses'] = Course.objects.exclude(pk=self.object.pk).order_by('-id')[:3]
        return ctx
