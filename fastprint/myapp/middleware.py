from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = JWTAuthentication()

        # Ambil token dari header Authorization
        raw_token = request.headers.get('Authorization')
        print(f"Authorization Header: {raw_token}")  # Debug token

        
        if request.method == "POST" and request.path.startswith('/api/produks/'):
            if raw_token:  
                try:
                    # Validasi token
                    validated_token = auth.get_validated_token(raw_token.split(' ')[1])  
                    request.user = auth.get_user(validated_token)
                    print(f"Authenticated User: {request.user.username}")  # Debug user
                except AuthenticationFailed as e:
                    print(f"Token Validation Error: {str(e)}")  # Debug error
                    return JsonResponse({"error": f"Invalid or expired token: {str(e)}"}, status=401)
            else:
                return JsonResponse({"error": "Authentication required"}, status=401)

        # Jika bukan operasi tambah produk, lewati middleware
        return self.get_response(request)
