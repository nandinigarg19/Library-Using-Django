from django.db import models
from django.urls import reverse
from django.utils.html import format_html
import uuid
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction)")

    def __str__(self):
        return self.name

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book's Natural language (e.g. Hindi, English, French, etc.)")

    def __str__(self):
        return self.name

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering=['first_name','last_name']

    def __str__(self):
        return '{0} {1}'.format(self.first_name,self.last_name)
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def get_books(self):
        return Book.objects.filter(author=self)

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter a book title")
    summary = models.TextField(max_length=1000, help_text="Enter a brief summary of the book")
    # We can also add html tags in help text like <a> in isbn
    isbn = models.CharField(verbose_name="ISBN", max_length=13, help_text="13 digit <a href='https://www.isbn-international.org/content/what-isbn'>ISBN Number</a>")
    # Foreign key relationship models are specified within strings like 'Author' or 'Language'
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    # Many to Many relationship models are specified as objects like Genre
    genre = models.ManyToManyField(Genre, help_text="Select a Genre for this field")

    def __str__(self):
        return self.title

    # Display the 3 or lesser genres in admin site as strings
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_available_copies(self):
        return BookInstance.objects.filter(book=self).filter(status='a')

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

class BookInstance(models.Model):
    # Globally unique ids for each book instance 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m','Maintainence'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,null=True,default='m',help_text="Book Availability")
    
    class Meta:
        ordering=['due_back']

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

    # to specify if book is overdue or not
    @property
    def is_overdue(self):
        if self.due_back and self.due_back < date.today():
            return True
        return False

    def colored_status(self):
        if(self.is_overdue):
            # For every field that has choices set, the object will have a 
            # get_FOO_display() method, where FOO is the name of the field. 
            # This method returns the “human-readable” value of the field.
            # For eg., here FOO= status
            return format_html('<span style="color: #{};">{}</span>',"FF0000",self.get_status_display())
        return self.get_status_display()
    


