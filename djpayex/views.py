import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from payex.service import PayEx

from djpayex.models import TransactionStatus

logger = logging.getLogger(__name__)

# Initialize PayEx service
service = PayEx(
    merchant_number=settings.PAYEX_MERCHANT_NUMBER, 
    encryption_key=settings.PAYEX_ENCRYPTION_KEY, 
    production=settings.PAYEX_IN_PRODUCTION
)

def callback(request):
    """
    NOTE Not fully implemented yet.
    
    PayEx will send a transaction callback (as HTTP Post) to the merchant, 
    if any transaction status is updated at the PayEx system.
    
    Request from PayEx:
        HTTP 200 transactionRef =<32 digits>&transactionNumber=<8 digits>(&orderRef=<32 digits> if exists)
    Response from merchant:
        HTTP 200 OK or FAILURE. On "FAILURE" PayEx will retry the HTTP POST-request 5 times, with approximately 15 minutes interval
    
    Documentation:
    http://www.payexpim.com/quick-guide/9-transaction-callback/
    """
    
    logger.info('Got PayEx callback: %(raw_post_data)s\n%(meta)s\n%(post_data)s' % {
        'raw_post_data': request.raw_post_data,
        'meta': request.META,
        'post_data': request.POST,
    })
    
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST',])
    
    orderref = request.POST.get('orderRef', None)
    
    if orderref:
        response = service.complete(orderRef=orderref)
        status = TransactionStatus.objects.create_from_response(response)
        
        return HttpResponse('OK')
    
    return HttpResponse('FAILURE')
