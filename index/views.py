import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

from index.models import TCategory, TBook


def index(request):
    levels1 = TCategory.objects.filter(level=1)
    levels2 = TCategory.objects.filter(level=2)
    today = datetime.date.today()
    print(today)
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    new_books = TBook.objects.all().order_by('-make_time')[:8]
    hot_books1 = TBook.objects.filter(make_time__gte=last_month).order_by('-sell_count')[:5]
    # books1 = sorted(books1, key=lambda item: item.sales_nummber, reverse=True)   第二种方法
    great_books = TBook.objects.all().order_by('-flow')[:10]
    hot_books2 = TBook.objects.filter(flow__gte=3000).order_by('-sell_count')[:5]
    return render(request, 'index.html',
                  {'levels1': levels1, 'levels2': levels2, 'new_books': new_books, 'hot_books1': hot_books1,
                   'great_books': great_books, 'hot_books2': hot_books2})


def booklist(request, id):
    levels1 = TCategory.objects.filter(level=1)
    levels2 = TCategory.objects.filter(level=2)

    level1 = TCategory.objects.filter(id=id)[0]
    if level1.level == 2:
        level2 = ' > ' + TCategory.objects.filter(id=level1.parent_id)[0].class_name
    else:
        level2 = ''

    level = TCategory.objects.filter(id=id)[0].level
    if level == 1:
        if TCategory.objects.filter(parent_id=id).count():
            books = TBook.objects.filter(category__parent_id=id)
        else:
            books = TBook.objects.filter(category__id=id)
    else:
        books = TBook.objects.filter(category=id)

    num = request.GET.get('num', 1)
    paginator = Paginator(books, per_page=2)
    page = paginator.page(int(num))
    return render(request, 'booklist.html',
                  {'levels1': levels1, 'levels2': levels2, 'level1': level1, 'level2': level2, 'books': books,
                   'page': page, 'id': int(id)})


def details(request, id):
    c_id = TBook.objects.filter(id=id)[0].category_id
    level1 = TCategory.objects.filter(id=c_id)[0]
    if level1.level == 2:
        level2 = ' > ' + TCategory.objects.filter(id=level1.parent_id)[0].class_name
    else:
        level2 = ''
    book = TBook.objects.filter(id=id)[0]
    return render(request, 'Book details.html', {'level1': level1, 'level2': level2, 'book': book, 'id': c_id})