# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from .models import Userprofile
# 并集运算
from django.db.models import Q
from .forms import LoginForm,RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from untils.email_send import send_register_eamil
from .models import EmailVerifyRecord


class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # 跳转到首页 user request会被带回到首页
                return render(request, "index.html")
            # 没有成功说明里面的值是None，并再次跳转回主页面
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误! "})

            # 验证不成功跳回登录页面
            # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
                return render(
                    request, "login.html", {
                        "login_form": login_form,
                        "msg":"用户名或密码错误"
                })


# 注册功能的view
class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = Userprofile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认激活状态为false
            user_profile.is_active = False
            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 发送邮件
            # 发送注册激活邮件
            send_register_eamil(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",
            {
                "msg": "格式错误",
                "register_form": register_form,
            })


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = Userprofile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效","active_form": active_form})


# 用户忘记密码的处理view
class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_from = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_from":forget_from })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form验证合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件
            send_register_eamil(email, "forget")
            # 发送完毕返回登录页面并显示发送邮件成功。
            return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
        # 如果表单验证失败也就是他验证码输错等。
        else:
            return render(request, "forgetpwd.html", {"forget_from": forget_form})


# 重置密码的view
class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                return render(request, "password_reset.html", {"email":email})
        # 自己瞎输的验证码
        else:
            return render(
                request, "forgetpwd.html", {
                    "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})


 # 改变密码的view
class ModifyPwdView(View):
    def post(self, request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            # 如果密码一致
            user = Userprofile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "login.html", {"msg": "密码修改成功，请登录"})
        # 验证失败说明密码位数不够。
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modiypwd_form":modiypwd_form})


# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate，可点进源码查看
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询

            user = Userprofile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):

            if user.check_password(password):
                return user
        except Exception as e:
            return None




#
# '''
# 函数方法登录
# '''
# # 当我们配置url被这个view处理时，自动传入request对象.
# def user_login(request):
#     # 前端向后端发送的请求方式: get 或post
#
#     # 登录提交表单为post
#     if request.method == "POST":
#         # 取不到时为空，username，password为前端页面name值
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#
#         # 成功返回user对象,失败返回null
#         user = authenticate(username=user_name, password=pass_word)
#
#         # 如果不是null说明验证成功
#         if user is not None:
#             # login_in 两参数：request, user
#             # 实际是对request写了一部分东西进去，然后在render的时候：
#             # request是要render回去的。这些信息也就随着返回浏览器。完成登录
#             login(request, user)
#             # 跳转到首页 user request会被带回到首页
#             return render(request, "index.html")
#         # 没有成功说明里面的值是None，并再次跳转回主页面
#         else:
#             return render(request, "login.html", {
#                 "msg": "用户名或者密码错误"
#             })
#     # 获取登录页面为get
#     elif request.method == "GET":
#         # render就是渲染html返回用户
#         # render三变量: request 模板名称 一个字典写明传给前端的值
#         return render(request, "login.html", {})

# Create your views here.
