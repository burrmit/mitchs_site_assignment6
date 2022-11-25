# blog/views.py
"""
The blog app views.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, FormView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms, models

class HomeView(TemplateView):
    """
    The Home View Class Template View.
    """
    template_name = 'blog/home.html'

class AboutView(TemplateView):
    """
    The About View Class Template View.
    """
    template_name = 'blog/about.html'

class PostListView(ListView):
    """
    The Post List View.
    """
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class PostDetailView(DetailView):
    """
    The Post Detail View.
    """
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the post object
        post = self.get_object()

        # Set the post field on the form
        comment_form = forms.CommentForm(initial={'post': post})
        comments = models.Comment.objects.filter(post=post)

        context['comment_form'] = comment_form
        context['comments'] = comments.order_by('-created')

        return context

class TopicListView(ListView):
    """
    The Topic List View.
    """
    model = models.Topic
    context_object_name = 'topics/'
    queryset = models.Topic.objects.all()

class TopicDetailView(DetailView):
    """
    The Topic Detail View.
    """
    model = models.Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics_posts'] = models.Post.objects.filter(\
            topics__slug=self.kwargs['slug']).published().order_by('-published')

        return context

def terms_and_conditions(request):
    """
    The Terms and Conditions request function.
    """
    return render(request, 'blog/terms_and_conditions.html')

class ContactView(TemplateView):
    """
    The Contact View Class Template View.
    """
    template_name = 'blog/contact.html'

class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)

class PhotoContestView(CreateView):
    template_name = 'blog/photo_contest_form.html'
    model = models.PhotoContest
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for your submission! Good Luck!'
        )
        return super().form_valid(form)
