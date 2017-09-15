# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/5/3 16:01'

from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from mxzx.settings import EMAIL_FROM


def code_generator(code_length):
    code = ''
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    length = len(pool) - 1
    random = Random()
    for i in range(code_length):
        code += pool[random.randint(0,length)]
    return code


def send_register_mail(email):
    email_record = EmailVerifyRecord()
    code = code_generator(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = 'register'
    email_record.save()

    email_title = '名校在线：注册激活链接'
    email_body = '点击链接以激活:http://www.zenofpy.cn/activate/{0}'.format(code)

    send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
    if send_status:
        pass


def send_forgetpwd_mail(email):
    email_record = EmailVerifyRecord()
    code = code_generator(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = 'forget'
    email_record.save()

    email_title = '名校在线：重置密码链接'
    email_body = '点击链接以重置密码:http://www.zenofpy.cn/RedirectToReset/{0}'.format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass

def send_update_mail(email):
    email_record = EmailVerifyRecord()
    code = code_generator(4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = 'update'
    email_record.save()
    email_title = '名校在线：你正在更改绑定邮箱'
    email_body = '你正在更改绑定邮箱，验证码:{0}'.format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass
