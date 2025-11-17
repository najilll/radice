from django.contrib import admin

from .models import Banner, courses, Course,Blog, Enrollment, Placements,WhatsAppNumber

# Register your models here.

admin.site.site_header = "Radice Administration"
admin.site.site_title = "Radice Admin Portal"
admin.site.index_title = "Welcome to Radice Admin Portal"

class BannerCourseInline(admin.TabularInline):
    model = courses
    extra = 1
    fields = ("name",)
    min_num = 0

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    inlines = [BannerCourseInline]
    list_display = ("title", "subtitle", "course_list", "image_preview")
    search_fields = ("title", "subtitle", "courses__name")
    readonly_fields = ("image_preview",)

    def course_list(self, obj):
        return ", ".join([c.name for c in obj.courses.all()])
    course_list.short_description = "Courses"

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height:40px"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "price")
    search_fields = ("title", "description")

admin.site.register(Course, CourseAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Blog, BlogAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "email", "phone", "enrolled_at")
    search_fields = ("name", "email", "phone", "course__title")
    list_filter = ("enrolled_at",)

admin.site.register(Enrollment, EnrollmentAdmin)

class PlacementsAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview")
    search_fields = ("name",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height:40px"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

admin.site.register(Placements, PlacementsAdmin)

class WhatsAppNumberAdmin(admin.ModelAdmin):
    list_display = ("number",)

admin.site.register(WhatsAppNumber, WhatsAppNumberAdmin)