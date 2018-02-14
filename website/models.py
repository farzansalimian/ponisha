from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import pre_save,  post_save
from django.core.urlresolvers import reverse
import jdatetime
from django.utils.text import slugify
import itertools
from django.contrib.auth.models import User
from django.dispatch import receiver

#Posts
class posts(models.Model):
	title = models.CharField(max_length=100, null=True)
	context = RichTextField()
	author = models.CharField(max_length=100)
	image   = models.ImageField(null=True,upload_to='postsImages', height_field=None, width_field=None, max_length=100)
	createdDate   = models.DateField(auto_now_add=True, auto_now=False)
	updatedDate   = models.DateField(auto_now_add=False, auto_now=True)
	category_name =models.ForeignKey('categories',on_delete=models.CASCADE,null=True)
	slug = models.SlugField(null=True, blank=True, unique=True, allow_unicode=True)
	summary = RichTextField()
	readTime = models.CharField(max_length=100, null=True)
	justUsers = models.BooleanField(default=False)
	justPaidUsers = models.BooleanField(default=False)

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


#Profile
class Profile(models.Model):
	#image   = models.ImageField(null=True,upload_to='usersImages', height_field=None, width_field=None, max_length=100, blank=True)
	is_paid = models.BooleanField(default=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		max_length = instance._meta.get_field('slug').max_length
		instance.slug = orig = slugify(instance.title, allow_unicode=True)[:max_length]
		for x in itertools.count(1):
			if not posts.objects.filter(slug=instance.slug).exists():
				break
			instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)


pre_save.connect(rl_pre_save_receiver, sender=posts)

class PostComments(models.Model):
	userName = models.CharField(max_length=150, default='کاربر مهمان')
	fullName = models.CharField(max_length=150, blank=True)
	comment = models.TextField()
	mail = models.EmailField(max_length=254)
	allow =models.BooleanField(default=False)
	postOwner = models.ForeignKey('posts', on_delete=models.CASCADE,null=True)
	post_date = models.DateTimeField(auto_now_add=True, auto_now=False,null=True)


	def __str__(self):
		username = self.userName
		if self.userName =='کاربر مهمان' : 
			username +=" - "+ self.fullName
		return username

class HomePageSlideShow(models.Model):
	context = RichTextField()
	image1 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)
	image2 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)
	image3 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)


class CategorySlideShow(models.Model):
	category_name = models.ForeignKey('categories', on_delete=models.CASCADE)
	context = RichTextField()
	image1 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)
	image2 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)
	image3 = models.ImageField(upload_to='slidShowImages', height_field=None, width_field=None, max_length=100)