"""
Various utilities.
"""


def generate_client_identifier(request):
    """
    Returns a client identifier based on a request, used for help with fraud detection.
    """
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    return 'useragent=%(user_agent)s' % {'user_agent': user_agent}
