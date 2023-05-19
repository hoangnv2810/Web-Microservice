from django.contrib import admin
from .models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'pay_tran_no', 'order_id', 'pay_date', 'ip', 'pay_tran_status')


admin.site.register(Payment, PaymentAdmin)
