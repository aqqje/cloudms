from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, StreamingHttpResponse
import os
from datetime import  datetime
from django.template import Template, Context
# Create your views here.
def msgproc(request):
    datalist = []
    if request.method == 'POST':
        userA = request.POST.get('userA', None)
        userB = request.POST.get('userB', None)
        msg = request.POST.get('msg', None)
        time = datetime.now()
        with open('msgdate.txt', 'a+') as f:
            f.write('{}--{}--{}--{}--\n'.format(userA, userB,\
                msg, time.strftime('%Y-%m-%d %H:%M:%S')))

    if request.method == 'GET':
        userC = request.GET.get('userC', None)
        if userC != None:
            with open('msgdate.txt', 'r') as f:
                cnt = 0
                for line in f:
                    linedata = line.split('--')
                    if linedata[0] == userC:
                        cnt = cnt+1
                        d = {'userA':linedata[1],'msg':linedata[2],'time':linedata[3]}
                        datalist.append(d)
                    if cnt >= 10:
                        break
    return render(request, 'MsgSingleWeb.html', {'data':datalist})


def homeproc(request):
    reponse = HttpResponse()
    reponse.write("<h1>这是首页，具体功能请访问<a href='./msggata/'>这里</a><h1>")
    reponse.write("这是第二行！")
    return reponse
    #return HttpResponse("<h1>这是首页，具体功能请访问<a href='./msggata/'>这里</a><h1>")

def homeproc1(request):
    response = JsonResponse({'key': 'value1'})
    return response

def homeproc2(request):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reponse = FileResponse(open(cwd + '/msgapp/templates/1.jpeg', 'rb'))
    reponse['Content-Type'] = 'application/octet-stream'  # 指定指定文件类型
    reponse['COntent-Disposition'] = 'attachment;filename="1.jpeg"' # 指定文件名称
    return  reponse

def file_downloa(request):
    # do something...
    with open('msgdate.txt') as f:
        c = f.read()
    return HttpResponse(c)

def big_file_download(request):
    #do something...
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    fname = 'msgdate.txt'
    response = StreamingHttpResponse(file_iterator(fname))
    return response

def pgproc(request):
    template = Template("<h1>这个程序的名字是{{ name }}</h1>")
    context = Context({"name": "实验平台"})
    return HttpResponse(template.render(context))

'''
模板语言 --- 注释

单行注释： {# 这是单行注释 #}

多行注释： {% comment %}
            这是多行注释第一行
            这是多行注释第二行
          {% endcomment %}
          
模板语言 --- 变量

变量
    {{ name }}
    
v如果变量本身是字典类型，列表类型或对象，用.获取元素

    {{ adict.key}}  {{alist.0}}  {{object.attribute}}
    
模板语言 ---标签

标签 
    {{% 关键字引导的程序 %}}
    
标签中的关键字包括
    for, endfor, block, endblock, if, elif, else, endif, in, trans, as, with, extends ...
'''