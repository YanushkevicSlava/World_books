from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Book, Author, BookInstance
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import FormAddAuthor, FormEditAuthor
from django.urls import reverse


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    # Универсальный класс представления списка книг,
    # находящихся в заказе у текущего пользователя.
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


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
    # Число посещений главной страницы
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # словарь для передачи данных в шаблон index.html
    context = {
        'text_head': text_head,
        'books': books,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'authors': authors,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'catalog/index.html', context)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    context_object_name = 'book'


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


def edit_authors(request):
    author = Author.objects.all()
    context = {
        'author': author,
    }
    return render(request, 'catalog/edit_authors.html', context=context)


def add_author(request):
    if request.method == 'POST':
        form = FormAddAuthor(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            about = form.cleaned_data.get("about")
            photo = form.cleaned_data.get("photo")
            obj = Author.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                about=about,
                photo=photo,
            )
            obj.save()
            return HttpResponseRedirect(reverse('authors-list'))
    else:
        form = FormAddAuthor()
        context = {"form": form}
        return render(request, "catalog/authors_add.html", context=context)


def delete(request, id):
    obj = Author.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect("/edit_authors/")


def edit_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        instance = Author.objects.get(id=id)
        form = FormEditAuthor(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/edit_authors/")
    else:
        form = FormEditAuthor(instance=author)
        content = {"form": form}
        return render(request, "catalog/edit_author.html", content)


def edit_books(request):
    book = Book.objects.all()
    context = {"book": book}
    return render(request, "catalog/edit_books.html", context=context)


