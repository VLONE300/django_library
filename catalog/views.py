from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic import ListView, DetailView


def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='Available').count()

    return render(request, 'index.html', {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_book_instances': num_book_instances,
        'num_instances_available': num_instances_available
    })


class AuthorListView(ListView):
    model = Author
    template_name = 'authors_list.html'
    context_object_name = 'authors_list'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detailed.html'


class BookListView(ListView):
    model = Book
    template_name = 'books_list.html'
    context_object_name = 'books_list'


class BookDetailView(DetailView):
    model = Book
    template_name = 'detailed_book.html'


class BookInstanceDetailView(DetailView):
    model = BookInstance
    template_name = 'book_instance.html'
