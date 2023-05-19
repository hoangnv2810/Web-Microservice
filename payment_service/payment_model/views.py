import hashlib
import hmac
from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment_model.models import Payment
from payment_model.vnpay import vnpay
from payment_service import settings


# Create your views here.
@api_view(['POST'])
def payment(request):
    order_id = request.data['order_id']
    amount = request.data['amount']
    order_desc = request.data['order_desc']
    bank_code = request.data['bank_code']
    language = request.data['language']
    ipaddr = get_client_ip(request)
    # Build URL Payment
    vnp = vnpay()
    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = amount * 100
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = order_id
    vnp.requestData['vnp_OrderInfo'] = order_desc
    # Check language, default: vn
    if language and language != '':
        vnp.requestData['vnp_Locale'] = language
    else:
        vnp.requestData['vnp_Locale'] = 'vn'
    if bank_code and bank_code != "":
        vnp.requestData['vnp_BankCode'] = bank_code

    vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.requestData['vnp_IpAddr'] = ipaddr
    vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
    print(vnpay_payment_url)
    return Response(vnpay_payment_url)


@api_view(['GET'])
def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_BankTranNo = inputData['vnp_BankTranNo']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                payment = Payment.objects.create()
                payment.bank_code = vnp_BankCode
                payment.bank_tran_no = vnp_BankTranNo
                payment.ip = get_client_ip(request)
                payment.order_info = order_desc
                payment.pay_date = vnp_PayDate
                payment.pay_tran_no = vnp_TransactionNo
                payment.pay_tran_status = vnp_TmnCode
                payment.order_id = order_id
                payment.card_type = vnp_CardType
                payment.save()
                return Response({"title": "Kết quả thanh toán",
                                 "result": "Thành công", "order_id": order_id,
                                 "amount": amount,
                                 "order_desc": order_desc,
                                 "vnp_TransactionNo": vnp_TransactionNo,
                                 "vnp_ResponseCode": vnp_ResponseCode}, status=200)
            else:
                return Response({"title": "Kết quả thanh toán",
                                 "result": "Lỗi", "order_id": order_id,
                                 "amount": amount,
                                 "order_desc": order_desc,
                                 "vnp_TransactionNo": vnp_TransactionNo,
                                 "vnp_ResponseCode": vnp_ResponseCode}, status=400)
        else:
            return Response({"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                             "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                             "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"}, status=400)
    else:
        return Response({"title": "Kết quả thanh toán", "result": "Lỗi"}, status=400)


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
