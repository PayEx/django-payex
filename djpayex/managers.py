from django.db import models


class PayexResponseManager(models.Manager):
    """
    Manager with convenience methods for classes subclassing PayexResponse.
    """
    
    def create_from_response(self, response, obj=None, commit=True):
        """
        Sets variables on an object based on a response dictionary from `pypayex`.
        """
        
        available_fields = self.model._meta.get_all_field_names()
        
        # Instantiate a new object if not provided
        if obj is None:
            obj = self.model()
        
        obj.raw_response = response
        
        # Explicitly set response status
        if 'status' in response:
            obj.errorcode = response['status']['errorCode']
            obj.description = response['status']['description']
            obj.paramname = response['status']['paramName'] or u''
            obj.thirdpartyerror = response['status']['thirdPartyError'] or u''
        
        # Explicitly set eventual error codes
        if 'errorDetails' in response:
            obj.transactionerrorcode = response['errorDetails']['transactionErrorCode'] or u''
            obj.transactionerrordescription = response['errorDetails']['transactionErrorDescription'] or u''
            obj.transactionthirdpartyerror = response['errorDetails']['transactionThirdPartyError'] or u''
        
        # Set response on available fields
        for key, val in response.iteritems():
            
            # Normalize key case
            key = key.lower()
            
            # Convert None values to empty strings
            if val is None:
                val = u''
            
            if key in available_fields:
                setattr(obj, key, val)
        
        if commit:
            obj.save()
        
        return obj

class InitializedPaymentManager(PayexResponseManager):
    """
    Manager for InitializedPayment model.
    """
    
    pass

class TransactionStatusManager(PayexResponseManager):
    """
    Manager for TransactionStatus model.
    """
    
    pass

class AgreementManager(PayexResponseManager):
    """
    Manager for Agreement model.
    """
    
    pass

class AutoPayStatusManager(PayexResponseManager):
    """
    Manager for AutoPayStatus model.
    """
    
    pass
