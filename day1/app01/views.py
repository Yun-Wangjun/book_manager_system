from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from app01 import models
# Create your views here.


# 首页
def home(request):
    return render(request, "index.html")


# 用户登录
def acc_login(request):
    if request.method == "POST":
        username = request.POST.get("user_email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print("********user:{}*********".format(user))
        if user:
            login(request, user)
            return redirect("/publisher_list/")
        # if user_email == "test@163.com" and password == "test123456":
        #     return redirect("/publisher_list/")
        return render(request, 'user/login.html')
    return render(request, 'user/login.html')


# 用户退出
def acc_logout(request):
    logout(request)
    # 跳转到登录界面
    return redirect("/login/")


# 展示所有的出版社信息
@login_required
def publisher_list(request):
    # 去数据库查出所有的出版社，填充到HTML中，给用户返回
    # order_by('id')按id排序
    ret = models.Publisher.objects.all().order_by('id')

    return render(request, 'publisher/publisher_list.html', {"publisher_list": ret, })


# 添加出版社信息
@login_required
def add_publisher(request):
    if request.method == "POST":
        new_name = request.POST.get('publisher_name').strip()
        new_addr = request.POST.get('publisher_addr').strip()
        if new_name and new_addr:

            # 通过ORM在数据库中新建一条记录
            models.Publisher.objects.create(name=new_name,addr=new_addr)
            # 跳转到出版社信息展示页面，查看是否添加成功
            return redirect("/publisher_list/")
        else:
            error_msg = "出版社名称和地址均不能为空"
            return render(request, 'publisher/add_publisher.html', {'error_msg':error_msg})
    return render(request, 'publisher/add_publisher.html')


# 删除出版社信息
@login_required
def delete_publisher(request):
    # 删除指定的数据
    # 1、从GET请求的参数里面拿到将要删除的数据的ID值
    del_id = request.GET.get('id', None)
    # 如果能取到id值
    if del_id:
        # 去数据库删除当前id值的数据
        # 根据id值查找到数据
        # del_obj = models.Publisher.objects.get(id=del_id)
        del_obj = models.Publisher.objects.filter(id=del_id)
        # 删除
        del_obj.delete()
        # 推荐写法 models.Publisher.objects.get(id=del_id).delete()
        # 跳转到出版社信息页面查看是否删除
        return redirect('/publisher_list/')
    else:
        return HttpResponse("要删除的数据不存在")


# 编辑出版社信息
@login_required
def edit_publisher(request):
    # 获取修改后的出版社名字
    if request.method == "POST":
        publisher_id = request.POST.get('publisher_id')
        new_name = request.POST.get('publisher_name').strip()
        new_addr = request.POST.get('publisher_addr').strip()
        if new_name and new_addr:
            # 根据id获取编辑的出版社对象
            edit_obj = models.Publisher.objects.get(id=publisher_id)
            edit_obj.name = new_name  # 更新name属性
            edit_obj.addr = new_addr
            edit_obj.save()  # 把修改提交到数据库
            # 跳转出版社信息页面，查看是否修改
            return redirect("/publisher_list/")
        else:
            error_msg = "名称和地址均不能为空"
            return render(request, 'publisher/edit_publisher.html', {'error_msg': error_msg})
    # 从GET请求中的url获取参数
    edit_id = request.GET.get('id')
    # 根据edit_id获取到当前编辑的出版社对象
    publisher_obj = models.Publisher.objects.get(id=edit_id)
    return render(request, 'publisher/edit_publisher.html', {"publisher_obj": publisher_obj, })


# 测试GET方法获取数据
def test(request):
    print(request.GET)
    print(request.GET.get('id'))
    print(request)

    return HttpResponse("ok")


# 展示书信息
@login_required
def book_list(request):
    # 从数据库获取书的信息
    ret = models.Book.objects.all()
    return render(request, 'book/book_list.html', {"book_list": ret, })


# 添加书
@login_required
def add_book(request):
    if request.method == "POST":
        # {'title': ['汉字之美'], 'publisher': ['10']}
        new_title = request.POST.get('title').strip()
        publisher_id = request.POST.get('publisher')
        # 查看用户输入的是否为空值
        if new_title:
            # 创建新书对象自动提交
            models.Book.objects.create(title=new_title, publisher_id=publisher_id)
            # 使用出版社对象提交
            # publisher_obj = models.Publisher.objects.get(id=publisher_id)
            # models.Book.objects.create(title=new_title, publisher=publisher_obj)
            # 跳转到书籍信息展示页面 查看是否添加成功
            return redirect("/book_list/")
        error_msg = "书籍名称不能为空"
        publisher_list = models.Publisher.objects.all()
        return render(request, "book/add_book.html", {'error_msg': error_msg, 'publisher_list':publisher_list})
    # 获取所有的出版社信息
    publisher_list = models.Publisher.objects.all()
    print("*****{}****".format(request.POST))
    return render(request, 'book/add_book.html', {"publisher_list": publisher_list, })


# 删除书
@login_required
def delete_book(request):
    # url中获取要操作的书的id
    del_id = request.GET.get("id")
    if del_id:
        models.Book.objects.get(id=del_id).delete()
        # 跳转到书的信息页面看是否删除
        return redirect("/book_list/")


# 编辑书
@login_required
def edit_book(request):
    if request.method == "POST":
        new_title = request.POST.get('title').strip()
        publisher_id = request.POST.get('publisher')
        edit_id = request.POST.get('id')
        if new_title:
            # 更新书的信息
            edit_obj = models.Book.objects.get(id=edit_id)
            edit_obj.title = new_title
            edit_obj.publisher_id = publisher_id
            # 将修改提交到数据库
            edit_obj.save()
            # 跳转到书的信息页面查看是否更新
            return redirect("/book_list/")

        publisher_list = models.Publisher.objects.all()
        return render(request, 'book/edit_book.html', {'error_msg': "书籍名称不能为空", 'publisher_list': publisher_list,})
    # 用户要编辑书的id
    edit_id = request.GET.get('id')
    # 编辑的书对象
    edit_book = models.Book.objects.get(id=edit_id)
    # 获取所有的出版社信息
    publisher_list = models.Publisher.objects.all()
    return render(request, 'book/edit_book.html', {"publisher_list": publisher_list, "edit_book": edit_book, })


# 测试
def book_test(request):
    book_list = models.Book.objects.all()
    # for i in book_list:
    #     print(i)
    #     print(i.title)
    #     print(i.publisher)
    #     print(i.publisher.name)
    #     print(i.publisher.addr)
    #     print("=" * 20)
    new_book_obj = models.Book.objects.create(
        title="余罪",
        publisher_id=10)
    print("####{}####".format(new_book_obj))
    return HttpResponse("ok")


# 获取作者信息
@login_required
def author_list(request):
    author_obj = models.Author.objects.get(id=1)
    print(author_obj.book.all())
    print('#' * 200)
    # 查询所有作者
    all_author = models.Author.objects.all()
    return render(request, 'author/author_list.html', {'author_list': all_author, })


# 添加作者
@login_required
def add_author(request):
    if request.method == "POST":
        # 获取新的作者name
        new_author_name = request.POST.get('author_name').strip()
        # 获取新作者的作品
        # 获取多个值时用getlist(如多选的checkbox或多选的select),
        # 单个值用get
        new_books = request.POST.getlist('book_list')
        print("new_author_name:", new_author_name)
        print("new_books:", new_books)
        if new_author_name and new_books:
            # 添加新作者到数据库
            new_author_obj = models.Author.objects.create(name=new_author_name)
            # 添加新作者与其作品的对应关系到数据库
            new_author_obj.book.set(new_books)
            # 跳转至作者列表，查看是否添加成功
            return redirect("/author_list/")
        ret = models.Book.objects.all()
        return render(request, "author/add_author.html", {'error_msg': "作家姓名和作品均不能为空", 'book_list': ret})

    # 获取所有的书
    ret = models.Book.objects.all()
    print(f'request:{request.POST.get}')
    return render(request, 'author/add_author.html', {'book_list': ret})


# 删除作者
@login_required
def delete_author(request):
    # 从URL中获取要删除作者的id
    delete_id = request.GET.get("id")
    # 根据delete_id获取要删除的对象，然后直接删除
    # 删除过程1、去作者和书的关系表中，删除关联记录
    # 2、去作者表中删除作者信息
    models.Author.objects.get(id=delete_id).delete()
    # 跳转至author_list页面,查看是否删除成功
    return redirect("/author_list/")


# 编辑作者
@login_required
def edit_author(request):
    if request.method == "POST":
        new_author_name = request.POST.get("author_name").strip()
        print('new_author_name:', new_author_name)
        # 拿到编辑后作者关联的书
        new_books = request.POST.getlist("book_list")
        # 拿到编辑作者的id
        edit_id = request.POST.get("author_id")
        if new_author_name and new_books:
            # 根据id获取编辑对象
            edit_obj = models.Author.objects.get(id=edit_id)
            # 根据对象设置编辑后的作者的name属性
            edit_obj.name = new_author_name
            # 根据对象设置编辑后的作者与书的对应关系
            edit_obj.book.set(new_books)
            # 将修改保存到数据库
            edit_obj.save()
            # 跳转至author_list页面查看是否编辑成功
            return redirect("/author_list/")
            # 获取书库所有书籍
        book_list = models.Book.objects.all()
        return render(request, 'author/edit_author.html', {'error_msg': "作家名称及作品均不能为空", 'book_list': book_list})
    # 从URL中获取要编辑作者的id
    edit_id = request.GET.get("id")
    edit_obj = models.Author.objects.get(id=edit_id)
    # 获取书库所有书籍
    book_list = models.Book.objects.all()
    print("********{}******".format(edit_obj.book.all()))
    return render(request, 'author/edit_author.html', {'edit_obj': edit_obj, 'book_list': book_list})

