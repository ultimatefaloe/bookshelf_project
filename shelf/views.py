from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'shelf/home.html')
  
def books(request):
    return render(request, 'shelf/books.html')
  
def book_detail(request, book_id):
    return render(request, 'shelf/book_detail.html', {'book_id': book_id})
  
def add_book(request):
    return render(request, 'shelf/add_book.html')

def edit_book(request, book_id):
    return render(request, 'shelf/edit_book.html', {'book_id': book_id})

def delete_book(request, book_id):
    return render(request, 'shelf/delete_book.html', {'book_id': book_id})