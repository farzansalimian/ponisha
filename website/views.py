from django.shortcuts import render
from django.views.generic import DetailView , ListView , CreateView, TemplateView
from .models import posts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegisterForm, ContactForm, Cooperation
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

class Homepage(ListView):
	models=posts
	template_name='homepage.html'
	queryset = posts.objects.all()

	def get_context_data(self,**kwargs):
		context = super(Homepage,self).get_context_data(**kwargs)
		queryset=posts.objects.all()
		paginator = Paginator(queryset, 10)

		page = self.request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)
		context['posts'] = contacts
		return context


class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'register.html'
	success_url = '/'


class PostView(DetailView):
	model = posts
	template_name = 'postView.html'
	def get_queryset(self):
		queryset = posts.objects.filter(slug=self.kwargs.get("slug"))
		return queryset

class AboutusView(TemplateView):
	template_name = "aboutUs.html"

def ContactusView(request):
	
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']
			recipients = ['info@example.com']
			if cc_myself:
				recipients.append(sender)

			send_mail(subject, message, sender, recipients)
			return HttpResponseRedirect('/')

	else:
		form = ContactForm()

	return render(request, 'contactus.html', {'form': form})




def CooperationView(request):
	
	if request.method == 'POST':
		form = Cooperation(request.POST)
		if form.is_valid():
			fullName = form.cleaned_data['fullName']
			birthdayDate = form.cleaned_data['birthdayDate']
			email = form.cleaned_data['email']
			phonenumber = form.cleaned_data['phonenumber']
			job = forms.form.cleaned_data['job']
			city = form.cleaned_data['city']
			Resume = form.cleaned_data['Resume']
			gender = form.cleaned_data['gender']
			description = form.cleaned_data['description']
			
			return HttpResponseRedirect('/')

	else:
		form = Cooperation()

	return render(request, 'cooperation.html', {'form': form})

