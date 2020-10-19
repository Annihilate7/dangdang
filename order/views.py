import time

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from index.models import TAddress, TUser, TCar, TBook, TOrder, TOrderItem


class Book:
    def __init__(self, id, count):
        book = TBook.objects.get(pk=id)
        self.id = id
        self.name = book.book_name
        self.press = book.press
        self.price = book.new_price
        self.discount = book.discount
        self.count = count
        self.total = self.price * self.count


def indent(request):
    # all_price = request.GET.get('all_price')
    username = request.session.get('username')
    user = TUser.objects.get(user_name=username)
    address = TAddress.objects.filter(user_id=user.id)
    cars = TCar.objects.filter(user_id=user.id)
    books = []
    books_count = 0
    all_price = 0
    for car in cars:
        book = Book(car.book_id, car.count)
        books_count += book.count
        all_price += book.count * book.price
        books.append(book)
    return render(request, 'indent.html', {'address': address, 'all_price': all_price, 'books_count': books_count, 'books': books})


def add_address(request):
    username = request.session.get('username')
    user = TUser.objects.get(user_name=username)
    man = request.POST.get('man')
    address = request.POST.get('address')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    telephone = request.POST.get('telephone')
    if TAddress.objects.filter(user_id=user.id, address=address):
        return HttpResponse('no')
    with transaction.atomic():
        TAddress.objects.create(order_user=man, address=address, post_code=email, phone=phone, telephone=telephone, user_id=user.id)
    return HttpResponse('yes')


def choce(request):
    address = request.POST.get('address')
    add = TAddress.objects.get(address=address)
    def mydefault(u):
        if isinstance(u,TAddress):
            return {'man':u.order_user,'address':u.address,'email':u.post_code,'phone':u.phone,'telephone':u.telephone}
    return JsonResponse({'address':add},safe=False,json_dumps_params={'default':mydefault})


def return_car(request):
    username = request.session.get('username')
    user = TUser.objects.get(user_name=username)
    book_name = request.POST.get('name')
    book = TBook.objects.get(book_name=book_name)
    cars = TCar.objects.filter(user_id=user.id, book_id=book.id)
    books = request.session.get('books')
    if not books:
        books = []
    for car in cars:
        books.append(car)
    request.session['books'] = books
    return HttpResponse('yes')


def get_order_code():
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    return order_no


def indent_ok(request):
    username = request.session.get('username')
    books = request.session.get('books')
    user = TUser.objects.get(user_name=username)
    count = request.GET.get('books_count')
    price = float(request.GET.get('all_price'))
    code = request.GET.get('code')
    taddress = TAddress.objects.filter(user_id=user.id, post_code=code)[0]
    order_user = taddress.order_user
    cars = TCar.objects.filter(user_id=user.id)
    with transaction.atomic():
        order = TOrder.objects.create(order_item=str(int(time.time()*1000))+str(int(time.clock()*1000000)), price=price, user_id=user.id, address_id=taddress.id)
    for car in cars:
        if books:
            for book in books:
                if car != book:
                    with transaction.atomic():
                        car.delete()
        else:
            with transaction.atomic():
                car.delete()
    del request.session['books']
    return render(request, 'indent ok.html', {'order': order, 'count': count, 'user': order_user})