from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from website.utils import random_string_generator
from django.core.urlresolvers import reverse
import jdatetime
#Posts
class posts(models.Model):
	title = models.CharField(max_length=100, null=True)
	context = RichTextField()
	author = models.CharField(max_length=100)
	image   = models.ImageField(null=True,upload_to='postsImages', height_field=None, width_field=None, max_length=100)
	createdDate   = models.DateField(auto_now_add=True, auto_now=False)
	updatedDate   = models.DateField(auto_now_add=False, auto_now=True)
	category_name =models.ForeignKey('categories',on_delete=models.CASCADE,null=True)
	slug = models.SlugField(null=True, blank=True)
	summary = RichTextField()
	readTime = models.CharField(max_length=100, null=True)


	class Meta:
		ordering = ['-pk']

	def __str__(self):
		return self.title;

	def get_summary_text(self):
		no_tags =self.context
		no_tags = no_tags.replace('&nbsp;', ' ')
		trimmed = no_tags[0:1024]
		if trimmed.rfind('.') != -1:
			return trimmed[:trimmed.rfind('.') + 1] + ('...' if trimmed.endswith('.') else '')
		else:
			return trimmed


	def get_absolute_url(self):
		return reverse('postsUrl', kwargs={'slug': self.slug})


#Categories
class categories(models.Model):
		category_name     = models.CharField(null=True,max_length=30)
		def __str__(self):
			return self.category_name


#Users
class users(models.Model):
	username    = models.CharField(max_length=50)
	password    = models.CharField(max_length=100)
	email       = models.EmailField(max_length=400)
	first_name = models.CharField(max_length=100,null=True)
	last_name = models.CharField(max_length=100,null=True)
	last_login  = models.DateField(auto_now_add=False, auto_now=True)
	date_joined = models.DateField(auto_now_add=True, auto_now=False,null=True)
	image       = models.ImageField(null=True,upload_to='usersImages', height_field=None, width_field=None, max_length=100, blank=True)
	is_active      = models.BooleanField(default=0)
	is_superuser   = models.BooleanField(default=0)
	is_staff       = models.BooleanField(default=0)

	def __str__(self):
		return self.username


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=posts)

