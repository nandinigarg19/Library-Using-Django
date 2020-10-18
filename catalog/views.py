from django.shortcuts import render
from django.views import generic

from catalog.models import Book, BookInstance, Author, Genre

from catalog.filters import BookFilter, AuthorFilter

def index(request):
    
    # Total number of books and book instances
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Number of instances available with status as 'a'
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # 'all' is implied by default
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }

    return render(request, 'catalog/index.html', context= context)


class BookListView(generic.ListView):
    model = Book
    # by default, it searches for a template in 
    # LocalLibrary/catalog/templates/catalog/book_list.html
    # Also, the default template variable is object_list or book_list
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book
    # by default, it searches for a template in 
    # LocalLibrary/catalog/templates/catalog/book_detail.html
    # Also, the default template variable is object or book

class AuthorListView(generic.ListView):
    model = Author
    # by default, it searches for a template in 
    # LocalLibrary/catalog/templates/catalog/author_list.html
    # Also, the default template variable is object_list or author_list
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    # by default, it searches for a template in 
    # LocalLibrary/catalog/templates/catalog/author_detail.html
    # Also, the default template variable is object or author

def searchBook(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET,queryset = book_list)
    return render(request,'catalog/book_filter.html',{'book_filter': book_filter})

def searchAuthor(request):
    author_list = Author.objects.all()
    author_filter = AuthorFilter(request.GET,queryset = author_list)
    print(request.GET)
    return render(request,'catalog/author_filter.html',{'author_filter': author_filter})