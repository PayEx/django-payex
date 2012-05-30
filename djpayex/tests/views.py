import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from djpayex.models import TransactionStatus


class CallbackTests(TestCase):
    
    def testCallbackView(self):
        """
        Test manager method for an initiated payment.
        """
        
        # GET is not allowed
        response = self.client.get(reverse('payex-callback'))
        self.assertTrue(response.status_code, 405)
        
        # POST a callback with missing argument
        response = self.client.post(reverse('payex-callback'), {})
        self.assertTrue(response.status_code, 200)
        self.assertEquals(response.content, 'FAILURE')
        
        # Only test against PayEx test server
        if not getattr(settings, 'PAYEX_IN_PRODUCTION', True):
            
            # POST a valid callback 
            response = self.client.post(reverse('payex-callback'), {
                'transactionRef': '123',
                'transactionNumber': '456',
                'orderRef': 'abc123',
            })
            self.assertTrue(response.status_code, 200)
            self.assertEquals(response.content, 'OK')
            
            # Check object
            self.assertEquals(TransactionStatus.objects.count(), 1)
            
            status = TransactionStatus.objects.get()
