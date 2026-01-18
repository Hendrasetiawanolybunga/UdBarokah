from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Transaksi
from .tasks import send_notification_task

# Dictionary to temporarily store previous status values
# Using a simple approach with a cache-like mechanism
previous_status_cache = {}

@receiver(post_save, sender=Transaksi)
def transaksi_status_change_handler(sender, instance, created, **kwargs):
    """
    Signal handler untuk mengirim notifikasi ketika status transaksi berubah.
    """
    # Debug logging untuk verifikasi signal tereksekusi
    print(f"--- [DEBUG Sinyal] Post_Save Transaksi #{instance.id} dipicu. Created: {created}. Status: {instance.status_transaksi} ---")
    
    # Jika ini adalah transaksi baru, tidak perlu mengirim notifikasi perubahan status
    if created:
        return
    
    # Ambil status lama dari cache atau database
    old_status = None
    
    # Coba ambil dari cache dulu
    if instance.id in previous_status_cache:
        old_status = previous_status_cache[instance.id]
    else:
        # Jika tidak ada di cache, ambil dari database
        try:
            old_instance = Transaksi.objects.get(pk=instance.pk)
            old_status = old_instance.status_transaksi
        except Transaksi.DoesNotExist:
            print(f"DEBUG: Tidak dapat menemukan instance lama untuk transaksi {instance.id}")
            return
    
    # Update cache dengan status baru
    previous_status_cache[instance.id] = instance.status_transaksi
    
    # Periksa apakah status berubah
    if old_status != instance.status_transaksi:
        print(f"DEBUG: Status berubah dari {old_status} ke {instance.status_transaksi} untuk transaksi {instance.id}")
        
        # Siapkan pesan berdasarkan status baru
        try:
            status_messages = {
                'DIBAYAR': 'Pembayaran pesanan Anda telah dikonfirmasi.',
                'DIKIRIM': 'Pesanan Anda sedang dalam pengiriman.',
                'SELESAI': 'Pesanan Anda telah selesai. Terima kasih telah berbelanja!',
            }
            
            # Khusus untuk status DIBATALKAN, buat pesan yang lebih informatif
            if instance.status_transaksi == 'DIBATALKAN':
                print(f"DEBUG: Menyiapkan pesan khusus untuk pembatalan transaksi {instance.id}")
                nama_bank = getattr(instance.idPelanggan, 'nama_bank', 'N/A')
                nomor_rekening = getattr(instance.idPelanggan, 'nomor_rekening', 'N/A')
                print(f"DEBUG: Data bank diambil - Nama Bank: {nama_bank}, Nomor Rekening: {nomor_rekening}")
                message = (
                    f"Pesanan #{instance.id} telah DIBATALKAN oleh Admin. "
                    f"Dana Anda telah kami kembalikan ke rekening {nama_bank} ({nomor_rekening}). "
                    f"Silakan cek detail riwayat pemesanan untuk melihat Bukti Transfer Refund dan alasan pembatalan."
                )
                # Update URL target untuk notifikasi pembatalan
                url_target = f"/pesanan/{instance.id}/"
            else:
                # Dapatkan pesan untuk status baru
                message = status_messages.get(instance.status_transaksi, 
                                    f'Status pesanan Anda berubah menjadi: {instance.status_transaksi}')
                url_target = None
        except Exception as e:
            print(f"ERROR dalam menyusun pesan refund: {str(e)}")
            status_messages = {
                'DIBAYAR': 'Pembayaran pesanan Anda telah dikonfirmasi.',
                'DIKIRIM': 'Pesanan Anda sedang dalam pengiriman.',
                'SELESAI': 'Pesanan Anda telah selesai. Terima kasih telah berbelanja!',
            }
            
            # Khusus untuk status DIBATALKAN dalam error case, buat pesan yang lebih informatif
            if instance.status_transaksi == 'DIBATALKAN':
                nama_bank = getattr(instance.idPelanggan, 'nama_bank', 'N/A')
                nomor_rekening = getattr(instance.idPelanggan, 'nomor_rekening', 'N/A')
                message = (
                    f"Pesanan #{instance.id} telah DIBATALKAN oleh Admin. "
                    f"Dana Anda telah kami kembalikan ke rekening {nama_bank} ({nomor_rekening}). "
                    f"Silakan cek detail riwayat pemesanan untuk melihat Bukti Transfer Refund dan alasan pembatalan."
                )
                # Update URL target untuk notifikasi pembatalan
                url_target = f"/pesanan/{instance.id}/"
            else:
                message = f'Status pesanan Anda berubah menjadi: {instance.status_transaksi}'
                url_target = None
        
        # Untuk status SELESAI, tambahkan link untuk memberikan feedback
        if instance.status_transaksi == 'SELESAI':
            detail_url = reverse('detail_pesanan', args=[instance.pk])
            message += f" <a href='{detail_url}' class='alert-link'>Beri Feedback</a>"
        
        # Debug information
        print(f"--- DEBUG SIGNALS ---")
        print(f"Mengirim notifikasi ke User: {instance.idPelanggan.id}")
        print(f"Isi Pesan: {message}")
        
        # Import transaction
        from django.db import transaction
        
        # Kirim notifikasi melalui Celery task setelah transaksi commit
        def send_notification_after_commit():
            # Ubah tipe_pesan untuk pembatalan menjadi 'PENGEMBALIAN DANA (REFUND)'
            tipe_pesan_final = 'PENGEMBALIAN DANA (REFUND)' if instance.status_transaksi == 'DIBATALKAN' else 'Status Transaksi'
            
            # Debug Penting
            print(f"DEBUG SIGNALS: Mencoba mengirim pesan refund untuk transaksi {instance.id}")
            
            # Gunakan url_target yang telah ditentukan sebelumnya
            send_notification_task.delay(
                pelanggan_id=instance.idPelanggan.id,
                tipe_pesan=tipe_pesan_final,
                isi_pesan=message,
                url_target=url_target
            )
        
        transaction.on_commit(send_notification_after_commit)
    else:
        print(f"DEBUG: Status tidak berubah untuk transaksi {instance.id}, tidak perlu kirim notifikasi")