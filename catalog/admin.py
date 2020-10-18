from django.contrib import admin
from .models import Genre,Language,Book,Author,BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['last_name','first_name',('date_of_birth','date_of_death')]


class BookInstanceInline(admin.StackedInline):
    model = BookInstance
    extra = 1
    fieldsets = (
        (None,{
            'fields': ('id','book','imprint')
        }),
        ('Availability',{
            'fields': ('status','due_back')
        }),
    )

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','id','colored_status','due_back')
    fieldsets = (
        (None,{
            'fields': ('id','book','imprint')
        }),
        ('Availability',{
            'fields': ('status','due_back')
        }),
    )
    list_filter = ('status','due_back')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BookInstanceInline]


admin.site.register(Genre)
admin.site.register(Language)