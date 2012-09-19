from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from djpayex.managers import InitializedPaymentManager, TransactionStatusManager, AgreementManager, AutoPayStatusManager


class PayexResponse(models.Model):
    """
    Abstract base class for responses from PayEx API.
    """
    
    # Request status
    errorcode = models.CharField(_('errorCode'), max_length=255, blank=True, help_text=_('OK if request is successful. This does NOT indicate whether the transaction requested was successful.'))
    description = models.CharField(_('description'), max_length=255, blank=True, help_text=_('Literal description explaining the result.'))
    paramname = models.CharField(_('paramName'), max_length=255, blank=True, help_text=_('Name of the parameter that contains invalid data.'))
    thirdpartyerror = models.CharField(_('thirdPartyError'), max_length=255, blank=True, help_text=_('Error code received from third party (if returned).'))
    
    # The raw response received from the client
    raw_response = models.TextField(_('raw response'), blank=True)
    
    # Timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    
    class Meta:
        abstract = True

##################
# Payment models #
##################

class InitializedPayment(PayexResponse):
    """
    Initialization of a Payment.
    """
    
    orderref = models.CharField(_('orderRef'), max_length=255, blank=True, help_text=_('If successful, a 32bit hexadecimal value (Guid) identifying the orderRef.'))
    redirecturl = models.CharField(_('redirectUrl'), max_length=255, blank=True, help_text=_('Dynamic URL to send the end user to, when using redirect model.'))
    
    objects = InitializedPaymentManager()
    
    class Meta:
        verbose_name = _('initialized payment')
        verbose_name_plural = _('initialized payments')
    
    def __unicode__(self):
        return _('Initialized payment %s') % self.id


class TransactionStatus(PayexResponse):
    """
    Status of a performed or cancelled transaction.
    """
    
    # Transaction status
    transactionstatus = models.CharField(_('transactionStatus'), max_length=255, blank=True, help_text=_('0=Sale, 1=Initialize, 2=Credit, 3=Authorize, 4=Cancel,5=Failure,6=Capture'))
    transactionnumber = models.CharField(_('transactionNumber'), max_length=255, blank=True, help_text=_('Transaction number if the transaction is successful.'))
    
    # Info about the order
    orderid = models.CharField(_('orderId'), max_length=255, blank=True, help_text=_('The orderID supplied by the merchant when the order was created.'))
    productid = models.CharField(_('productId'), max_length=255, blank=True)
    paymentmethod = models.CharField(_('paymentMethod'), max_length=255, blank=True)
    amount = models.CharField(_('amount'), max_length=255, blank=True)
    alreadycompleted = models.BooleanField(_('alreadyCompleted'), default=False)
    stopdate = models.CharField(_('stopDate'), max_length=255, blank=True)
    productnumber = models.CharField(_('productNumber'), max_length=255, blank=True)
    clientgsmnumber = models.CharField(_('clientGsmNumber'), max_length=255, blank=True)
    orderstatus = models.CharField(_('orderStatus'), max_length=255, blank=True, help_text=_('0=Order completed (but check transactionStatus for result), 1=Processing, 2=Not found'))
    agreementref = models.CharField(_('agreementRef'), max_length=255, blank=True)
    paymentmethodexpiredate = models.CharField(_('paymentMethodExpireDate'), max_length=255, blank=True)
    
    # Card information
    bankhash = models.CharField(_('BankHash'), max_length=255, blank=True, help_text=_('Hash of the credit card number.'))
    maskednumber = models.CharField(_('maskedNumber'), max_length=255, blank=True)
    authenticatedstatus = models.CharField(_('AuthenticatedStatus'), max_length=255, blank=True)
    authenticatedwith = models.CharField(_('AuthenticatedWith'), max_length=255, blank=True)
    frauddata = models.BooleanField(_('fraudData'), default=False, help_text=_('The transaction has triggered the fraud detection module.'))
    pending = models.BooleanField(_('pending'), default=False, help_text=_('True if we do not know the status of the transaction from third party, transactionStatus will be init.'))
    
    # Error info
    transactionerrorcode = models.TextField(_('transactionErrorCode'), blank=True)
    transactionerrordescription = models.TextField(_('transactionErrorDescription'), blank=True)
    transactionthirdpartyerror = models.TextField(_('transactionThirdPartyError'), blank=True)
    
    objects = TransactionStatusManager()
    
    class Meta:
        verbose_name = _('transaction status')
        verbose_name_plural = _('transaction statuses')
    
    def __unicode__(self):
        return _('Transaction status %s') % self.id
    
    def is_completed_successfully(self):
        """
        Checks if the transaction was completed successfully.
        """
        
        return self.errorcode == 'OK' and self.transactionstatus in ('0', '3')
    
    def get_decimal_amount(self):
        """
        Returns the amount as Decimal.
        """
        
        if self.amount:
            return Decimal(self.amount) / 100
        
        return Decimal('0.00')

####################
# Agreement models #
####################

class Agreement(PayexResponse):
    """
    Agreement between merchant and client.
    """
    
    agreementref = models.CharField(_('agreementRef'), max_length=255, blank=True, help_text=_('Reference to the created agreement.'))
    
    # Information about the agreement given by the merchant upon creation
    maxamount = models.CharField(_('maxAmount'), max_length=255, blank=True, help_text=_('One single transaction can never be greater than this amount.'))
    
    objects = AgreementManager()
    
    class Meta:
        verbose_name = _('agreement')
        verbose_name_plural = _('agreements')
    
    def __unicode__(self):
        return _('Agreement %s') % self.agreementref
    
    def is_verified(self):
        """
        Checks with PayEx if the agreement is verified.
        """
        
        from django.conf import settings
        from payex.service import PayEx
        
        # Initialize service
        service = PayEx(
            merchant_number=settings.PAYEX_MERCHANT_NUMBER, 
            encryption_key=settings.PAYEX_ENCRYPTION_KEY, 
            production=settings.PAYEX_IN_PRODUCTION
        )
        
        response = service.check_agreement(agreementRef=self.agreementref)
        
        if response['status']['description'] == 'OK':
            return response['agreementStatus'] == '1'
        
        return False

class AutoPayStatus(PayexResponse):
    """
    Status of an autopay performed on an agreement.
    """
    
    # Transaction status
    transactionstatus = models.CharField(_('transactionStatus'), max_length=255, blank=True, help_text=_('0=Sale, 1=Initialize, 2=Credit, 3=Authorize, 4=Cancel,5=Failure,6=Capture'))
    transactionref = models.CharField(_('transactionRef'), max_length=255, blank=True, help_text=_('An ID to the transaction completed.'))
    transactionnumber = models.CharField(_('transactionNumber'), max_length=255, blank=True, help_text=_('Transaction number if the transaction is successful.'))
    paymentmethod = models.CharField(_('paymentMethod'), max_length=255, blank=True, help_text=_('Payment method used for this transaction.'))
    
    objects = AutoPayStatusManager()
    
    class Meta:
        verbose_name = _('autopay status')
        verbose_name_plural = _('autopay statuses')
    
    def __unicode__(self):
        return _('Autopay status %s') % self.id
    
    def is_completed_successfully(self):
        """
        Checks if the transaction was completed successfully.
        """
        
        return self.errorcode == 'OK' and self.transactionstatus in ('0', '3')
