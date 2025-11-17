from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView
from .forms import EnrollmentForm
from .models import Banner, Blog,Course, Enrollment, Placements,WhatsAppNumber
from urllib.parse import quote

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
    
    def post(self, request, *args, **kwargs):
        form = EnrollmentForm(request.POST)
        number = WhatsAppNumber.objects.first()
        if not number:
            return JsonResponse({'success': False, 'error': 'WhatsApp number not configured.'})
        if form.is_valid():
            form.save()
            
            whatsapp_number = number.number # Replace with actual number

            # Construct message text
            message = (
                f"New Enrollment Enquiry Submission:\n"
                f"Course: {form.cleaned_data['course']}\n"
                f"Name: {form.cleaned_data['name']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Phone: {form.cleaned_data['phone']}"
            )

            # Encode message for URL
            encoded_message = quote(message)

            # Construct WhatsApp API URL
            api_url = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"

            # Redirect to WhatsApp
            return redirect(api_url)

        else:
            return JsonResponse({'success': False, 'errors': form.errors})


# Paginated blog list
class BlogListView(ListView):
    model = Blog
    template_name = "web/blog_list.html"
    context_object_name = "blogs"  # what template uses
    ordering = ['-published_date']  # newest first

from django.core.exceptions import FieldError
class BlogDetailView(DetailView):
    model = Blog
    template_name = "web/blog_detail.html"
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        number = WhatsAppNumber.objects.first()
        # exclude current blog from recent list
        qs = Blog.objects.exclude(pk=self.object.pk)

        # try common date fields to order recent posts robustly
        try:
            recent = qs.order_by('-published_date')[:4]
        except FieldError:
            try:
                recent = qs.order_by('-created_at')[:4]
            except FieldError:
                # final fallback
                recent = qs.order_by('-id')[:4]

        context['recent_blogs'] = recent
        context['number'] = number
        return context

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
        ctx['related_courses'] = Course.objects.exclude(pk=self.object.pk).order_by('-id')[:2]
        return ctx
    

class AboutView(TemplateView):
    template_name = "web/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["placements"] = Placements.objects.all() 
        return context
    