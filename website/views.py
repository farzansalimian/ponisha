from django.shortcuts import render
from django.views.generic import DetailView as DV
from django.views.generic.list import ListView as LV
from .models import posts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def show(request):
	return render(request,"base.html",)


class homepage(LV):
	models=posts
	template_name='homepage.html'
	queryset = posts.objects.all()

	def get_context_data(self,**kwargs):
		context = super(homepage,self).get_context_data(**kwargs)
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
