from django.db import models
from ckeditor.fields import RichTextField

#Posts

class posts(models.Model):
	title = models.CharField(max_length=100, null=True)
	context = RichTextField()
	author = models.CharField(max_length=100)
	image   = models.ImageField(null=True,upload_to='postsImages', height_field=None, width_field=None, max_length=100)
	createdDate   = models.DateField(auto_now_add=True, auto_now=False,null=True)
	updatedDate   = models.DateField(auto_now_add=False, auto_now=True)
	category_name =models.ForeignKey('categories',on_delete=models.CASCADE,null=True)
	class Meta:
		ordering = ['-pk']

	def __str__(self):
		return self.title;


class categories(models.Model):
		category_name     = models.CharField(null=True,max_length=30)
		def __str__(self):
			return self.category_name