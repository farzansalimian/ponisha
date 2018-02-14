from django import forms
from django.contrib.auth import get_user_model
from django.forms import SelectDateWidget
from .models import PostComments

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("تکرار گذرواژه صحیح نمی باشد")
        return password2

    def clean_email(self):
        # Check that the given email is exist already or not
        email = self.cleaned_data.get("email")
        if( User.objects.filter(email=self.cleaned_data.get("email")) ):
            raise forms.ValidationError("این ایمیل قبلا در سایت ثبت شده است")
        return email
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    fullName = forms.CharField(max_length=100)


class CooperationForm(forms.Form):
    GENDER_CHOICES = (
        ('Male', 'مرد'),
        ('Female', 'زن'),
    )
    fullName = forms.CharField(max_length=100)
    birthdayDate = forms.DateField(widget=SelectDateWidget())
    email = forms.EmailField()
    phonenumber = forms.CharField(max_length=100)
    job = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    Resume = forms.FileField(required=False, widget = forms.FileInput)
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
    description = forms.CharField(widget=forms.Textarea, required=False)

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ('comment',)
class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ('mail','comment','fullName')

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100)