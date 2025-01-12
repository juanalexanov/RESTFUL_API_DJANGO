from rest_framework import serializers
from .models import Kategori, Status, Produk

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ProdukSerializer(serializers.ModelSerializer):
    kategori_id = serializers.IntegerField(write_only=True)
    status_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori_id', 'status_id']

    def create(self, validated_data):
        kategori = Kategori.objects.get(id_kategori=validated_data.pop('kategori_id'))
        status = Status.objects.get(id_status=validated_data.pop('status_id'))
        produk = Produk.objects.create(kategori=kategori, status=status, **validated_data)
        return produk

class ProdukResponseSerializer(serializers.ModelSerializer):
    kategori = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']

    def get_kategori(self, obj):
        return obj.kategori.nama_kategori

    def get_status(self, obj):
        return obj.status.nama_status