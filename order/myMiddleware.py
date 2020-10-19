from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("中间件已经初始化完毕")

    # view处理请求前执行
    def process_request(self, request):  # 某一个view

        print("request:", request,'我是view处理请求前执行的')

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):

        # print("view:", request, view_func, view_args, view_kwargs)
        if "login" not in request.path:  # 路径中如果没有"login"
            print("登录验证")
            session = request.session  # 获取session
            if session.get("username"):  # 判断是否有登录的标记
                print("已登录")
            elif "regist" in request.path:
                print("未登录,开启注册")
            elif "captcha" in request.path:
                print("未登录，开启验证码权限")
            elif 'check_user' in request.path:
                print("未登录，开启验证用户权限")
            elif 'index' in request.path:
                print("未登录，开始浏览主页")
            elif 'booklist' in request.path:
                print("未登录，开始浏览图书列表")
            elif 'details' in request.path:
                print("未登录，开始浏览图书详情")
            elif 'car' in request.path:
                print("未登录，开始浏览购物车")
            else:
                print("未登录，正在跳转到登录界面")
                # 未登录且访问到未开启权限的界面时，跳转登录页面,并直接为page赋值，使其登录或注册后直接跳转到订单页面
                return render(request, "login.html", {'page': '/car/?page=1'})
        else:
            print("正在登录")  # 如果路径中"login"即为登录流程本身


    # view执行之后，响应之前执行
    def process_response(self, request, response):
        print("response:", request, response)
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        print("exception:", request, ex)