# Create your views here.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, HttpResponse 

#necessary for email confirmation
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail, BadHeaderError, EmailMultiAlternatives

from django.views.decorators.csrf import csrf_exempt, csrf_protect


from email.mime.image import MIMEImage

from  django.views.decorators.http import require_http_methods
from .forms import  SignUpForm, ResetPasswordForm, PostForm, ProfileForm, ContactForm, NewsUsersForm
from .tokens import account_token
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authtoken.models import Token
from .models import View,Like,Clap, Post, Profile, Category, Clap, Profile
from django.conf import settings


def highest_clapper_post():
    claps_count = []
    for user in User.objects.all():
        for p in Post.objects.filter(post_by=user):
            clap_count.append(Clap.objects.filter(post=p))
    print(max(clap_count))

@require_http_methods(['POST', 'GET'])
def newsletter(request):
    newsform = NewsUsersForm()
    msg = ""
    if request.POST:
        newsform = NewsUsersForm(request.POST)
        if newsform.is_valid():
            msg = "Thanks for subscribing :)"
            newsform.save()
    context = {'newsform': newsform, 'msg': msg}
    return context

def index(request):
    head_post  = Post.objects.all().first()
    categories = Category.objects.all()
    last_p = Post.objects.latest()
    top_blogs  = list(Post.objects.order_by("-id")[:5].values_list("topic", flat=True)).append([last_p, head_post])
    context_1 = newsletter(request)
    if head_post:
        related_posts_first = Post.objects.filter(category=head_post.category).order_by("topic", "modified").exclude(pk=head_post.id)[:1]
        recipe_for_head     = Post.objects.filter(pk=head_post.id)
        side_posts = list(v.post for v in View.objects.order_by('-num')[:5])
        recent_posts = list(l.post for l in Like.objects.order_by("-num_of_likes"))[:8]
        top_posts = Post.objects.all()[:2]

    context = {'top_blogs': top_blogs, 'head_post': head_post, 'related_posts_first': related_posts_first, 'recipe_for_head':recipe_for_head, 'top_posts': top_posts, 'recent_posts': recent_posts, 'side_posts': side_posts, 'categories': categories, 'last_p': last_p,}
    context.update(context_1)
    return render(request, "index.html", context)


