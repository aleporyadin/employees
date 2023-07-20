from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255, db_index=True)
    position = models.CharField(max_length=100, db_index=True)
    hire_date = models.DateField(db_index=True)
    email = models.EmailField(db_index=True)
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def get_children(self):
        return Employee.objects.filter(manager=self)

    def has_children(self):
        return Employee.objects.filter(manager=self).exists()

    def __str__(self):
        return self.full_name

    def get_sub_employees(self):
        return Employee.objects.filter(manager=self)
