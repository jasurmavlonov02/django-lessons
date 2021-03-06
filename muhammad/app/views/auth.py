from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, TemplateView

from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, send_email
from app.models import User
from app.token import account_activation_token


class LoginMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

# Product list
class LoginPage(LoginMixin,LoginView):
    form_class = LoginForm
    template_name = 'app/auth/login.html'
    success_url = reverse_lazy('index')




# def login_page(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(email = form.cleaned_data['email'],password = form.cleaned_data['password'])
#             if user:
#                 login(request, user)
#             else:
#                 messages.add_message(
#                     request,
#                     level=messages.WARNING,
#                     message='This profile not active!'
#                 )
#                 return render(request, 'app/auth/login.html', {'form': form})
#             return redirect('index')
#         else:
#             messages.add_message(
#                 request,
#                 level = messages.ERROR,
#                 message='Loginda xatolik'
#             )
#
#
#         # email = request.POST.get('email')
#         # password = request.POST.get('password')
#     return render(request, 'app/auth/login.html',{'form':form})


class RegisterPage(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('login_page')
    template_name = 'app/auth/register.html'


    def form_valid(self, form):
        form.save()
        send_email(form.data.get('email'),self.request,'register')
        messages.add_message(
            self.request,
            level=messages.SUCCESS,
            message='Successfully send your email, Please activate your profile'
        )
        return super().form_valid(form)



class LogoutPage(LogoutView):
    template_name = 'app/auth/logout.html'


class ForgotPassword(FormView):
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('login_page')
    template_name = 'app/auth/forgot-password.html'

    def form_valid(self, form):
        send_email(form.data.get('email'),self.request,'forgot')
        return super().form_valid(form)



class ActivateEmailView(TemplateView):
    template_name = 'app/auth/confirm_mail.html'

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(e)
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message="Your account successfully activated!"
            )
            return redirect('index')
        else:
            return HttpResponse('Activation link is invalid!')

