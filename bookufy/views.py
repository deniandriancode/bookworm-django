from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import Book

class HomeView(View):
    def get(self, request):
        return render(request, "bookufy/home.html")

class IndexView(View):
    def get(self, request):
        all_books = Book.objects.all().order_by("id")
        context = {"books": all_books}
        return render(request, "bookufy/index.html", context)

class NewBookView(View):
    def get(self, request):
        return render(request, "bookufy/new.html")

    def post(self, request):
        print(request.POST)
        title = request.POST['title']
        num_of_page = request.POST['num_of_page']
        book = Book(title=title, num_of_page=num_of_page)
        book.save()
        return redirect(reverse("bookufy:index"))

class EditBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        context = {"book": book}
        return render(request, "bookufy/edit.html", context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.title = request.POST["title"]
        book.num_of_page = request.POST["num_of_page"]
        book.save()
        return redirect(reverse("bookufy:index"))

class DeleteBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return redirect(reverse("bookufy:index"))
