from django.shortcuts import render, redirect
from django.contrib import messages
from shelf.models import Book
from django.db.models import Count, Q

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
  
def add_book(request):
    statuses = Book.STATUS_CHOICES
    context = {
        'statuses': statuses,
    }
    
    if request.POST:
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        status = request.POST.get('status')
        isbn = request.POST.get('isbn') == 'on'
        isbn_number = request.POST.get('isbn_number') if isbn else None
        cover = request.FILES.get('cover')
        
        if not title or not author or not description or not status:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'shelf/add_book.html', context)

        book = Book(
            title=title,
            author=author,
            description=description,
            status=status,
            isbn=isbn,
            isbn_number=isbn_number,
            cover=cover
        )
        book.save()
        messages.success(request, 'Book added successfully!')
        return redirect('shelf:books')
    
    return render(request, 'shelf/add_book.html', context)

def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    statuses = Book.STATUS_CHOICES
    context = {
        'book': book,
        'statuses': statuses,
    }

    if request.POST:
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.status = request.POST.get('status')
        book.isbn = request.POST.get('isbn') == 'on'
        book.isbn_number = request.POST.get('isbn_number') if book.isbn else None
        cover = request.FILES.get('cover')
        if cover:
            book.cover = cover
            
        if not book.title or not book.author or not book.description or not book.status:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'shelf/edit_book.html', context)
         
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('shelf:book_detail', book_id=book.id)
    
    return render(request, 'shelf/edit_book.html', context)

def delete_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('shelf:books')
    return render(request, 'shelf/delete_book.html', {'book_id': book_id})