from .models import categories

def categories_list(request):
	categoriesList = categories.objects.all()
	return { 'categories': categoriesList}
