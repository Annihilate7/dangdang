from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from index.models import TCar, TBook, TUser


class Book:
    def __init__(self, id, count):
        book = TBook.objects.get(pk=id)
        self.id = id
        self.name = book.book_name
        self.count = count
        self.price = book.new_price
        self.pic = book.book_pic


class Car:
    def __init__(self):
        self.book_list = []

    def get_book(self, id):
        for book in self.book_list:
            if book.id == id:
                return book

    def add_book(self, id, count):
        book = self.get_book(id)
        if book:
            book.count += count
        else:
            book = Book(id=id, count=count)
            self.book_list.append(book)

    def remove_book(self, id):
        book = self.get_book(id)
        self.book_list.remove(book)


def car(request):
    username = request.session.get('username')
    if username:
        books = []
        user = TUser.objects.get(user_name=username)
        car_books = request.session.get('car')
        if car_books:
            for book in car_books.book_list:
                if TCar.objects.filter(book_id=book.id):
                    car = TCar.objects.filter(book_id=book.id)[0]
                    car.count = car.count + book.count
                    car.save()
                else:
                    with transaction.atomic():
                        TCar.objects.create(count=book.count, user_id=user.id, book_id=book.id)
            del request.session['car']
        cars = TCar.objects.filter(user_id=user.id)
        for car in cars:
            book = Book(car.book_id, car.count)
            books.append(book)
        page = request.GET.get('page')
        if page:
            return redirect('order:indent')
        return render(request, 'car.html', {'books': books})
    else:
        books = request.session.get('car')
        if books:
            return render(request, 'car.html', {'books': books.book_list})
        return render(request, 'car.html', {'books': books})


def add_car(request):
    count = int(request.POST.get('count'))
    id = request.POST.get('book_id')
    username = request.session.get('username')
    if username:
        user = TUser.objects.get(user_name=username)
        if TCar.objects.filter(book_id=id, user_id=user.id):
            car = TCar.objects.filter(book_id=id, user_id=user.id)[0]
            car.count = car.count + count
            car.save()
        else:
            with transaction.atomic():
                TCar.objects.create(count=count, user_id=user.id, book_id=id)
    else:
        car = request.session.get('car')
        if not car:
            car = Car()
        car.add_book(id, count)
        request.session['car'] = car
    return HttpResponse('yes')


def del_car(request):
    id = request.POST.get('book_id')
    username = request.session.get('username')
    if username:
        user = TUser.objects.get(user_name=username)
        car = TCar.objects.get(user_id=user.id, book_id=id)
        car.delete()
    else:
        car = request.session.get('car')
        car.remove_book(id)
        request.session['car'] = car
    return HttpResponse('yes')
