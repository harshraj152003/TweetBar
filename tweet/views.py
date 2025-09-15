from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    # FIX: Fetch the tweet first, then check if the user is the owner.
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this tweet.")

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            # FIX: Simplified the save logic. 'form.save()' is enough here.
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})


@login_required
def tweet_delete(request, tweet_id):
    # FIX: Fetch the tweet first, then check if the user is the owner.
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this tweet.")

    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method == "POST":
        # FIX: Used the correct form name 'UserRegistrationForm'
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # FIX: 'form.save()' handles password hashing automatically
            user = form.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    
    tweet_count = Tweet.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'tweet_count': tweet_count
    }
    return render(request, 'profile.html', context)