from catalog.models import Book, BookInstance, Author, Genre, Language
import django_filters

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr = 'icontains')
    class Meta:
        model = Book
        fields = ['title','author','genre','language'] 

class AuthorFilter(django_filters.FilterSet):
    book_title = django_filters.CharFilter(lookup_expr = 'icontains')
    book_genre = django_filters.ModelChoiceFilter(queryset = Genre.objects.all())
    book_language = django_filters.ModelChoiceFilter(queryset = Language.objects.all())
    class Meta:
        model = Author
        fields = ['first_name','last_name','book_title','book_genre','book_language']
