from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ProdukForm
from .models import Produk

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProdukSerializer, ProdukResponseSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


# View untuk halaman login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login_page(request):
    if request.method == "GET":
        # Tampilkan halaman login untuk browser
        return render(request, 'myapp/login.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Buat token JWT baru
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Cek apakah permintaan berasal dari browser atau API
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

            if "postman" in user_agent or "insomnia" in user_agent:
                # Respons JSON untuk API
                return JsonResponse({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=200)
            else:
                # Redirect ke halaman home untuk browser
                response = redirect('home')
                response.set_cookie('access_token', access_token, httponly=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True)
                return response

        else:
            # Jika login gagal
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    # Jika metode tidak valid
    return JsonResponse({"error": "Invalid request method"}, status=400)




# View untuk logout
def logout_view(request):
    response = JsonResponse({"message": "Logout successful"})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


# CRUD = Create, Read, Update, Delete

#Home View
def home_view(request):
    return render(request, 'myapp/home.html')

#Create View
def produk_create_view(request):
    form = ProdukForm()
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produk_list')
    return render(request, 'myapp/produk_form.html', {'form': form})

#Read View
def produk_list_view(request):
    produks = Produk.objects.all()
    return render(request, 'myapp/produk_list.html', {'produks': produks})

#Update View
def produk_update_view(request, id_produk):
    produk = Produk.objects.get(id_produk=id_produk)
    form = ProdukForm(instance=produk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('produk_list')
    return render(request, 'myapp/produk_form.html', {'form': form})

#Delete View
# def produk_delete_view(request, id_produk):
#     produk = Produk.objects.get(id_produk=id_produk)
#     if request.method == 'POST':
#         produk.delete()
#         return redirect('produk_list')
#     return render(request, 'myapp/produk_delete.html', {'produk': produk})
def produk_delete_view(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    if request.method == 'POST':
        produk.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# API Views
class ProdukListAPIView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        print(f"Authorization Header: {auth_header}")  # Debug header

        if not auth_header:
            return Response({"error": "Authentication required"}, status=401)

        # Validasi token
        raw_token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else auth_header
        print(f"Raw Token: {raw_token}")  # Debug token

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(raw_token)
            user = auth.get_user(validated_token)
            print(f"Authenticated User: {user.username}")  # Debug user
        except AuthenticationFailed as e:
            print(f"Token Validation Error: {str(e)}")  # Debug error
            return Response({"error": f"Invalid or expired token: {str(e)}"}, status=401)

        # Jika token valid, proses data
        serializer = ProdukSerializer(data=request.data)
        if serializer.is_valid():
            produk = serializer.save()
            return Response(ProdukResponseSerializer(produk).data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        # Ambil token dari header Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"error": "Authentication required"}, status=401)

        
        raw_token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else auth_header

        # Validasi token
        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(raw_token)
            user = auth.get_user(validated_token)
        except AuthenticationFailed as e:
            return Response({"error": f"Invalid or expired token: {str(e)}"}, status=401)

        # Jika token valid, kembalikan daftar produk
        produks = Produk.objects.all()
        serializer = ProdukResponseSerializer(produks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProdukDetailAPIView(APIView):
    def get(self, request, id_produk):
        try:
            produk = Produk.objects.get(id_produk=id_produk)
            # serializer = ProdukSerializer(produk)
            serializer = ProdukResponseSerializer(produk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Produk.DoesNotExist:
            return Response({"error": "Produk not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id_produk):
        try:
            # Ambil produk berdasarkan ID
            produk = Produk.objects.get(id_produk=id_produk)

            # Serialize data yang diterima dari request
            serializer = ProdukSerializer(produk, data=request.data)
            if serializer.is_valid():
                # Simpan data yang valid
                produk = serializer.save()


                response_serializer = ProdukResponseSerializer(produk)
                return Response(
                    {
                        "message": "Product updated successfully",
                        "data": response_serializer.data  
                    },
                    status=status.HTTP_200_OK
                )

            # Jika data tidak valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Produk.DoesNotExist:
            # Jika produk tidak ditemukan
            return Response({"error": "Produk not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id_produk):
        try:
            produk = Produk.objects.get(id_produk=id_produk)
            nama_produk = produk.nama_produk
            produk.delete()
            return Response({"message": f"Product '{nama_produk}' deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Produk.DoesNotExist:
            return Response({"error": "Produk not found"}, status=status.HTTP_404_NOT_FOUND)

class ProdukFilterByStatusAPIView(APIView):
    def get(self, request):
        # Ambil query parameter dari URL
        nama_status = request.query_params.get('status', None)
        
        if nama_status:
            # Filter produk berdasarkan nama status
            produks = Produk.objects.filter(status__nama_status__icontains=nama_status)
            if not produks.exists():
                return Response(
                    {"error": f"Tidak ada produk dengan status '{nama_status}'"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Default: Tampilkan hanya produk dengan status "Bisa Dijual"
            produks = Produk.objects.filter(status__nama_status="Bisa Dijual")
            if not produks.exists():
                return Response(
                    {"error": "Tidak ada produk dengan status 'Bisa Dijual'"},
                    status=status.HTTP_404_NOT_FOUND
                )
        

        serializer = ProdukResponseSerializer(produks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)