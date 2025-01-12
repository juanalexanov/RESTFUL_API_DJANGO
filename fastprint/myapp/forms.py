from django import forms
from .models import Kategori, Status, Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = '__all__'
        labels = {
            'id_produk': 'ID Produk',
            'nama_produk': 'Nama Produk',
            'harga': 'Harga',
            'kategori': 'Kategori',
            'status': 'Status',
        }
        widgets = {
            'id_produk': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                }
            ),
            'nama_produk': forms.TextInput(
                attrs={
                    'placeholder': 'Masukkan Nama Produk',
                    'class': 'form-control',
                }
            ),
            'harga': forms.NumberInput(
                attrs={
                    'placeholder': 'Masukkan Harga Produk',
                    'class': 'form-control',
                }
            ),
            'kategori': forms.Select(
                attrs={
                    'placeholder': 'Pilih Kategori Produk',
                    'class': 'form-control',
                }
            ),
            'status': forms.Select(
                attrs={
                    'placeholder': 'Pilih Status Produk',
                    'class': 'form-control',
                }
            ),
        }

# Validasi untuk nama_produk
    def clean_nama_produk(self):
        nama_produk = self.cleaned_data.get('nama_produk')
        if not nama_produk:
            raise forms.ValidationError("Nama produk harus diisi.")
        return nama_produk

# Validasi untuk harga
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga is None:
            raise forms.ValidationError("Harga harus berupa angka.")
        if harga <= 0:
            raise forms.ValidationError("Harga harus lebih besar dari 0.")
        return harga