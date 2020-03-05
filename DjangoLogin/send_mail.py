import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoLogin.settings'
if __name__ == '__main__':

#一、在Django中发送邮件
    #对于send_mail方法，
    # 第一个参数是邮件主题subject；
    # 第二个参数是邮件具体内容；
    # 第三个参数是邮件发送方，需要和你settings中的一致；
    # 第四个参数是接受方的邮件地址列表。请按你自己实际情况修改发送方和接收方的邮箱地址。

    # send_mail('Subject here', 'Here is the message.', 'wengmq5216@sina.com',
    # ['wengmq@163.com'], fail_silently=False)




#二、发送HTML格式的邮件
    #通常情况下，我们发送的邮件内容都是纯文本格式。
    # 但是很多情况下，我们需要发送带有HTML格式的内容，
    # 比如说超级链接。一般情况下，为了安全考虑，
    # 很多邮件服务提供商都会禁止使用HTML内容，
    # 幸运的是对于以http和https开头的链接还是可以点击的。
    #下面是发送HTML格式的邮件例子。
    subject, from_email, to = '来自Django的测试邮件', 'wengmq5216@sina.com', 'wengmq@163.com'
    text_content = '欢迎访问我的Django！！'
    html_content = '<p>欢迎访问<a href="http://www.wengmq.top" target=blank>www.wengmq.top</a>wengmq的个人网站</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



