import django_filters
from django import forms
from .models import Transaksi, Produk

class TransaksiFilter(django_filters.FilterSet):
    TIPE_CHOICES = [
        ('ringkasan_pelanggan', 'Ringkasan Transaksi Pelanggan'),
        ('ultah_pelanggan', 'Pelanggan Ulang Tahun'),
        ('diskon_pelanggan', 'Pelanggan Penerima Diskon'),
    ]
    
    tipe_laporan = django_filters.ChoiceFilter(
        choices=TIPE_CHOICES,
        label='Tipe Laporan',
        empty_label='Pilih Tipe Laporan',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tanggal_transaksi__gte = django_filters.DateFilter(
        field_name='tanggal', 
        lookup_expr='gte', 
        label='Tanggal Mulai',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    tanggal_transaksi__lte = django_filters.DateFilter(
        field_name='tanggal', 
        lookup_expr='lte', 
        label='Tanggal Akhir',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = Transaksi
        fields = {
            'status_transaksi': ['exact'],
        }
        widgets = {
            'status_transaksi': forms.Select(attrs={'class': 'form-control'})
        }

class ProdukTerlarisFilter(django_filters.FilterSet):
    nama_produk = django_filters.CharFilter(
        field_name='nama_produk',
        lookup_expr='icontains',
        label='Nama Produk',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tanggal_transaksi__gte = django_filters.DateFilter(
        field_name='detailtransaksi__idTransaksi__tanggal',
        lookup_expr='gte',
        label='Tanggal Mulai',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    tanggal_transaksi__lte = django_filters.DateFilter(
        field_name='detailtransaksi__idTransaksi__tanggal',
        lookup_expr='lte',
        label='Tanggal Akhir',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = Produk
        fields = []