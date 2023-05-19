from django.db import models


# Create your models here.
class Payment(models.Model):
    bank_code = models.CharField(max_length=3, null=False)
    bank_tran_no = models.CharField(max_length=20, null=False)
    ip = models.CharField(null=False, max_length=20)
    order_info = models.CharField(max_length=255)
    pay_date = models.CharField(max_length=100, null=False)
    pay_tran_no = models.CharField(null=False, max_length=20)
    pay_tran_status = models.CharField(max_length=2, null=False)
    order_id = models.CharField(null=False, max_length=20)
    card_type = models.CharField(null=False, max_length=20)

    def __str__(self):
        return self.id
