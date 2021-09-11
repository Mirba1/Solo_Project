from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


def validate_rating(rating):
    if rating < 0:
        raise ValidationError(('Рейтинг не может быть ниже 0'),params={'rating': rating},)
    elif rating > 5:
        raise ValidationError(('Рейтинг не может быть выше 5'),params={'rating': rating},)
    else:
        return rating



class Film(models.Model):
    GENRE = (
        ('Horror', 'Ужастик',),
        ('Action', 'Боевик'),
        ('Comedy', 'Комедия'),
        ('Drama', 'Драма'),
        ('Westerns', 'Вестерн'),
        ('Documentary', 'Документалка'),
    )
    title = models.CharField(max_length=60)
    description = models.TextField()
    image = models.ImageField(upload_to='image')
    author = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=40, choices=GENRE)
    sam_film = models.FileField(upload_to='sam_film')
    created_at = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
    film = models.ForeignKey(Film,
                                on_delete=models.CASCADE,
                                related_name='comment')
    user = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Favorite(models.Model):
    user = models.CharField(max_length=50)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)


class Rating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='rating_manga')
    user = models.CharField(max_length=50)
    rating = models.SmallIntegerField(default=0, validators=[validate_rating])


class Like(models.Model):
    user = models.CharField(max_length=50)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)