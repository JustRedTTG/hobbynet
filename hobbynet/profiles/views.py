from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

UserModel: User = get_user_model()

def profile_details(request, pk, slug):
    user = UserModel.objects.get(pk=pk)
    if not user:
        raise Http404("User profile doesn't exist")
    if user.profile.slug != slug:
        return redirect('profile_details', pk=pk, slug=user.profile.slug)
    return render(request, 'profiles/profile.html', context={
        'user': user,
        'slug': slug
    })


class ProfileEdit:
    pass


class ProfileDetails:
    pass


@login_required
def profile_details_self(request):
    return redirect('profile_details', pk=request.user.pk, slug=request.user.profile.slug)