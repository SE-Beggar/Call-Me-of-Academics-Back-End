from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from user.models import User


# Create your views here.
class RegisterView(APIView):

    def get(self, request):
        email = request.GET.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'errno': 2001})
        try:
            rand_str = self.send_message(email)  # 发送邮件
            request.session['code'] = rand_str  # 验证码存入session，用于做注册验证
            return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 2004, 'msg': "发送验证码失败"})

    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if code != request.session.get('code'):
            return JsonResponse({'errno': 1002})
        if password_1 != password_2:
            return JsonResponse({'errno': 1003})
        password = make_password(password_1)
        User.objects.create(email=email, username=username, password=password)
        return JsonResponse({'errno': 0})

    def send_message(self, email):
        import random
        str1 = '0123456789'
        rand_str = ''
        for i in range(0, 6):
            rand_str += str1[random.randrange(0, len(str1))]
        message = "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
        print(rand_str)
        mailBoxes = []
        mailBoxes.append(email)
        send_mail('验证码', message, '1030519668@qq.com', mailBoxes, fail_silently=False)
        return rand_str


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = email
                request.session['username'] = user.username
                return JsonResponse({'errno': 0, 'msg': "登录成功", 'username': user.username, 'email': email})
            else:
                return JsonResponse({'errno': 1001, 'msg': "密码错误"})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户不存在"})
        pass
    else:
        return JsonResponse({'errno': 1003, 'msg': "请求方式错误"})


def logout(request):
    request.session.flush()
    return JsonResponse({'errno': 0, 'msg': "注销成功"})


class InfoView(APIView):

    def get(self, request):
        email = request.session.get('email')
        user = User.objects.get(email=email)
        data = {
            'email': user.email,
            'username': user.username,
            'description': user.description,
            'sex': user.sex,
        }
        return JsonResponse({'errno': 0, 'data': data})

    def post(self, request):
        email = request.session.get('email')
        user = User.objects.get(email=email)
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('description'):
            user.description = request.POST.get('description')
        if request.POST.get('sex'):
            user.sex = request.POST.get('sex')
        user.save()
        return JsonResponse({'errno': 0, 'msg': "更改个人信息成功"})

