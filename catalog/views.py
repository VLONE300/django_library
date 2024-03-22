import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from catalog.models import Book, Author, BookInstance
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


class ReservationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book_instance = get_object_or_404(BookInstance, pk=pk)
        borrower = request.user

        overdue_books = BookInstance.objects.filter(
            Q(borrower=borrower),
            Q(status='On loan'),
            Q(reservation_start_date__lt=timezone.now() - datetime.timedelta(days=14))
        )

        if overdue_books.exists():
            messages.error(
                request,
                'You have books that you have held back for more than 2 weeks. Return them before you book other books.')
            return redirect(book_instance.get_absolute_url())

        if book_instance.status == 'Available':
            book_instance.borrower = borrower
            book_instance.status = 'On loan'
            book_instance.reservation_start_date = timezone.now()
            book_instance.due_back = timezone.now() + datetime.timedelta(days=14)
            book_instance.save()
        return redirect(book_instance.get_absolute_url())

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
