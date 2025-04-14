from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class TelegramUserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError('The Telegram ID must be set')
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(telegram_id, password, **extra_fields)


class TelegramUser(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Фамилия"
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Баланс"


    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создание"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновление"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Персонал"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Суперпользователь"
    )

    objects = TelegramUserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"
        ordering = ['-created_at']

    def __str__(self):
        return self.last_name or str(self.telegram_id)
