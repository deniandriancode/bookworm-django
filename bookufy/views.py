from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator

from urllib.parse import parse_qs

from .models import Book

class HomeView(View):
    def get(self, request):
        return render(request, "bookufy/home.html")

class IndexView(View):
    def get(self, request):
        item_per_page = 4
        qs = parse_qs(request.META["QUERY_STRING"])
        if "page" not in qs:
            page_num = 1
        else:
            page_num = int(qs["page"][0])
        all_books = Book.objects.all().order_by("id")
        pager = Paginator(all_books, item_per_page)
        page = pager.page(page_num)
        page.number_prev = page_num - 1
        page.number_next = page_num + 1
        prev_page = page.has_previous()
        next_page = page.has_next()
        context = {"books": page.object_list, "page": page, "prev": prev_page, "next": next_page}
        return render(request, "bookufy/index.html", context)

class NewBookView(View):
    def get(self, request):
        return render(request, "bookufy/new.html")

    def post(self, request):
        post = request.POST
        title = post['title']
        num_of_page = post['num_of_page']
        author = post.get("author")
        genre = post.get("genre")
        release_year = post.get("release_year")
        score = post.get("score")
        is_public_domain = post.get("is_public_domain")
        note = post.get("note")
        book = Book(
            title=title,
            num_of_page=num_of_page,
            author=author,
            genre=genre,
            release_year=release_year,
            score=score,
            is_public_domain=is_public_domain,
            note=note
        )
        book.save()
        return redirect(reverse("bookufy:detail", args=[book.id]))

class SearchBookView(View):
    def get(self, request):
        item_per_page = 4
        is_search = False
        search_string = ""
        if "search_string" in request.GET:
            search_string = request.GET["search_string"]
            is_search = True

        qs = parse_qs(request.META["QUERY_STRING"])
        if "page" not in qs:
            page_num = 1
        else:
            page_num = int(qs["page"][0])
            
        filtered_books = \
            Book.objects.filter(title__icontains=search_string)  | \
            Book.objects.filter(author__icontains=search_string) | \
            Book.objects.filter(genre__icontains=search_string)  | \
            Book.objects.filter(note__icontains=search_string)
        
        pager = Paginator(filtered_books, item_per_page)
        page = pager.page(page_num)
        page.number_prev = page_num - 1
        page.number_next = page_num + 1
        prev_page = page.has_previous()
        next_page = page.has_next()
        prev_url = f"?search_string={search_string}&page={page.number_prev}"
        next_url = f"?search_string={search_string}&page={page.number_next}"
        context = {"filtered_books": page.object_list,
                   "page": page, "prev": prev_page, "next": next_page,
                   "prev_url": prev_url, "next_url": next_url, 
                   "search_string": search_string, "is_search": is_search,
                   "query": request.META["QUERY_STRING"]}
        return render(request, "bookufy/search.html", context)

class EditBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        print(book.is_public_domain)
        context = {"book": book}
        return render(request, "bookufy/edit.html", context)

    def post(self, request, book_id):
        post = request.POST
        book = get_object_or_404(Book, pk=book_id)
        book.title = post["title"]
        book.num_of_page = post["num_of_page"]
        book.author = post.get("author")
        book.genre = post.get("genre")
        book.release_year = post.get("release_year")
        book.score = post.get("score")
        book.is_public_domain = post.get("is_public_domain")
        book.note = post.get("note")
        book.save()
        return redirect(reverse("bookufy:detail", args=[book.id]))

class DetailBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        context = {"book": book}
        return render(request, "bookufy/detail.html", context)
    
class DeleteBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return redirect(reverse("bookufy:index"))
