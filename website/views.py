from django.shortcuts import render
from django.views.generic import DetailView , ListView , CreateView, TemplateView
from .models import posts, PostComments, HomePageSlideShow, CategorySlideShow
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegisterForm, ContactForm, CooperationForm, CommentForm, UserCommentForm
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from suds.client import Client
from django.contrib.messages.views import SuccessMessageMixin

MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 1000  # Amount will be based on Toman  Required
description = u'یﺖﺴﺗ ﺶﻧکاﺮﺗ ﺕﺎﺣیﺽﻮﺗ'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/verify/'



def send_request(request):
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return HttpResponse('Error')


def verify(request):
    client = Client(ZARINPAL_WEBSERVICE)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.GET['Authority'],
                                                    amount)
        if result.Status == 100:
            return HttpResponse('Transaction success. RefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed. Status: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')



class Homepage(ListView):
	model=posts
	template_name='homepage.html'

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
		context['slideShow'] = HomePageSlideShow.objects.all()
		return context


class RegisterView(SuccessMessageMixin, CreateView):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return render(request, 'info.html', {'message': 'شما هم اکنون عضو سایت هستید'})
		else:
			return render(request, 'register.html', {'form': RegisterForm()})
	form_class = RegisterForm
	template_name = 'register.html'
	success_url = '/login'
	success_message = "ثبت نام با موفقیت انجام شد"

class PostView(UserPassesTestMixin , DetailView):
	login_url = '/login/'
	model = posts
	template_name = 'postView.html'
	def get_queryset(self):
		queryset = posts.objects.filter(slug=self.kwargs.get("slug"))
		return queryset

	def test_func(self):
		queryCheck = self.get_queryset()
		if queryCheck[0].justPaidUsers:
			return self.request.user.is_authenticated and self.request.user.profile.is_paid
		if queryCheck[0].justUsers :
			return self.request.user.is_authenticated
		return True

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['form'] = UserCommentForm()
		else:
			context['form'] = CommentForm()

		context['Comments'] = PostComments.objects.filter(postOwner__slug=self.kwargs.get("slug"),allow=True)
		return context

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
			fullName = form.cleaned_data['fullName']
			recipients = ['farzan_salimiyan@yahoo.com']
			html_message = loader.render_to_string(
			'contactUsEmail.html',
			{
			'sender': sender,
			'subject': subject,
			'message': message,
			'fullName':fullName
			}
			)
			if cc_myself:
				recipients.append(sender)
			try:
				send_mail(subject, message, sender, recipients, html_message = html_message)
				return render(request, 'info.html', {'message': 'درخواست با موفقیت ارسال شد'})
			except:
				return render(request, 'Error.html', {'message': 'خطا در ارسال لطفا دوباره اقدام کنید'})
			return render(request, 'Error.html', {'message': 'خطا در ارسال لطفا دوباره اقدام کنید'})

	else:
		form = ContactForm()
		return render(request, 'contactUs.html', {'form': form})




def CooperationView(request):
	
	if request.method == 'POST':
		form = CooperationForm(request.POST, request.FILES)
		if form.is_valid():
			fullName = form.cleaned_data['fullName']
			birthdayDate = form.cleaned_data['birthdayDate']
			email = form.cleaned_data['email']
			phonenumber = form.cleaned_data['phonenumber']
			job = form.cleaned_data['job']
			city = form.cleaned_data['city']
			Resume = request.FILES['Resume']
			gender = form.cleaned_data['gender']
			description = form.cleaned_data['description']

			html_message = loader.render_to_string(
			'cooperationEmail.html',
			{
			'fullName': fullName,
			'birthdayDate': birthdayDate,
			'email': email,
			'phonenumber':phonenumber,
			'job': job,
			'city': city,
			'gender':gender,
			'description': description,
			}
			)
			subject = "cooperation"
			message = description


			try:
				mail = EmailMessage(subject, html_message, to = ['farzan_salimiyan@yahoo.com'], from_email = email)
				mail.content_subtype = "html"
				mail.attach(Resume.name, Resume.read(), Resume.content_type)
				mail.send()
				return render(request, 'info.html', {'message': 'درخواست با موفقیت ارسال شد'})
			except:
				return render(request, 'Error.html', {'message': 'فایل اپلود شده ایراد دارد یا حجم زیادی دارد'})	
			return render(request, 'Error.html', {'message': 'خطا در ارسال لطفا دوباره اقدام کنید'})

	else:
		form = CooperationForm()
		return render(request, 'cooperation.html', {'form': form})

	
def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/login")


class PostCommentView(SingleObjectMixin, FormView):
	template_name = 'postView.html'
	form_class = CommentForm
	model = posts

	def post(self, request, *args, **kwargs):
		self.object= post = self.get_object()
		if request.user.is_authenticated:
			form = UserCommentForm(request.POST)
		else:
			form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.postOwner = post
			if self.request.user.is_authenticated:
				comment.mail = self.request.user.email
				comment.userName = self.request.user.username
				comment.fullName = self.request.user.first_name +' '+ self.request.user.last_name
			comment.save()
		return redirect('postsUrl', slug=self.object.slug)

	def get_success_url(self):
		return reverse('postsUrl', kwargs={'slug': self.object.slug})

class PostDetailViewCombine(View):

    def get(self, request, *args, **kwargs):
        view = PostView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentView.as_view()
        return view(request, *args, **kwargs)

class postsViewByCategories(ListView):
	template_name='homepage.html'
	def get_queryset(self):
		return posts.objects.filter(category_name__category_name=self.kwargs["category_name"])
	def get_context_data(self,**kwargs):
		context = super(postsViewByCategories,self).get_context_data(**kwargs)
		context['categorySlideShow'] = CategorySlideShow.objects.filter(category_name__category_name=self.kwargs.get("category_name"))
		context['object_list'] = posts.objects.filter(category_name__category_name=self.kwargs.get("category_name"))
		return context


class search(ListView):
	template_name='homepage.html'
	paginate_by = 2	
	def get_queryset(self):
		query = self.request.GET.get('q')
		queryset =posts.objects.filter(context__icontains=query)
		return queryset


class ProfileView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name ='profile.html'
	def get_queryset(self):
		return self.request.user.profile


