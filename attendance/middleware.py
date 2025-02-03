# attendance/middleware.py
'''
def get_client_ip(request):
    """
    Extracts the real IP address of the client, considering the use of proxies and Ngrok.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
'''

def get_client_ip(request):
    """
    Extracts the real IP address of the client, considering the use of proxies and Ngrok.
    If an IPv6 address is provided, it will attempt to convert it into IPv4.
    """
    # First check if the client sent the 'X-Forwarded-For' header (common when using proxies like Ngrok)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    # If 'X-Forwarded-For' exists, it contains a list of IPs, with the real client IP being the first one
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # If 'X-Forwarded-For' is not set, fall back to REMOTE_ADDR, which gives the direct connection IP
        ip = request.META.get('REMOTE_ADDR')

    # Now handle if the IP is IPv6 and attempt to get the IPv4 address
    if ip and ip.startswith("::ffff:"):  # This indicates an IPv6-mapped IPv4 address
        ip = ip[7:]  # Strip the "::ffff:" prefix to get the actual IPv4 address

    # If the IP is still an IPv6 address (like `2401:4900:...`), we could try fetching the client from a different source.
    # For example, you could manually handle IPv6 -> IPv4 conversion or try to rely more on Ngrok's forwarded headers.
    if ':' in ip and not ip.startswith("::ffff:"):  # If it's still an IPv6 address
        # You could log this for debugging purposes, but handling IPv6 correctly might depend on your environment.
        print(f"IPv6 address detected: {ip}")  # Debug log for IPv6 addresses
        # Optional: You could set a fallback to your public-facing IPv4 address from headers if you want.
        ip = "Fallback to public IPv4"  # Placeholder for fallback logic or more sophisticated handling

    return ip



class GetClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        request.META['REMOTE_ADDR'] = ip  # Override REMOTE_ADDR with the real client IP
        return self.get_response(request)

    def get_client_ip(self, request):
        """
        This function will get the client's real IP address, considering proxies like Ngrok.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # The first IP in the list is the real client IP
        else:
            ip = request.META.get('REMOTE_ADDR')  # Fallback to REMOTE_ADDR if no X-Forwarded-For
        return ip
