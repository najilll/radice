from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title
    
class courses(models.Model):
    name = models.CharField(max_length=200)
    banner = models.ForeignKey(Banner, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='courses/')
    description = HTMLField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('web:course_detail', args=[self.slug])
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blogs/')
    content = HTMLField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_home = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('web:blog_detail', args=[self.slug])
    
class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.title} - {self.enrolled_at}"