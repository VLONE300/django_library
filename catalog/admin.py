from django.contrib import admin
from catalog.models import Author, Genre, Language, Book, BookInstance, Country


class BookInLine(admin.TabularInline):
    model = Book


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance


# @admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'pseudonym']
    search_fields = ['first_name', 'last_name', 'pseudonym']
    inlines = [BookInLine]


# @admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genre']
    search_fields = ['title', 'author__pseudonym', 'author__first_name', 'author__last_name', 'genre__name']
    inlines = [BookInstanceInLine]


# @admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'isbn', 'status', 'borrower')
    fieldsets = (
        ('Group 1', {
            'fields': ('book', 'isbn', 'language')
        }),
        ('Group 2', {
            'fields': ('borrower', 'reservation_start_date', 'due_back', 'status')
        }),
    )


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
