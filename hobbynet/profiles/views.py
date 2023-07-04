from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def profile_details(request, pk, slug):
    return render(request, 'profiles/profile.html')


class ProfileEdit:
    pass


class ProfileDetails:
    pass


@login_required
def profile_details_self(request):
    return redirect('profile_details', pk=request.user.pk, slug=request.user.profile.slug)