def list_posts(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    posts_from_category = Post.objects.filter(category=category).order_by('-id', '-modified')
    # for the explore footer
    head_post = Post.objects.all().first()  
    last_p = Post.objects.all().last()
    
    paginator = Paginator(posts_from_category, 9) # Show 1 post per page
    page = request.GET.get('page') #paginate returns the page key for post(s)
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    
    context = {'categories': categories,  'posts': posts, 'category':category, 'head_post': head_post, 'last_p': last_p}
    return render(request, "website/category_posts.html", context)


def getpost(request, slug=None):
    req_post = get_object_or_404(Post, slug=slug)
    try:
        related_posts = set([random.choice(Post.objects.filter(category=req_post.category).exclude(pk=req_post.id)) for p in range(5)])
        posts    = set([random.choice(Post.objects.exclude(id__in=([c.id for c in related_posts]))) for p in range(5)])
    except Exception as e:
        related_posts = None
        posts = None
        
    recipe_for_req = Post.objects.filter(pk=req_post.id)
    categories = Category.objects.all()
    head_post = Post.objects.all().first()
    last_p = Post.objects.latest()

    clap_count = 0
    try:
        for post in Post.objects.filter(post_by=req_post.post_by):
            clap_count += int(post.clap.num_claps)
    except Exception as e:
        clap_count = 0
    if request.user.is_authenticated:
         token = str(Token.objects.get_or_create(user=request.user)[0].key)
    context_1 = newsletter(request) 
    try:
        profile = get_object_or_404(Profile, pk=req_post.post_by)
    except:
        profile="Anonymous"
    context = {'req_post': req_post, 'related_posts': related_posts, 'recipe_for_req': recipe_for_req, 'posts': posts, 'categories': categories, 'head_post': head_post, 'last_p': last_p, 'clap_count': clap_count,  'profile': profile}
    context.update(context_1)
    return render(request, "website/requested_post.html", context)



        

def contact(request):
    categories = Category.objects.all()
    form = ContactForm(request)
    head_post = Post.objects.latest()
    last_p = Post.objects.first()

    if request.POST:
        form = ContactForm(request, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Message Sent")        
            return redirect(reverse("contact"))
    context = {"form": form, "categories": categories, 'head_post': head_post,'last_p': last_p}
    return render(request, 'website/contact.html', context)


def email_password_reset(request):
    email = request.POST.get('email', '')
    try:
       user = User.objects.get(email=email)
       if user and user.is_active:
        message = render_to_string("activate_reset_password.html", {
            "email" : email,
            "domain" : get_current_site(request).domain,
            "uid" : urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            "token" : account_token.make_token(user)
        })

        mail = EmailMessage("Please use the Reset link ",
            message,
            to=[email],
            headers = {'Reply-To': 'noreply@divweb.com'}
            )
        mail.attach_alternative(message, "text/html")
        mail.content_subtype = "html"
        mail.mixed_type = "related"
        mail.send()     
    except(BadHeaderError, ValueError, Exception):
        messages.info(request, "link sent to email")
        return redirect("signin")
    else:
        messages.info(request, "sent you an email")
        return redirect("signin")    


def password_reset_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(pk=uid)
    user = None
    if user.is_active and account_token.check_token(user, token):
        user.refresh_from_db()
        login(request, user)
        return redirect(reverse("reset_password"))
    else:
        return redirect("page_not_found")




#considering request.post as a dictionary get a value from a key(say request.POST.get("email"))
def registration(request):
    signupform = SignUpForm(request)
    if request.POST:
        signupform = SignUpForm(request, request.POST)
        if signupform.is_valid():
            signupform.save()
            return HttpResponse('PLEASE CHECK EMAIL FOR FURTHER INSTRUCTIONS')
    return render(request, "registration/signup.html",{"signupform": signupform, 'fterms': ("Username","Email")})




def activate(request, uidb64, token):
    try:
    	uid = urlsafe_base64_decode(uidb64).decode()
    	user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
        
    if user is not None and account_token.check_token(user, token):
    	user.refresh_from_db()
    	user.is_active = True
    	user.save()
    	login(request, user)
    	messages.success(request,"registration completed successfully")    
        
    	return redirect(reverse("dashboard", args=(user.username,)))
    else:
        return redirect("page_not_found")

def userlogin(request):
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user     = authenticate(request, username=username, password=password)
        if user is not None and user.is_active: # if the account of the user is still active
                login(request, user)
                request.session["identity"] = request.user.id 
                messages.success(request,"Welcome %s your dashboard" % request.user.username)
                return redirect(reverse('dashboard', args=(request.user.username,)))
        else:
            context = {"errors" : "login details are invalid"}
            return render(request, "registration/login.html", context)
    else:
        return render(request, "registration/login.html", {})

@login_required
def reset(request):
    if request.POST:
        form = ResetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request,"Password reset is successfull")
            return redirect(reverse('dashboard', args=(request.user.username,)))
    else:
        form = ResetPasswordForm(request.user)
    return render(request, "dashboard/reset.html",{"form": form})
    
@never_cache
@login_required(login_url = "signin")
def dashboard(request,  username):
    try:
        username = request.user.username
        profile = get_object_or_404(Profile, author=request.user)
        
        user = get_object_or_404(User, username=username)
        try:

            posts = Post.objects.filter(post_by=user.id).order_by("-modified")
            count = posts.count()
            user_claps = 0
            for p in posts:
                user_claps += p.clap.num_claps
        except Exception as e:
            posts = None
            count = 0
            user_claps = 0

        context = {'post_count': count, "posts":posts, "profile":profile, 'claps': user_claps}
        return render(request, 'layouts/dashboard.html', context)
    except Exception as e:
        print("\n", e, "\n")
        messages.info(request, "You are not authorised ")

        logout(request)
        return redirect(reverse("signin"))

@login_required(login_url='signin')
def userlogout(request):
    """ simply logs out the user """
    logout(request)
    return redirect(reverse("indexpage"))



@login_required(login_url="signin")
def create_content(request):
    """ Create content to be displayed"""
    claps = 0
    for p in Post.objects.filter(post_by=request.user):
        claps += p.clap.num_claps
    if request.method == "POST":
        form = PostForm(request, request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            messages.info(request, "Your post was added successfully")
            return redirect(reverse("dashboard", args=(request.user.username,)))
    
    form = PostForm(request)
    profile = get_object_or_404(Profile, pk=request.user.id)
    return render(request, "dashboard/user_content.html", {'form': form, 'subvalue':"Create Post", 'profile': profile, 'claps': claps})


@login_required(login_url='signin')
def edit_post(request, pk):
   post = get_object_or_404(Post, pk=pk)
   profile = get_object_or_404(Profile, pk=post.post_by.id)  
   form = PostForm(request, request.POST or None,request.FILES or None, instance=post)
   if form.is_valid():
        form.save()
        messages.info(request, "Post is updated successfully")
        return redirect(reverse("dashboard", args=(request.user.username,)))
   return render(request, "dashboard/user_content.html", {'form': form, 'subvalue': "Update Post", "post":post, 'profile': profile})

@login_required(login_url="signin")
def delete_post(request, pk):
    try:
        post = get_object_or_404(Post, id=pk)
        post.delete()
    except Exception as e:
        return redirect("page_not_found")
    else:
        messages.info(request, "The post was successfully removed")
        return redirect("dashboard", args=(request.user.username))

@login_required(login_url="signin")
def search_posts(request):
    results = Category.objects.filter()
    pass


def search_site(request):
    posts = Post.objects.filter(tags="")

@login_required(login_url="signin")
def edit_profile(request, name):
    claps = 0
    for p in Post.objects.filter(post_by=request.user):
        claps += p.clap.num_claps
    name = request.user.username 
    profile = get_object_or_404(Profile, pk=request.user.id)
    form = ProfileForm(request, request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        messages.info(request, "Hurray! you now own a work profile")
        return redirect(reverse("dashboard", args=(request.user.username,)))
    return render(request, "dashboard/profile.html", {'form':form, 'legend': "edit profile", 'profile':profile, 'claps': claps})


def page_not_found(request):
    return render(request, "404.html", {})


def stripepay(request):
    import stripe # new
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = settings.STRIPE_PUBLISHABLE_KEY
    if request.POST:
        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='9bloggers Funding',
            source=request.POST['stripeToken']
            )
        messages.info(request, "Thanks For Your Support ")
        redirect(reverse('payment'))
    context = {'key' : key}
    return render(request, 'payments/payment.html', context)


def no_js(request):
    return HttpResponse('<center><h1><b><big> PLEASE ENABLE JAVASCRIPT TO VIEW THIS PAGE</big></b></h1></center>')