import datetime

from django.conf import settings
from django.test import TestCase

from djpayex.models import InitializedPayment, TransactionStatus, AutoPayStatus

class InitializedPaymentTests(TestCase):
    
    def testManagerCreateResponse(self):
        """
        Test manager method for an initiated payment.
        """
        
        response = {
            'status': {
                'errorCode': 'OK', 
                'code': 'OK', 
                'description': 'OK', 
                'thirdPartyError': None, 
                'paramName': None
            }, 
            'header': {
                'date': '2011-10-07 12:35:34', 
                'name': 'Payex Header v1.0', 
                'id': 'a3a2da2c9cdd4aebbcaa6b609df6fd52'
            }, 
            'sessionRef': '5996a5a093af4820a8c5755a73e6e76b', 
            'redirectUrl': 'https://test-account.payex.com/MiscUI/PxMenu.aspx?orderRef=c59cc7c7cc0c4194b1e21c27d6ba4074', 
            'orderRef': 'c59cc7c7cc0c4194b1e21c27d6ba4074'
        }
        
        # Don't save
        obj = InitializedPayment.objects.create_from_response(response, commit=False)
        self.assertEquals(InitializedPayment.objects.count(), 0)
        
        # Save as new object
        obj = InitializedPayment.objects.create_from_response(response)
        self.assertEquals(InitializedPayment.objects.count(), 1)
        
        # Check that fields are set
        self.assertEquals(obj.raw_response, response)
        self.assertEquals(obj.errorcode, response['status']['errorCode'])
        self.assertEquals(obj.description, response['status']['description'])
        self.assertEquals(obj.orderref, response['orderRef'])
        self.assertEquals(obj.redirecturl, response['redirectUrl'])
        
        self.assertTrue(isinstance(obj.created, datetime.datetime))
        self.assertTrue(isinstance(obj.updated, datetime.datetime))

class TransactionStatusTests(TestCase):
    
    def testManagerCreateResponseUnfinished(self):
        """
        Test manager create method for an unfinished transaction.
        """
        
        response = {
            'status': {
                'errorCode': 'Order_OrderProcessing', 
                'code': 'Order_OrderProcessing', 
                'description': 'The user has not initialized the purchase yet', 
                'thirdPartyError': None, 
                'paramName': None
            },
            'header': {
                'date': '2011-10-07 12:53:53', 
                'name': 'Payex Header v1.0', 
                'id': 'd9d4c533c8484a7c8141fda341e830e1'
            },
            'orderStatus': '1'
        }
        
        # Don't save
        obj = TransactionStatus.objects.create_from_response(response, commit=False)
        self.assertEquals(TransactionStatus.objects.count(), 0)
        
        # Save as new object
        obj = TransactionStatus.objects.create_from_response(response)
        self.assertEquals(TransactionStatus.objects.count(), 1)
        
        # Check that fields are set
        self.assertTrue(isinstance(obj.created, datetime.datetime))
        self.assertTrue(isinstance(obj.updated, datetime.datetime))
        self.assertEquals(obj.raw_response, response)
        self.assertEquals(obj.errorcode, response['status']['errorCode'])
        self.assertEquals(obj.description, response['status']['description'])
        
        # The customer has not started payment process
        self.assertEquals(obj.orderstatus, '1')
    
    def testManagerCreateResponseCompleted(self):
        """
        Test manager create method for a completed transaction.
        """
        
        response = {
            'status': {
                'errorCode': 'OK', 
                'code': 'OK', 
                'description': 'OK', 
                'thirdPartyError': None, 
                'paramName': None
            }, 
            'orderId': 'test1', 
            'transactionNumber': '40276785', 
            'clientAccount': '0', 
            'pending': False, 
            'alreadyCompleted': False, 
            'clientGsmNumber': None, 
            'productNumber': '123', 
            'AuthenticatedStatus': '3DSecure', 
            'maskedNumber': '41**********1111', 
            'header': {
                'date': '2011-10-07 12:59:30', 
                'name': 'Payex Header v1.0', 
                'id': 'efb64f26a27449b9bd513f949a077080'
            }, 
            'amount': '5000', 
            'fraudData': False, 
            'orderStatus': '0', 
            'AuthenticatedWith': 'Y', 
            'transactionRef': 'e4ee430eba5a4cdb85f7e81a93c2e424', 
            'transactionStatus': '0', 
            'paymentMethod': 'VISA', 
            'BankHash': '12300001-4111-1111-1111-000000000000', 
            'productId': '123'
        }
        
        # Don't save
        obj = TransactionStatus.objects.create_from_response(response, commit=False)
        self.assertEquals(TransactionStatus.objects.count(), 0)
        
        # Save as new object
        obj = TransactionStatus.objects.create_from_response(response)
        self.assertEquals(TransactionStatus.objects.count(), 1)
        
        # Check that fields are set
        self.assertTrue(isinstance(obj.created, datetime.datetime))
        self.assertTrue(isinstance(obj.updated, datetime.datetime))
        self.assertEquals(obj.raw_response, response)
        self.assertEquals(obj.errorcode, response['status']['errorCode'])
        self.assertEquals(obj.description, response['status']['description'])
        
        self.assertEquals(obj.transactionnumber, '40276785')
        
        # The customer has paid
        self.assertEquals(obj.orderstatus, '0')
        
        # Check booleans
        self.assertFalse(obj.pending)
        self.assertFalse(obj.alreadycompleted)
        self.assertFalse(obj.frauddata)
        
        self.assertTrue(obj.is_completed_successfully())

class AutoPayTests(TestCase):
    
    def testAutoPayResponse(self):
        """
        Test manager create method for an autopay transaction.
        """
        
        response = {
            'status': {
                'errorCode': 'OK', 
                'code': 'OK', 
                'description': 'OK', 
                'thirdPartyError': None, 
                'paramName': None
            }, 
            'header': {
                'date': '2012-05-30 14:36:09', 
                'name': 'Payex Header v1.0', 
                'id': 'c7421744c7a24b448fd34caee0563cdb'
            }, 
            'transactionNumber': '041029056', 
            'transactionRef': 'b23a5779df944b0dae745065dd1804f2', 
            'paymentMethod': 'VISA', 
            'transactionStatus': '0'
        }
        
        # Don't save
        obj = AutoPayStatus.objects.create_from_response(response, commit=False)
        self.assertEquals(AutoPayStatus.objects.count(), 0)
        
        # Save as new object
        obj = AutoPayStatus.objects.create_from_response(response)
        self.assertEquals(AutoPayStatus.objects.count(), 1)
        
        # Check that fields are set
        self.assertTrue(isinstance(obj.created, datetime.datetime))
        self.assertTrue(isinstance(obj.updated, datetime.datetime))
        self.assertEquals(obj.raw_response, response)
        self.assertEquals(obj.errorcode, response['status']['errorCode'])
        self.assertEquals(obj.description, response['status']['description'])
        
        self.assertEquals(obj.transactionnumber, '041029056')
        self.assertEquals(obj.transactionstatus, '0')
        
        self.assertTrue(obj.is_completed_successfully())
