# hogaim
Kodun amacı, bir ekran kaydedici ve otomatik hedefleme sistemi (aimbot) geliştirmektir. Ancak, bu tür yazılımlar çevrimiçi oyunlarda kullanıldığında hile sayılabilir ve oyun geliştiricileri tarafından tespit edilerek ceza uygulanabilir. Bu kod bir hile (aimbot) yazılımı içerdiği için kullanımı birçok oyunda yasaktır. Hile tespit sistemleri (Vanguard, Easy Anti-Cheat, vb.) bu tarz yazılımları tespit edebilir ve oyuncuları kalıcı olarak yasaklayabilir. Kodun kimliğini, yapısını gizleme ve oyun güvenliğini kapama kodu geliştirmelisiniz. Eğitim, kişisel veya bilimsel araştırmalar için örnektir.

Kullanılan Kütüphaneler

Kodda kullanılan ana kütüphaneler şunlardır:

sys: Sistemle ilgili işlemler yapmak için kullanılır.
cv2 (OpenCV): Görüntü işleme işlemleri için kullanılır.
numpy: Matematiksel işlemler ve görüntü analizi için kullanılır.
random: Rastgelelik eklemek için kullanılır.
time: Zaman gecikmeleri eklemek için kullanılır.
win32api, win32con, win32gui: Windows işletim sistemi üzerinde fare ve pencere yönetimi işlemleri için kullanılır.
mss: Ekran görüntüsü almak için kullanılır.
PyQt5: Grafiksel kullanıcı arayüzü (GUI) oluşturmak için kullanılır.

ScreenRecorderAlpha Sınıfı

Kodun ana kısmı ScreenRecorderAlpha adlı bir PyQt5 tabanlı arayüz sınıfıdır. Bu sınıfın işlevleri:

2.1. Yapıcı Metot (__init__)

Pencerenin başlığı "Screen Recorder Alpha" olarak ayarlanıyor.
Pencere boyutu 800x600 olarak belirleniyor.
Uygulama simgesi "camera.ico" olarak ayarlanıyor.

Çeşitli değişkenler tanımlanıyor:

Oyun durumu (self.game_running): Hedefleme sisteminin aktif olup olmadığını belirler.
Nişangah boyutu (self.crosshair_size): Hedefleme çapını belirler.
Zoom modu (self.zoom_mode): Yakınlaştırma modu olup olmadığını belirler.
Hedefleme gecikmeleri (self.aim_smooth_min, self.aim_smooth_max): Otomatik hedefleme sırasında fare hareketinin ne kadar hızlı olması gerektiğini belirler.
Tıklama gecikmeleri (self.click_delay_min, self.click_delay_max): Tıklama hızlarını belirler.
Baş vuruş olasılığı (self.headshot_probability): %80 ihtimalle düşmanın kafasına nişan alır.
Hedef pencere adı (self.target_window_name): "test" olarak belirlenmiş, yani kod sadece bu pencere aktif olduğunda çalışır.
Renk filtresi (self.hsv_lower, self.hsv_upper): Mor renk aralığını tespit etmek için HSV renk uzayında sınırları belirler.

Kullanıcı Arayüzünü Başlatma (init_ui)

Video akışı gösterecek bir QLabel bileşeni ekleniyor.
Hedefleme hassasiyetini ayarlamak için QSpinBox kullanılıyor.
Zoom modu açma/kapatma butonu ekleniyor.
Başlat ve durdur butonları ekleniyor.

Hedefleme Sistemi

Kodda, düşman tespiti ve otomatik nişan alma için şu işlemler yapılıyor:

3.1. is_game_window_active Metodu

Bu metod, aktif pencerenin "var" olup olmadığını kontrol eder. Eğer oyun penceresi aktif değilse, sistem çalışmaz.

3.2. is_purple_detected Metodu

Bu metod:
Ekrandaki görüntü bölgesini HSV renk uzayına çevirir.
Belirlenen mor renk aralığında kaç piksel olduğunu hesaplar.
Eğer bu pikseller toplam görüntünün belirli bir yüzdesinden fazlaysa (0.02 ile 0.3 arasında), düşmanın tespit edildiği kabul edilir.
3.3. process_frame Metodu
Bu metod ekran görüntüsü alarak HOG (Histogram of Oriented Gradients) tabanlı insan tespiti algoritmasını uygular:
Ekran görüntüsü alınır (1920x1080 piksel).

Görüntü işlenir:

Açık pencereden ekran görüntüsü alınır.
Renk uzayı cv2.COLOR_BGRA2BGR ile dönüştürülür.
HOGDescriptor kullanılarak nesne tespiti yapılır.
Hedef belirleme ve nişan alma işlemi:
Algılanan her nesne için merkezi koordinat hesaplanır.
Nişangahın alanı içinde olup olmadığı kontrol edilir.
Eğer mor renk tespit edilirse veya rastgele bir faktör geçerse, farenin hedefe yöneltilmesi sağlanır.
Eğer hedef düşmanın kafasına yakınsa, nişan alınır ve sol tıklama gerçekleştirilir.
Eğer hedef bulunamazsa, kayıp hedef çerçeve sayacı artırılır.

3.4. move_mouse ve left_click Metotları

move_mouse(x, y): Farenin pozisyonunu belirlenen koordinatlara taşır.
left_click(): Sol tıklama işlemini simüle eder.

Uygulama Akışı

Program başlatıldığında, ScreenRecorderAlpha sınıfı başlatılır ve PyQt5 arayüzü görüntülenir.
Kullanıcı "Start" butonuna tıklarsa, self.timer.start(5) metodu çağrılır ve her 5 ms'de bir yeni kare işlenir.
Program sürekli ekran görüntüsü alır, insanları tespit eder, mor renge göre hedef belirler ve fareyi o yöne hareket ettirerek ateş eder.
Kullanıcı "Stop" butonuna tıklarsa, hedefleme sistemi durdurulur.

Kod, bilgisayardaki ekran görüntüsünü analiz ederek hedef belirleyen, farenin konumunu otomatik olarak ayarlayan ve atış yapan bir otomatik hedefleme sistemi içerir. Ancak bu tür sistemlerin hile olarak kabul edilebileceği ve oyun kurallarına aykırı olabileceği unutulmamalıdır.

Bu Python kodunun çalışması için gerekli olan kütüphaneleri yüklemek ve çalıştırılabilir (.exe) dosya oluşturmak için aşağıdaki adımları takip edebilirsiniz:

Gerekli kütüphaneleri yüklemek için aşağıdaki komutu terminal veya komut istemcisine yazın:

pip install opencv-python numpy pyqt5 pyqt5-tools pyinstaller mss pywin32

Python Kodunu .exe Dosyasına Dönüştürme
Python kodunuzu exe formatına çevirmek için PyInstaller kullanabilirsiniz.
Aşağıdaki komutu çalıştırarak .exe dosyası oluşturabilirsiniz:

pyinstaller --onefile --windowed --icon=camera.ico aimasistant.py
