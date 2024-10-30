from django.db import models


class CustomModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Pattern(CustomModel):
    name = models.CharField(max_length=100)
    regex = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CaughtMessage(CustomModel):
    content = models.TextField()
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    ts = models.DecimalField(max_digits=20, decimal_places=6)
    channel = models.CharField(max_length=100)

    def __str__(self):
        return self.content
