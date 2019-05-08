#-*- coding:utf-8 -*-
import re

import os.path
from PIL import Image
from io import StringIO, BytesIO


from django import forms 
from django.forms import PasswordInput, TextInput, Textarea, Select, HiddenInput
from django.utils.translation import  ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives as EM, send_mass_mail
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.text import slugify
from django.core.files.storage import default_storage as storage
from django.core.validators import validate_email, RegexValidator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
#from django.contrib.postgres.forms import SimpleArrayField
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.template.loader import get_template
from django.utils.encoding import  force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model

from .tokens import account_token
from .models import Post, Category, Profile, NewsUsers, Clap

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ("first_name", "last_name", "username", "password1", "password2", 'email')
        attrs  = {"class":"form-control reginput"}
        widgets= {
            'first_name': TextInput({**attrs.copy(), "autofocus": "true", "required": "true"}), 'last_name':  TextInput({**attrs.copy(), "required": "true"}),
            'username'  : TextInput(attrs.copy()),
            'email'     : TextInput(attrs.copy()),
        }

    def __init__(self, request, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.request = request
        
        self.fields['password1'].widget.attrs.update({"class":"form-control reginput"})
        self.fields['password2'].widget.attrs.update({"class":"form-control reginput"})
        
    
    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        # find a user to match for the email
        try:
            User.objects.get(email=email)
        except (Exception, IOError):
            print("User Email is new, Preparing to save")
        else:
            raise forms.ValidationError("Email is already in use")
        return email
    
    
    def save(self, *args, commit=True, **kwargs):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            print("This for saved user", user)
            mail_subject = "Activate Your Account"
            mail_message = render_to_string('activate_acct_mail.html', {
                'user'   :   user,
                "domain" : get_current_site(self.request).domain,      
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_token.make_token(user)
            })

            try:
                email = EM(
                    mail_subject, 
                    mail_message, 
                    to=[user.email],
                    headers = {'Reply-To': 'noreply@9blogspace.com'}
                    )
                email.attach_alternative(mail_message, "text/html")
                email.send(fail_silently=True)
            except Exception as e:
                print("\n", e)
            


       

class ResetPasswordForm(SetPasswordForm):
    """helps to autogenerate change password  form"""
    pass

class PostForm(forms.ModelForm):
    """ create a form to generate Posts"""
    content = forms.CharField(label=_("Blog Content"), min_length=500, widget=forms.Textarea(attrs= { 'rows':"30", 'cols':'50'}))
    class Meta:
        model  = Post
        fields = ("category","topic", "content", "photos", "tags")
        attrs  = {"class":"form-control reginput"}
        widgets = {
            'category': Select(attrs.copy()),
            'topic': TextInput(attrs.copy()), 'content':  Textarea({'rows': '30', 'cols': '40',**attrs.copy()}),
            'tags':  TextInput({**attrs.copy(), 'placeholder': 'type a search keyword followed by a comma here', "data-role": "tagsinput"})
            }
       

    def __init__(self, request, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_photos(self):
        try:
            filename, file_ext = os.path.splitext(self.cleaned_data['photos'].name)
            print(filename, "\t", file_ext)
            self.cleaned_data['photos'].name = "%s%s" % (slugify(self.cleaned_data['topic']).lower(), file_ext)
            print("\n", self.cleaned_data['photos'].name)
        except Exception as e:
            print(e)
        else:
            return self.cleaned_data['photos']

    def save(self, commit=True):
        your_post = super(PostForm, self).save(commit=False)
        your_post.post_by = self.request.user
        if commit:
            your_post.save()
        

        
class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label=_("Describe Yourself (not more than 200chars) "),widget=forms.Textarea(), max_length=201, help_text='use less than 200 characters')
    
    class Meta:
        model = Profile
        fields = ('bio','picture')
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def save(self, commit=True):
        try:
            profile = super().save(commit=False)
            profile.ip_addr = self.get_client_ip()
            print("\n Coming from profile forms \n", profile.ip_addr)
            if commit:
                profile.save()
        except Exception as e:
            print("\n", e, "\n")


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    main = os.path.splitext(value.name)[0]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u"File type is prohibited: Use images,.pdf', '.doc', '.docx', '.jpg', '.png'")

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    full_name = forms.CharField(required=True)
    company = forms.CharField(required=True, help_text='if you dont have, please enter none')
    phone = forms.CharField(validators=[RegexValidator(regex=r'^\+\d{1,3}\-\d{6,15}$', message="Enter a valid phone number")],
                             required=True, help_text="+xxx-xxxxxxxxx   -- > country code - number e.g +12-12929029202")
    sender_email = forms.EmailField(label=_("Your Email"), required=True)
    message = forms.CharField(label=_("Message"),required=True, widget=forms.Textarea())
    files   = forms.FileField(
        label = _("Select File to Upload"), 
        required = False,
        validators = [validate_file_extension],
        widget = forms.ClearableFileInput(attrs={'multiple': True, 'accept':["image/*","video/*",".pdf"]}))

    def __init__(self, request, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.request = request
    

    def clean_files(self):
        content = self.cleaned_data['files']
        if content is not None:
            if content.size > int(settings.MAX_UPLOAD_SIZE):
                raise forms.ValidationError("The maximum file size that can be uploaded is 5MB")

          
        return content
    
    
    def save(self):
        cleaned_data = self.cleaned_data
        try:
            mail_message = render_to_string("contact_mail.html",{
            "contact_email": cleaned_data['sender_email'],
            "contact_name" : cleaned_data['full_name'],
            "contact_company": cleaned_data['company'],
            "contact_phone" :  cleaned_data['phone'],
            "form_content":    cleaned_data['message'],

            })
            email = EM(
                        "New ContactForm Submission Tagged %s" % cleaned_data['subject'],
                        mail_message,
                        to=['gatezdomain@gmail.com'],
                headers = {'Reply-To': cleaned_data['sender_email'] }
                )
            if cleaned_data['files']:
            	try:
            		for upl_file in self.request.FILES.getlist('files'):
            			print(Path(str(upl_file)))
            			p = str(upl_file)
            			email.attach(p, upl_file.read())
            	except Exception as e:
            		print("Error >> ", e)

            email.attach_alternative(mail_message, "text/html")
            email.content_subtype = "html"
            email.mixed_type = "related"
            email.send(fail_silently=True)
        except (BadHeaderError, Exception) as e:
        	print("OVERALL CONTACT ERRORS ", e)




class NewsUsersForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control round-form", 'placeholder': "Your email"} ))
    class Meta:
        model = NewsUsers
        fields = ('email',)



        

