from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djpayex.models import InitializedPayment, TransactionStatus, Agreement, AutoPayStatus


class InitializedPaymentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Response status'), {
            'fields': ('errorcode', 'description', 'paramname', 'thirdpartyerror', )
        }),
        (_('Initialization'), {
            'fields': ('orderref', 'redirecturl', )
        }),
        (_('Timestamps'), {
            'fields': () # 'created', 'updated', 
        }),
        (_('Raw response'), {
            'classes': ('collapse',),
            'fields': ('raw_response', )
        }),
    )
    list_display = ('__unicode__', 'errorcode', 'orderref', 'created', )
    list_filter = ('created', )
    search_fields = ('id', 'orderref', )
    #readonly_fields = InitializedPayment._meta.get_all_field_names()

admin.site.register(InitializedPayment, InitializedPaymentAdmin)


class TransactionStatusAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Response status'), {
            'fields': ('errorcode', 'description', 'paramname', 'thirdpartyerror', )
        }),
        (_('Transaction'), {
            'fields': ('transactionstatus', 'transactionnumber', )
        }),
        (_('Order information'), {
            'fields': ('orderid', 'productid', 'paymentmethod', 'amount', 'alreadycompleted', 'stopdate', 'productnumber', 'clientgsmnumber', 'orderstatus', 'agreementref', 'paymentmethodexpiredate', )
        }),
        (_('Payment information'), {
            'fields': ('bankhash', 'maskednumber', 'authenticatedstatus', 'authenticatedwith', 'frauddata', 'pending', )
        }),
        (_('Error information'), {
            'fields': ('transactionerrorcode', 'transactionerrordescription', 'transactionthirdpartyerror', )
        }),
        (_('Timestamps'), {
            'fields': () # 'created', 'updated', 
        }),
        (_('Raw response'), {
            'classes': ('collapse',),
            'fields': ('raw_response', )
        }),
    )
    list_display = ('__unicode__', 'transactionnumber', 'transactionstatus', 'errorcode', 'alreadycompleted', 'created', )
    list_filter = ('created', )
    search_fields = ('id', 'transactionnumber', )
    #readonly_fields = TransactionStatus._meta.get_all_field_names()

admin.site.register(TransactionStatus, TransactionStatusAdmin)

class AgreementAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Response status'), {
            'fields': ('errorcode', 'description', 'paramname', 'thirdpartyerror', )
        }),
        (_('Agreement'), {
            'fields': ('agreementref', 'maxamount', )
        }),
        (_('Timestamps'), {
            'fields': () # 'created', 'updated', 
        }),
        (_('Raw response'), {
            'classes': ('collapse',),
            'fields': ('raw_response', )
        }),
    )
    list_display = ('__unicode__', 'errorcode', 'agreementref', 'created', )
    list_filter = ('created', )
    search_fields = ('id', 'agreementref', )
    #readonly_fields = Agreement._meta.get_all_field_names()

admin.site.register(Agreement, AgreementAdmin)

class AutoPayStatusAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Response status'), {
            'fields': ('errorcode', 'description', 'paramname', 'thirdpartyerror', )
        }),
        (_('Transaction'), {
            'fields': ('transactionstatus', 'transactionnumber', 'transactionref', )
        }),
        (_('Payment information'), {
            'fields': ('paymentmethod', )
        }),
        (_('Timestamps'), {
            'fields': () # 'created', 'updated', 
        }),
        (_('Raw response'), {
            'classes': ('collapse',),
            'fields': ('raw_response', )
        }),
    )
    list_display = ('__unicode__', 'errorcode', 'transactionnumber', 'created', )
    list_filter = ('created', )
    search_fields = ('id', 'transactionnumber', )
    #readonly_fields = AutoPayStatus._meta.get_all_field_names()

admin.site.register(AutoPayStatus, AutoPayStatusAdmin)
