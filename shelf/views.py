from django.shortcuts import render, redirect
from django.contrib import messages
from shelf.models import Book
from django.db.models import Count, Q
from .form import BookForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.


def index(request):
    stats = Book.objects.aggregate(
        all_count=Count('id'),
        currently_reading=Count('id', filter=Q(status='reading')),
        want_to_read=Count('id', filter=Q(status='want')),
        finished=Count('id', filter=Q(status='read')),
    )

    context = {
        'all': stats['all_count'],
        'currently_reading': stats['currently_reading'],
        'want_to_read': stats['want_to_read'],
        'finished': stats['finished'],
    }
    return render(request, 'shelf/home.html', context)

def books(request):
    search, status, author = request.GET.get('search', None), request.GET.get('status', None), request.GET.get('author', None)
    filter_params = {}
    if status:
        filter_params['status'] = status
    if author:
        filter_params['author'] = author
    if search:
        filter_params['title__icontains'] = search
        
    if filter_params:
        books = Book.objects.filter(**filter_params)
    else:
        books = Book.objects.all()
    
    authors = Book.objects.values_list('author', flat=True).distinct()
    
    context = {
        'books': books,
        'authors': authors,
        'statuses': Book.STATUS_CHOICES,
        'selected_status': status,
        'search_query': search,
        'selected_author': author,
    }
    return render(request, 'shelf/books.html', context)
  
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'shelf/book_detail.html', context)
  
@login_required
def add_book(request):
    statuses = Book.STATUS_CHOICES
    context = {
        'statuses': statuses,
    }
    
    if request.POST:
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('shelf:books')
        else:
            messages.error(request, 'Please correct the errors below.')
            context['form'] = form
    else:
        context['form'] = BookForm()
        
    return render(request, 'shelf/add_book.html', context)

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    statuses = Book.STATUS_CHOICES
    context = {
        'book': book,
        'statuses': statuses,
    }
    
    if book.owner is not request.user:
        raise PermissionDenied("You can only edit your own books.")
    
    if not book:
        messages.error(request, 'Book not found!')
        return redirect('shelf:books')

    if request.POST:
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('shelf:books')
        else:
            messages.error(request, 'Please correct the errors below.')
            context['form'] = form
    else:
        context['form'] = BookForm(instance=book)
        
    return render(request, 'shelf/edit_book.html', context)

@login_required
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    
    if book.owner is not request.user:
        raise PermissionDenied("You can only edit your own books.")
        
    
    if not book:
        messages.error(request, 'Book not found!')
        return redirect('shelf:books')
    
    if request.POST and book:
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('shelf:books')
   
    return render(request, 'shelf/delete_book.html', {'book_id': book_id})