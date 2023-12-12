from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance
from django.views.generic import ListView, DetailView


def index(request):
    text_head = 'На нашем сайте вы можете получить книги в электронном виде'
    # Данные о книгах и их количестве
    books = Book.objects.all()
    num_books = Book.objects.all().count()
    # Данные о эземплярах книг в БД
    num_instances = BookInstance.objects.all().count
    # Доступные книги (status = 'На складе')
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    # Данные об авторах книг
    authors = Author.objects.all()
    num_authors = Author.objects.all().count()
    # словарь для передачи данных в шаблон index.html
    context = {
        'text_head': text_head,
        'books': books,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'authors': authors,
        'num_authors': num_authors,
    }
    return render(request, 'catalog/index.html', context)


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 3


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'


class AuthorListView(ListView):
    model = Author
    paginate_by = 4
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'


def about(request):
    text_head = 'Сведения о компании'
    name = 'Интелектуальные системы'
    rab1 = 'Разработка приложений на основе AI'
    rab2 = 'Распознование дорожных обьектов'
    rab3 = 'Создание АРТ обьектов на основе AI'
    rab4 = 'Выпуск электронных книг'
    context = {
        'text_head': text_head,
        'name': name,
        'rab1': rab1,
        'rab2': rab2,
        'rab3': rab3,
        'rab4': rab4,
    }
    return render(request, 'catalog/about.html', context=context)


def contact(request):
    text_head = 'Контакты'
    name = 'Интелектуальные системы'
    address = '////.....////'
    email = 'aisoft@ai.com'
    tel = '+2252666636363'
    context = {
        'text_head': text_head,
        'name': name,
        'address': address,
        'email': email,
        'tel': tel,
    }
    return render(request, 'catalog/contact.html', context=context)
