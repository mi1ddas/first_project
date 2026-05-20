# dictionary/models.py

from django.db import models
class Term(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name="Термин")
    definition = models.TextField(verbose_name="Определение")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.word
class Message(models.Model):
    user_text = models.TextField(verbose_name="Сообщение пользователя")
    bot_response = models.TextField(verbose_name="Ответ бота")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user_text[:40]}..."
    class Meta:
        ordering = ['created_at']
        verbose_name = "Сообщение"
        verbose_name_plural = "История сообщений"