from django.shortcuts import render
from movieApp.models import *


def movie(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        director = request.POST.get('director')
        year = request.POST.get('year')
        rating = request.POST.get('rating')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')

        # Create a new Movie object
        New_movie = movie(
            title=title,
            director=director,
            year=year,
            rating=rating,
            duration=duration,
            genre=genre
        )

        New_movie.save()
    return render(request, 'addmovie.html')