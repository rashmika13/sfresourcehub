from .forms import ContactForm  # Add this
from .forms import AddResourceForm  # Add this
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Resource
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def resources_index(request):
    resources = Resource.objects.all()
    return render(request, 'resources/index.html', {'resources': resources})


def resourceView(request):
    error_message = ''
    if request.method == 'POST':
        form = AddResourceForm(request.POST)
        if form.is_valid():
            r = Resource(resource_name=form.cleaned_data['resource_name'],
                         org_name=form.cleaned_data['org_name'],
                         category=form.cleaned_data['category'],
                         opening_hours=form.cleaned_data['opening_hours'],
                         address=form.cleaned_data['address'],
                         street_number=form.cleaned_data['street_number'],
                         street_name=form.cleaned_data['street_name'],
                         city=form.cleaned_data['city'],
                         state=form.cleaned_data['state'],
                         country=form.cleaned_data['country'],
                         postal_code=form.cleaned_data['postal_code'],
                         long=form.cleaned_data['long'],
                         lat=form.cleaned_data['lat'],
                         phone=form.cleaned_data['phone'],
                         user=request.user,
                         url=form.cleaned_data['url'],
                         notes=form.cleaned_data['notes'])
            r.save()
            return redirect('index')
        else:
            print('!form.is_valid')
            print(form.errors)
            error_message = form.errors
    print("resourceView: requesting!")
    form = AddResourceForm()
    context = {'form': form}
    return render(request, 'resources/create.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Resource HUB: ' + form.cleaned_data['subject']
            sender = form.cleaned_data['from_email']
            message = '''
Sender: %s
Message: %s
            '''%(sender, form.cleaned_data['message'])
            recipent = ['sfresourcehub@gmail.com']
            try:
                send_mail(subject, message, sender,
                          recipent, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "email_success.html", {'subject': form.cleaned_data['subject'],
                                                          'message': form.cleaned_data['message'],
                                                          'sender': sender})
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

# def contact(request):
#     if request.method == "POST":
#         message_name = request.POST['message_name']
#         message_email = request.POST['message_email']
#         message = request.POST['message']

#         send_mail(
#             message_name,
#             message,
#             message_email,
#             ['sfresourcehub@gmail.com'],
#         )
#         return render(request, 'email.html', {'message_name': message_name})
#     else:
#         return render(request, 'email.html', {})

def resources_detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    return render(
        request,
        'resources/detail.html',
        {
            # Pass the cat and feeding_form as context
            'resource': resource
        })

class ResourceUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'resources/update.html'
    model = Resource
    form_class = AddResourceForm

class ResourceDelete(LoginRequiredMixin, DeleteView):
    model = Resource
    success_url = '/resources/'


@login_required
def myresources(request):
    myresources = Resource.objects.filter(user=request.user)
    return render(request, 'resources/myindex.html', {
        'myresources': myresources,
    })


def resources_categories(request):
    return render(request, 'categories.html')
