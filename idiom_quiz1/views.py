import json
import random
import requests
from django.http import JsonResponse
from .serializers import *
from rest_framework import generics
from .models import *
import time


class RetCode(object):
    SUCCESS = '0000'
    INVALID_PARA = '0001'
    USER_NOT_EXIST = '0002'
    SHOP_NOT_EXIST = '0003'
    WXSRV_ERROR = '0004'
    SRV_EXCEPTION = '0005'


def get_openid(js_code):
    appid, secret = 'wx9536e4863caab47d', 'f42f641333217112366a5489ed2f79e8'
    url = "https://api.weixin.qq.com/sns/jscode2session"
    args = {
        'appid': appid,
        'secret': secret,
        'js_code': js_code,
        'grant_type': 'authorization_code',
    }
    sess = requests.Session()
    resp = sess.get(url, params=args)

    return json.loads(resp.content.decode("utf-8"))


def user_login(request):
    resp = {}
    js_code = request.GET.get('js_code', None)
    user_token = request.GET.get('user_token', None)
    user_info = request.GET.get('user_info', None)
    try:
        # 有js_code 则user_token不生效
        if js_code is not None:
            wx_data = get_openid(js_code)
            if 'errcode' in wx_data:
                resp['retcode'] = RetCode.WXSRV_ERROR
                return JsonResponse(resp)
            try:
                app_user = AppUser.objects.get(openid=wx_data['openid'])
                resp['user_token'] = app_user.id.hex
            except AppUser.DoesNotExist:
                app_user = AppUser.objects.create()
                app_user.openid = wx_data['openid']
                resp['user_token'] = app_user.id.hex

            app_user.session_key = wx_data['session_key']
            if 'unionid' in wx_data:
                app_user.unionid = wx_data['unionid']
            if user_info:
                app_user.user_info = user_info
            app_user.save()

            resp['retcode'] = RetCode.SUCCESS
            return JsonResponse(resp)
        if user_token is not None:
            try:
                app_user = AppUser.objects.get(pk=user_token)
            except AppUser.DoesNotExist:
                resp['retcode'] = RetCode.USER_NOT_EXIST
                return JsonResponse(resp)
            resp['retcode'] = RetCode.SUCCESS

            if user_info != app_user.user_info:
                app_user.user_info = user_info
                app_user.save()
            return JsonResponse(resp)
    except BaseException as e:
        print(e)
        resp['retcode'] = RetCode.SRV_EXCEPTION
        return JsonResponse(resp)

    resp['retcode'] = RetCode.INVALID_PARA
    return JsonResponse(resp)


class IdiomList(generics.ListAPIView):
    serializer_class = IdiomsSerializer

    def get_queryset(self):
        start = time.clock()
        app_user = self.request.query_params.get('user_token', None)
        count = int(self.request.query_params.get('count', 1))
        if app_user is None:
            return Idioms.objects.all().none()
        try:
            app_user = AppUser.objects.get(pk=app_user)
        except AppUser.DoesNotExist:
            return Idioms.objects.all().none()

        exclude_li = [row.id for row in app_user.quizzed.iterator()]
        li = list(range(Idioms.objects.first().id, Idioms.objects.last().id))
        random.shuffle(li)
        selected_count = 0
        selected_li = []
        for x in li:
            if selected_count == count:
                break
            if x not in exclude_li:
                selected_count += 1
                selected_li.append(x)
                app_user.quizzed.add(x)

        # queryset = Idioms.objects.exclude(appuser__id__exact=app_user.id).raw('SELECT * FROM `idiom_quiz1_idioms` ORDER BY RAND()')[:count]
        # for idiom in queryset:
        #     app_user.quizzed.add(idiom.id)
        # app_user.save()
        queryset = Idioms.objects.filter(id__in=selected_li)
        app_user.save()
        return queryset
