from flask import Flask, request
from werkzeug.exceptions import TooManyRequests

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Dictionary untuk melacak jumlah request per IP = Membuat dictionary untuk menyimpan jumlah request yang diterima dari setiap alamat IP.
ip_request_count = {}

# Fungsi sebelum request diterima
# Middleware before_request
@app.before_request # Fungsi ini dijalankan sebelum setiap request. Di sini, kita menghitung jumlah request yang diterima dari masing-masing alamat IP.
def enforce_rate_limit():
    # Mendapatkan alamat IP klien yang mengirimkan request
    client_ip = request.remote_addr 

    # Memperbarui jumlah request untuk IP yang sama
    if client_ip in ip_request_count: # digunakan untuk memeriksa apakah alamat IP yang mengirimkan request (client_ip) sudah tercatat dalam dictionary ip_request_count.
        ip_request_count[client_ip] += 1  # Menambah jumlah request
    else:
        ip_request_count[client_ip] = 1  # Inisialisasi jumlah request untuk IP yang baru

    # Memeriksa apakah jumlah request melebihi batas yang ditentukan (100 request per menit)
    if ip_request_count[client_ip] > 100:
        # Jika lebih dari 100 request, kirimkan error TooManyRequests
        raise TooManyRequests("Request limit exceeded. Try again later.")

    # Jika ini adalah request pertama untuk IP tersebut, reset jumlah request setelah 60 detik
    if ip_request_count[client_ip] == 1:
        from threading import Timer
        # Timer untuk menghapus IP dari dictionary setelah 60 detik
        Timer(60, lambda: ip_request_count.pop(client_ip, None)).start()

# Mendefinisikan route untuk halaman utama ('/')
@app.route('/')
def home():
    # Menampilkan pesan selamat datang ketika halaman utama diakses
    return "Welcome to your web app!"

# Menjalankan aplikasi Flask dengan mode debug
if __name__ == "__main__":
    app.run(debug=True)
