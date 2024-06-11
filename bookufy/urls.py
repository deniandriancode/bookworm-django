from django.urls import path
from . import views

app_name = "bookufy"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("new/", views.NewBookView.as_view(), name="new"),
    path("search/", views.SearchBookView.as_view(), name="search"),
    path("edit/<int:book_id>/", views.EditBookView.as_view(), name="edit"),
    path("detail/<int:book_id>/", views.DetailBookView.as_view(), name="detail"),
    path("delete/<int:book_id>/", views.DeleteBookView.as_view(), name="delete"),
]
