from django.db import models

class Expenditure(models.Model):
    ename = models.CharField(max_length=20)
    eamount = models.DecimalField(max_digits=10, decimal_places=2)
    edate = models.DateField()
    issued_to= models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.issued_to}) - {self.date}"

    class Meta:
       db_table = 'expenditure'

# Create your models here.
