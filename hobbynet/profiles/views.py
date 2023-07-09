from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView

UserModel: User = get_user_model()


def profile_details(request, pk, slug):
    user = UserModel.objects.get(pk=pk)
    if not user or (
            request.user != user
            and
            user.profile.visibility != 'public'
    ):
        raise Http404("User profile doesn't exist")
    if user.profile.slug != slug:
        return redirect('profile_details', pk=pk, slug=user.profile.slug)
    return render(request, 'profiles/profile.html', context={
        'user': user,
    })


# TODO: add login required mixin
class ProfileEdit(FormView):
    """ This function will serve both the topic settings and profile settings,
    they are pretty similar, so we could manage with one common form,
    but also for profile will add extra stuff in the form"""
    # TODO: complete profile edit
    template_name = 'profiles/edit.html'

    def get_context_data(self):
        # TODO: return topic context
        return {}

    def get_form_class(self):
        # TODO: return form class, depending on what is being edited
        return None


class ProfileDetails:
    pass


@login_required
def profile_details_self(request):
    return redirect('profile_details', pk=request.user.pk, slug=request.user.profile.slug)
