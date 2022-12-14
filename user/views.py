from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from paper.documents import AuthorDocument
from user.models import User, Application


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
        password = request.POST.get('password')

        if code != request.session.get('code'):
            return JsonResponse({'errno': 1002})

        password = make_password(password)
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
                request.session['sex'] = user.sex
                return JsonResponse({'errno': 0, 'msg': "登录成功", 'username': user.username, 'email': email, 'sex': user.sex})
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

class FindBackView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if User.objects.filter(email=email).exists():
            try:
                rand_str = self.send_message(email)  # 发送邮件
                request.session['code'] = rand_str  # 验证码存入session，用于做注册验证
                return JsonResponse({'errno': 0, 'msg': "发送验证码成功"})
            except:
                return JsonResponse({'errno': 2, 'msg': "发送验证码失败"})
        else:
            return JsonResponse({'errno': 1, 'msg': "该邮箱未注册"})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            password = make_password(password)
            if code == request.session.get('code'):
                user.password=password
                user.save()
                return JsonResponse({'errno': 0, 'msg': "修改成功"})
            else:
                return JsonResponse({'errno': 1, 'msg': "验证码不正确"})
        else:
            return JsonResponse({'errno': 2, 'msg': "用户不存在"})


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


class InfoView(APIView):

    def get(self, request):
        email = request.session.get('email')
        print(email)
        user = User.objects.get(email=email)
        data = {
            'email': user.email,
            'username': user.username,
            'description': user.description,
            'sex': user.sex,
        }
        return JsonResponse({'errno': 0, 'user': data, 'isadmin': user.isadmin})

    def post(self, request):
        email = request.session.get('email')
        user = User.objects.get(email=email)
        print(request.data.get('user[username]'))
        if request.data.get('user[username]'):
            user.username = request.data.get('user[username]')
        if request.data.get('user[description]'):
            user.description = request.data.get('user[description]')
        if request.data.get('user[sex]'):
            user.sex = request.data.get('user[sex]')
        if request.data.get('user[password]', None):
            user.password = make_password(request.data.get('user[password]', None))
        user.save()
        return JsonResponse({'errno': 0, 'msg': "更改个人信息成功"})


class ApplicationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        description = request.data.get('description', None)
        author_id = request.data.get('id', None)
        attachment = request.FILES.get('file', None)
        application = Application()
        application.user = user
        if description:
            application.description = description
        if author_id:
            if User.objects.filter(author_id=author_id).exists():
                return Response({'errno': 1})
            application.author_id = author_id
            search = AuthorDocument.search()[0:500].filter('term', id=author_id)
            response = search.execute()
            print(response)
            application.author_name = response.hits[0].name
        if attachment:
            application.attachment = attachment
        application.save()
        return Response({'errno': 0})


class IdentifyView(APIView):
    def get(self, request):
        lists = [
            {
                'id': item.pk,
                'email': item.user.email,
                'scholarid': item.author_id,
                'username': item.user.username,
                'scholarname': item.author_name,
                'description': item.description,
                'url': 'http://127.0.0.1:8000/' + 'media/'+ str(item.attachment)
            } for item in Application.objects.all()
        ]
        return Response({'errno': 0, 'lists': lists})

    def post(self, request):
        application_id = request.data.get('listid')
        op = request.data.get('op')
        print(request.data)
        if op == "1":
            application = Application.objects.get(pk=application_id)
            application.delete()
        else:
            application = Application.objects.get(pk=application_id)
            user = User.objects.get(email=application.user.email)
            user.author_id = application.author_id
            user.save()
            application.delete()
        return Response({'errno': 0})





