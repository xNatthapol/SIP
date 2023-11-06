from django.shortcuts import render

# Create your views here.
from django.views import generic

class LoginView(generic.ListView):
    """
    Display the latest five questions.
    """
    template_name = 'login_page/index.html'

    def get_queryset(self):
        """
        Return the all published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')
