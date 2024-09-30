# werkudara
Automatically synchronize author and lecturer data in https://bima.kemdikbud.go.id (Unofficial)

## Documentation (ID)

### A. Pendahuluan dan Latar Belakang

Saat ini, data kepegawaian, penelitian, dan pengabdian masyarakat dosen perguruan tinggi di Indonesia telah terintegrasi ke dalam satu sistem terpadu, yang disebut BIMA. [BIMA](https://bima.kemdikbud.go.id) merupakan akronim dari _Basis Informasi Penelitian dan Pengabdian kepada Masyarakat_, yang dikembangkan dan diluncurkan oleh Kemdikbudristek pada tahun 2022. Adanya sistem informasi terpadu BIMA membuat pengajuan dan pemutakhiran data penelitian serta pengabdian masyarakat menjadi lebih mudah.

Meskipun demikian, BIMA mempunyai suatu fitur yang belum/tidak diimplementasikan di dalam kerangka sistemnya. Di dalam sistem BIMA, operator BIMA dari masing-masing perguruan tinggi harus menyinkronisasi data kepegawaian dosen yang ada di BIMA dengan data yang terdaftar di Pangkalan Data Pendidikan Tinggi (PD-DIKTI). Tidak ada opsi dalam BIMA untuk melakukan proses sinkronisasi semua data dosen secara jamak. Selama ini, operator BIMA harus membuka halaman profil masing-masing dosen dan mengklik tombol _sinkronisasi_ secara manual, satu per satu. Hal ini tentu memakan proses yang lama, terutama pada universitas-universitas di Indonesia yang memiliki jumlah tenaga pendidik lebih dari lima ratus orang.

**Werkudara** diciptakan untuk menjadi solusi atas permasalahan sinkronisasi data dosen di BIMA. **Werkudara** adalah aplikasi penyinkronisasi jamak data dosen yang ditulis dalam bahasa pemrograman Python dan dibangun di atas kerangka antarmuka PyQt5. Program ini merupakan pengakses tidak resmi (artinya, tidak dibuat oleh pihak yang berafiliasi dengan Kemdikbudristek) dari API BIMA, yang memberikan penggunanya kemampuan untuk melakukan sinkronisasi sebagian atau semua data dosen di BIMA secara serentak, harus membuka profil dosen secara manual, satu per satu.

**Werkudara** merupakan aplikasi sumber terbuka yang memiliki lisensi [GNU General Public License v3.0](https://spdx.org/licenses/GPL-3.0-or-later.html). Artinya, siapa saja boleh mengunduh kode sumber **Werkudara**, memodifikasi sebagian atau seluruh program, serta mendistribusikannya baik untuk tujuan komersial ataupun non-komersial, _selama tidak menggunakan nama program yang sama **dan** dengan memberikan atribusi kepada penulis asli **Werkudara**_.

**Werkudara** dibuat oleh S. Lykamanuella, mahasiswa S1 Fisika Universitas Kristen Satya Wacana (UKSW). Aplikasi ini dipersembahkan untuk Direktorat Riset dan Pengabdian Masyarakat UKSW serta seluruh universitas di Indonesia yang menggunakan sistem informasi BIMA dalam menjalankan operasional pendidikan tinggi.

Dengan adanya program **Werkudara** ini, diharapkan operator BIMA di universitas-universitas di seluruh Indonesia (tidak terbatas pada UKSW saja) dapat dipermudah dalam melakukan proses pemutakhiran data penelitian, pengabdian masyarakat, dan kepegawaian dari dosen dan peneliti pada instansi pendidikan tinggi masing-masing.

### B. Persiapan

#### B.1. Pengunduhan Program

Pastikan Anda telah mengunduh dan memasang Python di komputer Anda. Untuk dapat mengonfigurasi Python, Anda dapat mengunjungi situs [https://www.python.org](https://www.python.org).

Setelah Python terpasang pada sistem operasi yang Anda pakai, bukalah terminal (_Command Prompt_ pada Windows, _CLI_ pada Linux) lalu ketikkan perintah berikut:

```
pip install --upgrade werkudara
```

Perintah tersebut akan mengunduh serta menginstal **Werkudara** dari situs web [PyPI](https://pypi.org/project/werkudara) (Python Package Index). Anda juga dapat mengunduh dan menjalankan **Werkudara** secara manual melalui [repositori sumber terbuka **Werkudara**](https://github.com/groaking/werkudara).

> ![.](https://github.com/groaking/werkudara/blob/main/docs/1.png?raw=true)
> 
> **Gambar 1:** Werkudara sebagaimana ditampilkan pada situs web PyPI.

#### B.2. Instalasi

**Werkudara** adalah program portabel. Karena itu, **Werkudara** dapat dijalankan pada sistem operasi kompatibel tanpa memerlukan instalasi terlebih dahulu.

#### B.3. Menjalankan Program

Pastikan komputer Anda terhubung ke internet sebelum Anda menjalankan program **Werkudara**. Kemudian, buka terminal pada sistem operasi Anda dan ketikkan perintah di bawah:

```
python -m werkudara
```

Ketika program telah selesai termuat, maka akan muncul tampilan seperti pada gambar berikut.

> ![.](https://github.com/groaking/werkudara/blob/main/docs/2.png?raw=true)
> 
> **Gambar 2:** Jendela utama aplikasi Werkudara.

### C. Penggunaan Aplikasi Werkudara

#### C.1. Login Kredensial Operator BIMA Kemdikbud

Masukkan kredensial akun operator BIMA Anda, seperti _username_ dan _password_, sesuai dengan akun operator BIMA dari institusi afiliasi Anda. Anda dapat mencentang opsi `Remember Me` untuk menyimpan kredensial operator BIMA Anda secara lokal, sehingga Anda tidak perlu melakukan _login_ setiap kali membuka **Werkudara**. Kemudian tekan tombol `LOGIN`. Maka proses validasi kredensial akan dimulai.

> ![.](https://github.com/groaking/werkudara/blob/main/docs/3.png?raw=true)
> 
> **Gambar 3:** Jendela memasukkan kredensial operator BIMA.

Jika kredensial operator BIMA benar, maka akan muncul pesan seperti gambar berikut.

> ![.](https://github.com/groaking/werkudara/blob/main/docs/4.png?raw=true)
> 
> **Gambar 4:** Pesan berhasil log masuk.

Jika gagal, periksa koneksi internet dan kredensial operator BIMA Anda, lalu coba lagi.

#### C.2. Memuat Daftar Dosen yang Terdaftar BIMA

Setelah Anda berhasil log masuk menggunakan akun operator BIMA yang Anda miliki, Anda perlu menyinkronkan data dosen BIMA lokal dengan data yang ada di server Kemdikbud. Caranya, klik tombol `Refresh Online Data` pada dasbor utama aplikasi **Werkudara**.

> ![.](https://github.com/groaking/werkudara/blob/main/docs/5.png?raw=true)
>
> **Gambar 5:** Tampilan dasbor utama aplikasi **Werkudara**.

Ketika sinkronisasi data berhasil dilakukan, Anda akan melihat statistik dosen dan peneliti yang ada di universitas Anda pada panel di sebelah kanan. Jika sinkronisasi gagal, periksa koneksi internet Anda, lalu coba lagi.

#### C.3. Proses Pemutakhiran Data Peneliti dan Dosen

Pilih tab `Sync Selection` untuk membuka jendela pemutakhiran data peneliti dan dosen pada institusi Anda. Kemudian, tentukan apakah Anda ingin memutakhirkan data dari semua dosen dan peneliti yang ada dalam institusi perguruan tinggi Anda, atau hanya beberapa dosen dan peneliti spesifik yang datanya akan dimutakhirkan. Jika Anda ingin menyinkronisasi data publikasi semua dosen dan peneliti BIMA, pilih opsi `Sync all BIMA lecturers`. Sebaliknya, jika hanya beberapa akun yang perlu dimutakhirkan, pilih opsi `Only sync selected authors` otak pada panel sebelah kanan menunjukkan daftar peneliti dan dosen yang datanya akan dimutakhirkan secara spesifik.

Setelah selesai menentukan peneliti dan dosen yang datanya akan dimutakhirkan, klik tombol `Sync Now!`. Maka proses pemutakhiran data akan dimulai, dan log proses akan berjalan, seperti ditunjukkan oleh gambar berikut:

> ![.](https://github.com/groaking/werkudara/blob/main/docs/6.png?raw=true)
>
> **Gambar 6:** Panel berjalannya proses pemutakhiran data dosen dan peneliti melalui aplikasi **Werkudara**.

Tunggu sampai proses pemutakhiran data selesai, dan bar progres menunjukkan angka 100%. Setelah selesai, akan muncul notifikasi seperti ditunjukkan oleh gambar berikut.

> ![.](https://github.com/groaking/werkudara/blob/main/docs/7.png?raw=true)
>
> **Gambar 7:** Notifikasi bahwa pemutakhiran data peneliti dan dosen BIMA melalui **Werkudara** telah berhasil dilakukan.

Jika proses pemutakhiran gagal, periksa koneksi internet Anda, lalu coba lagi.

#### C.4. Menampilkan Detil Data Dosen dan Peneliti

Salah satu keunggulan aplikasi **Werkudara** adalah adanya fitur penampil data personal dosen dan peneliti secara detil. Hal ini dilakukan tanpa perlu membuka peramban _browser_ dan melakukan log masuk akun operator BIM secara manual.

Untuk dapat menggunakan fitur penampil data dosen dan peneliti, pertama-tama lakukan sinkronisasi data dengan server BIMA, seperti yang telah dijabarkan pada [**Bagian C.2**](https://github.com/groaking/werkudara#c2-memuat-daftar-dosen-yang-terdaftar-bima). Setelah itu, pilih tab `Lecturer Info`, lalu pilih dosen atau peneliti yang detil informasinya ingin dilihat melalui panel sebelah kiri. Tampilan informasi dosen dan peneliti adalah seperti ditunjukkan pada gambar berikut:

> ![.](https://github.com/groaking/werkudara/blob/main/docs/8.png?raw=true)
>
> **Gambar 8:** Tampilan informasi dosen dan peneliti sesuai data pada BIMA.

### D. Mengakhiri Program

Jika tidak operasi lain yang perlu Anda lakukan melalui **Werkudara**, Anda dapat menutup program **Werkudara** dengan menekan tombol `X` atau dengan memilih opsi `File > Quit` untuk keluar dari program **Werkudara**.

### E. Penutup

Kami membuka diri selebar-lebarnya terhadap masukan serta saran dari Anda. Jika ada pertanyaan, keluhan, saran, atau kritik yang ingin Anda ajukan terkait program **Werkudara**, dapat Anda kirimkan ke alamat surel sebagai berikut.

[`lykamanuella@outlook.com`](mailto:lykamanuella@outlook.com)

Anda juga dapat berkontribusi secara langsung terhadap pengembangan program **Werkudara** dengan menyunting langsung kode sumber program dan mengirimkan _pull request_, membuka isu program, dan menyarankan fitur baru dengan turut berkontribusi dalam repositori GitHub di repositori berikut:

[https://github.com/groaking/werkudara](https://github.com/groaking/werkudara)

Terima kasih atas minat Anda terhadap program **Werkudara**!

## Acknowledgement

This module uses and modifies some part of the code in [`save-thread-result`](https://github.com/shailshouryya/save-thread-result) v0.1.1.post1 by [**shailshouryya**](https://github.com/shailshouryya). Licensed under the [MIT License](https://spdx.org/licenses/MIT.html). Copyright (C) 2023 by the respective owner(s).
