from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # add user relation

    def __str__(self):
        return self.title