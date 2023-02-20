import django
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CASCADE

NULLABLE = {'blank': True, 'null': True}

class CustomUserManager(UserManager):

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    # use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class Client(AbstractUser):
    objects = CustomUserManager()


    username = None
    email = models.EmailField(
        verbose_name="Почта",
        max_length=54,
        unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    name = models.CharField(max_length=200, verbose_name='Фамилия Имя Отчество')
    comment = models.TextField(max_length=300, **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} {self.email}'


class Mssg(models.Model):
    STATUS_DONE = 'done'
    # STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'

    STATUSES = (
        (STATUS_DONE, False),
        # (STATUS_CREATED, 'создано'),
        (STATUS_STARTED, True),
    )
    PERIOD_DAY = 86400
    PERIOD_WEEK = 604800
    PERIOD_MONTH = 2419200
    PERIODS = (
        (PERIOD_DAY, 'день=86400'),
        (PERIOD_WEEK, 'неделя=604800'),
        (PERIOD_MONTH, 'месяц=2419200'),
    )

    link = models.ForeignKey('mailing.Client', max_length=100, verbose_name='Какому клиенту относится',
                             on_delete=models.CASCADE, **NULLABLE, default=1)
    text = models.CharField(max_length=100, verbose_name='Тема сообщения')
    ###auto_now  - update from save()##########ForeignKey Mssg
    status = models.BooleanField(default=False)
    period = models.TimeField(auto_now=True, max_length=10, choices=PERIODS, **NULLABLE)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.text} {self.link} {self.status}{self.period}'


# class MssgManager(models.Manager):

class Mailinglog(models.Model):
    mailing = models.CharField(max_length=100, verbose_name='Email')
    result = models.CharField(max_length=100, verbose_name='Result')
    last_attempt = models.DateTimeField(auto_now=True)


# class Emails(models.Model):#################ForeignKey  Client###########Hochu ostavit EmailField i FK
#     email = models.EmailField(max_length=50, verbose_name='Email')######

# Class StatusMssg(models.Model):
#     is_active = models.BooleanField(default=True)################ForeignKey  Mssg##############

# class Settings(models.Model):


# status = models.CharField(max_length=10, choices=STATUSES, default=STATUS_CREATED)
# time = models.TimeField()###Ne ponimau zachem time
class Emails(models.Model):
    comment = models.ForeignKey('mailing.Client', max_length=100, verbose_name='Какому клиенту относится',
                                on_delete=models.CASCADE, **NULLABLE, default=1)
    email = models.EmailField(max_length=50, verbose_name='Емэйл', unique=True)
    status_complete = models.BooleanField(default=False)  ##Client zapolniaet emails poka ne postavit staetus_complete

    class Meta:
        verbose_name = "Емэйл"
        verbose_name_plural = 'Емэйлы'

    def __str__(self):
        return f'{self.email} '

class Subject(models.Model):
    name = models.ForeignKey(Client, on_delete=CASCADE)  # , related_name="product_name"
    # product_name_again = models.CharField(max_length=50, verbose_name='prod name')
    email_subj = models.ForeignKey(Emails, on_delete=CASCADE, default=1)
    mssg_subj = models.ForeignKey(Mssg, on_delete=CASCADE, default=1)
    email = models.EmailField(max_length=50, verbose_name='Емэйл в форме сабджекта', default='andreymazo@mail.ru')
    topic = models.CharField(max_length=100, verbose_name='Тема сообщения в форме сабджекта', default='and here')
    text = models.CharField(max_length=100, verbose_name='Текст сообщения в форме сабджекта', default='and here')


    def __str__(self):
        return f"{self.name} {self.email} {self.topic} {self.text} "
