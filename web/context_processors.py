from web.forms import EnrollmentForm

def main_context(request):
    return {
        'enrollment_form': EnrollmentForm()
    }