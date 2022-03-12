from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, F, UniqueConstraint, Q
from django.db.models.deletion import CASCADE, SET_NULL

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Тема группы', unique=True)
    description = models.TextField('Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста', help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=CASCADE, related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка поста', upload_to='posts/',
        null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=SET_NULL, blank=True,
        null=True, related_name='posts',
        help_text='Выберите группу'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=CASCADE, related_name='comments'
    )
    text = models.TextField(
        'Текст комментария к посту',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=CASCADE, related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'], name='unique_follower'
            ),
            CheckConstraint(check=~Q(user=F('following')),
                            name='user_cant_follow_himself'),
        ]

    def __str__(self):
        return f'{self.user.username} подписался на {self.following.username}'
