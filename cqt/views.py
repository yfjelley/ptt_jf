from django.shortcuts import render, render_to_response
from cqt.forms import UserForm
from django.template import  RequestContext
from cqt.models import User

# Create your views here.
def home(request):
    return render_to_response('homepage.html')

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = User()
            user.username = username
            user.password = password
            user.save()
            return render_to_response('success.html',{'username':username}, context_instance = RequestContext(request))
    else:
        uf = UserForm()
        return render_to_response('register.html', {'uf' : uf}, context_instance = RequestContext(request))
