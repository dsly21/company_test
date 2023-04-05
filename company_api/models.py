from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200)
    director = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        related_name='departments'
    )

    class Meta:
        unique_together = (
            'name',
            'director'
        )


class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='static/photos/')
    position = models.CharField(max_length=300)
    salary = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
        blank=True,
        null=True,
    )
