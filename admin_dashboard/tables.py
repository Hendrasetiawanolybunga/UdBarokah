import django_tables2 as tables
from .models import Transaksi, Produk, Pelanggan, DiskonPelanggan

class TransaksiTable(tables.Table):
    id = tables.Column(verbose_name="ID")
    idPelanggan = tables.Column(verbose_name="Pelanggan")
    tanggal = tables.Column(verbose_name="Tanggal Transaksi")
    status_transaksi = tables.Column(verbose_name="Status")
    total = tables.Column(verbose_name="Total Harga")
    
    class Meta:
        model = Transaksi
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "idPelanggan", "tanggal", "status_transaksi", "total")
        attrs = {"class": "table table-striped table-bordered"}

class ProdukTerlarisTable(tables.Table):
    nama_produk = tables.Column(verbose_name="Nama Produk", accessor='nama_produk')
    total_kuantitas_terjual = tables.Column(verbose_name="Total Kuantitas Terjual")
    # total_pendapatan = tables.Column(verbose_name="Total Pendapatan")  # Removed for quantity focus
    
    class Meta:
        model = Produk
        template_name = "django_tables2/bootstrap.html"
        fields = ("nama_produk", "total_kuantitas_terjual")
        attrs = {"class": "table table-striped table-bordered"}


class PelangganTransaksiTable(tables.Table):
    id = tables.Column(verbose_name="No", accessor='id')
    nama_pelanggan = tables.Column(verbose_name="Nama Pelanggan", accessor='nama_pelanggan')
    total_transaksi = tables.Column(verbose_name="Banyaknya Transaksi")
    
    class Meta:
        model = Pelanggan
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "nama_pelanggan", "total_transaksi")
        attrs = {"class": "table table-striped table-bordered"}


class PelangganUltahTable(tables.Table):
    id = tables.Column(verbose_name="No", accessor='id')
    nama_pelanggan = tables.Column(verbose_name="Nama Pelanggan", accessor='nama_pelanggan')
    tanggal_lahir = tables.Column(verbose_name="Tanggal Lahir")
    no_hp = tables.Column(verbose_name="No HP")
    
    class Meta:
        model = Pelanggan
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "nama_pelanggan", "tanggal_lahir", "no_hp")
        attrs = {"class": "table table-striped table-bordered"}


class PelangganDiskonTable(tables.Table):
    id = tables.Column(verbose_name="No", accessor='id')
    nama_pelanggan = tables.Column(verbose_name="Nama Pelanggan", accessor='idPelanggan.nama_pelanggan')
    persen_diskon = tables.Column(verbose_name="Persen Diskon")
    status = tables.Column(verbose_name="Status Diskon")
    
    class Meta:
        model = DiskonPelanggan
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "nama_pelanggan", "persen_diskon", "status")
        attrs = {"class": "table table-striped table-bordered"}