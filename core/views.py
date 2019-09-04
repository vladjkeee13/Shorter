from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, RedirectView, TemplateView, FormView, UpdateView, DeleteView

from core.form import UrlForm, RegistrationForm, LoginForm
from core.models import Url, MyUser


def get_paginator(urls, request, context):

    paginator = Paginator(urls, 6)

    if 'page' in request:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context['urls'] = page.object_list
    context['page'] = page


class HomePageView(CreateView):

    template_name = 'home_page.html'
    form_class = UrlForm

    def form_valid(self, form):

        if self.request.user.is_anonymous:
            user = None
        else:
            user = self.request.user

        created_url_obj = form.save(user=user)

        messages.add_message(self.request,
                             messages.SUCCESS,
                             f'Short url http://127.0.0.1:8000/{created_url_obj.short_url}, '
                             f'for {created_url_obj.url} was created successfully!')

        return redirect('/')

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        try:
            urls = Url.objects.filter(author=self.request.user).order_by('-created_date')

            get_paginator(urls, self.request, context)
        except:
            pass

        return context


class RedirectToOriginalUrl(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        url = get_object_or_404(Url, short_url=self.kwargs['short_url'])

        if url:
            url.clicks += 1
            url.save()

        return url.url


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class AdminPanelView(CreateView):

    template_name = 'admin_panel.html'
    form_class = UrlForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        try:
            urls = Url.objects.all().order_by('-created_date')
            get_paginator(urls, self.request, context)
        except:
            pass

        return context

    def form_valid(self, form):

        form.save(user=self.request.user)

        return redirect(reverse('admin-panel'))


@method_decorator(login_required, name='dispatch')
class CRUDView(UpdateView):

    template_name = 'detail_url.html'
    model = Url
    fields = ('url', 'text', 'clicks', 'short_url', 'created_date')

    def get_success_url(self):
        return reverse('admin-panel')

    def post(self, request, *args, **kwargs):
        if 'Save' in request.POST['submit']:
            return super().post(request, *args, **kwargs)
        elif 'Delete' in request.POST['submit']:
            return redirect(reverse('core:delete-url', kwargs={'pk': self.get_object().pk}))


@method_decorator(login_required, name='dispatch')
class DeleteUrlView(DeleteView):

    model = Url

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin-panel')


class RegistrationView(FormView):

    template_name = 'registration.html'
    form_class = RegistrationForm

    def form_valid(self, form, backend='django.contrib.auth.backends.ModelBackend'):

        form.save()

        user = MyUser.objects.get(username=form.cleaned_data['username'])

        if user:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/')


class LoginView(FormView):

    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        login_user = authenticate(username=username, password=password)

        if login_user:
            login(self.request, login_user)

        return redirect('/')


@method_decorator(login_required, name='dispatch')
class MyAccountView(TemplateView):

    template_name = 'my_account.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        context['user'] = self.request.user

        return context
