from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from .serializers import UserSerializer
from .forms import RegisterForm, LoginForm
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user
import json
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, reverse


# Create your views here.

class PermissionList(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "authentication.custom_can_view_permissions"
    template_name = 'authentication/perm_table.html'

    def get(self, request, *args, **kwaregs):
        permission_list = Permission.objects.filter(codename__icontains='custom_').order_by('codename')
        user_groups = Group.objects.all().order_by('name')
        context = {
            'permission_list': permission_list,
            'user_groups': user_groups
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        group_name = payload['group_name']
        codename = payload['codename']
        permission = payload['permission']
        error = False
        try:
            permission_obj = Permission.objects.get(codename=codename)
            group, created = Group.objects.get_or_create(name=group_name)

            if int(permission) == 1:
                # Add Permission
                group.permissions.add(permission_obj)
            else:
                # Remove Permission
                group.permissions.remove(permission_obj)
        except Exception as e:
            print(e)
            error = True

        response = {
            'error': error
        }
        # breakpoint()
        return JsonResponse(response)
        # pass


"""
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # user = get_user(request)
            user = form.save()
            #
            maintainers, created = Group.objects.get_or_create(name='Maintainers')
            appusers, created = Group.objects.get_or_create(name='AppUsers')

            user_type = form.cleaned_data.get('user_type')
            if user_type == 1:
                # maintainers.user_set.add(user)
                user.groups.add(maintainers)
            elif user_type == 2:
                user.groups.add(appusers)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


class RegisterApiView(APIView):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

"""


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


class ChangePassword(LoginRequiredMixin, View):
    form_class = PasswordChangeForm
    template_name = 'authentication/change_password.html'

    def post(self, request, *args, **kwargs):
        password_change_form = self.form_class(request.user, request.POST)
        print(password_change_form.errors)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully updated.')
            return HttpResponseRedirect(reverse('change.password'))
        else:
            return render(request, self.template_name, context={'password_change_form': password_change_form})

    def get(self, request, *args, **kwargs):
        password_change_form = self.form_class(request.user)
        context = {
            'password_change_form': password_change_form
        }
        return render(request, self.template_name, context)
