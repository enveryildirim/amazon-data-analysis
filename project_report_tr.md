# Büyük Veri Proje Raporu: Amazon Satış Verisi Analizi

## 1. Giriş

Rekabetin yoğun olduğu e-ticaret sektöründe, büyümeyi sürdürmek ve operasyonel verimliliği sağlamak için veriye dayalı karar alma süreçleri hayati önem taşımaktadır. Bu proje, Amazon'un satış verilerinden eyleme dönüştürülebilir içgörüler elde etmek için büyük veri analitiğini kullanmayı amaçlamaktadır. Temel hedef, iş stratejisini optimize etmek için geçmiş satış modellerini, operasyonel maliyetleri ve envanter dağılımını analiz etmektir. Ayrıca proje, gelecekteki satış performansını tahmin etmek için makine öğrenimi uygulamalarını araştırarak daha doğru gelir tahmini ve kaynak planlaması yapılmasını sağlamaktadır.

## 2. Veri Tanımı

Bu analizin temeli, perakende operasyonunun çeşitli yönlerini temsil eden kapsamlı bir veri seti ekosistemine dayanmaktadır. Ana veri seti olan `amazon_sales`, analiz için istatistiksel olarak anlamlı bir örneklem sağlayan yaklaşık **128.976 kayıttan** oluşmaktadır.

### Veri Setlerine Genel Bakış

- **`amazon_sales`**: Temel işlem veri seti. Önemli öznitelikler şunlardır:
  - **Sipariş Detayları**: `Order ID` (Sipariş Kimliği), `Date` (Tarih), `Status` (Durum), `Fulfilment` (Teslimat Yöntemi).
  - **Ürün Detayları**: `SKU` (Stok Kodu), `Category` (Kategori), `Size` (Beden), `ASIN` (Amazon Standart Kimlik Numarası).
  - **Finansallar**: `Amount` (Gelir), `Currency` (Para Birimi).
  - **Müşteri Konumu**: `ship-city` (Şehir), `ship-state` (Eyalet/İl), `ship-postal-code` (Posta Kodu).
- **`international_sales`**: Sınır ötesi işlem nüanslarını kapsayan ek veriler.
- **`inventory`**: Satış hızı ile bulunabilirliği ilişkilendirmek için gerekli olan, SKU'lar ve Kategoriler bazında stok seviyelerinin anlık görüntüsü.
- **`pricing_may2022` & `pricing_march2021`**: İndirim ve marj analizi sağlayan, Minimum Perakende Fiyatı (MRP) ile Satış Fiyatı referans tabloları.
- **`expenses`** & **`warehouse_costs`**: Net kârlılığı hesaplamak için kullanılan operasyonel maliyet verileri.

### Veri Kalitesi ve Ön İşleme

Gerçek dünya verileri titiz bir temizlik gerektirir. Atılan temel adımlar şunları içerir:

- **Eksik Değerlerin İşlenmesi**: `Amount` sütunu, iptal edilen veya iade edilen siparişler için boş değerler (null) içeriyordu. Bunlar, belirli analitik bağlama göre stratejik olarak `0` ile dolduruldu veya atıldı (örneğin, ortalama sipariş değeri hesaplaması için atıldı, toplam gelir hesaplaması için 0 olarak tutuldu).
- **Tür Dönüşümü**: `Date` sütunu, ayrıntılı zaman serisi analizi (Günlük, Aylık, Çeyreklik) yapabilmek için standart bir `Timestamp` formatına dönüştürüldü.
- **Şema Doğrulama**: Pipeline genelinde tutarlı veri türlerinin (örneğin `Qty` için Tamsayı, `Amount` için Ondalıklı Sayı) sağlanması.

## 3. Metodoloji ve Teknoloji Yığını

Veri setlerinin ölçeği ve karmaşıklığı göz önüne alındığında, proje **Apache Spark** ekosistemini kullanan bir "Önce Büyük Veri" yaklaşımını benimsemektedir.

### Teknoloji Yığını

- **Apache Spark (PySpark)**: Dağıtık hesaplama yetenekleri nedeniyle seçilmiştir. Spark'ın bellek içi (in-memory) işlemesi, standart tek düğümlü ortamlarda verimsiz olacak büyük veri setleri üzerinde hızlı yinelemeye olanak tanır.
- **Spark MLlib**: Ölçeklenebilir makine öğrenimi için kullanılmıştır. Pipeline mimarisi, özellik mühendisliği ve modelleme adımlarının tekrarlanabilir ve verimli olmasını sağlar.
- **Pandas & Matplotlib/Seaborn**: Spark'ın birleştirilmiş çıktılarını raporlama için yüksek kaliteli grafiklere dönüştürerek, veri görselleştirmenin son katmanı olarak kullanılmıştır.

### Analiz İş Akışı

1.  **ETL (Çıkarma, Dönüştürme, Yükleme)**: Ham Parquet/CSV dosyaları Spark DataFrame'lerine alındı.
2.  **Keşifsel Veri Analizi (EDA)**: Eğilimleri, aykırı değerleri ve dağılımları belirlemek için toplama fonksiyonları (`groupBy`, `count`, `sum`) kullanıldı.
3.  **Özellik Mühendisliği (Feature Engineering)**: Ham veriler makine öğrenimi için bir özellik vektörüne dönüştürüldü. Bu şunları içeriyordu:
    - **Zamansal Çıkarım**: `Year` (Yıl), `Month` (Ay), `Day` (Gün) ve `DayOfWeek` (Haftanın Günü) türetilmesi.
    - **Kategorik Kodlama**: `Category` gibi alanlar için `StringIndexer` ve `OneHotEncoder` kullanımı.
4.  **Modelleme**: 70/30 Eğitim/Test ayrımı üzerinde bir Doğrusal Regresyon (Linear Regression) modelinin eğitilmesi.

## 4. Analiz ve Bulgular

### 4.1 Satış Analizi ve Mevsimsellik

Satışların zamansal dağılımının incelenmesi, kritik operasyonel içgörüleri ortaya çıkarmaktadır.

**Aylık Satış Trendleri**:
![Aylık Satış Trendleri](notebooks/output/monthly_sales_trends.png)

**Yorum**:

- **2. Çeyrek Artışı**: **Nisan, Mayıs ve Haziran 2022** aylarında satışlarda belirgin bir artış var. Bu üç aylık dönem, muhtemelen büyük bir satış etkinliğine (örneğin Yaz İndirimi) veya belirli giyim türlerine (Kurtalar, Elbiseler) yönelik mevsimsel talebe karşılık gelmektedir.
- **Korelasyon**: Hacim (`Qty`) ve gelir (`Amount`) çizgileri neredeyse mükemmel bir senkronizasyonla hareket etmektedir. Bu, gelir artışının sadece yüksek fiyatlı ürün satışlarından değil, gerçek talep artışından kaynaklandığını göstermektedir.

### 4.2 Kategori Performansı

Ürün performansına derinlemesine bir bakış, gelirin çoğunu birkaç kategorinin oluşturduğu "Pareto İlkesi"ni vurgulamaktadır.

![Kategori Performansı](notebooks/output/category_performance.png)

**Temel İçgörüler**:

- **Baskın Kategoriler**: 'Set' (Etnik takımlar), 'Kurta' ve 'Western Dress' (Batı Tarzı Elbise) mutlak liderlerdir. İşlem hacminin büyük kısmını oluştururlar.
- **Stratejik Envanter**: Bu ilk 3 kategori için %100 bulunabilirlik sağlamak kritik öneme sahiptir. Buradaki herhangi bir stok tükenmesi, toplam gelir üzerinde orantısız bir etkiye sahip olacaktır.
- **Uzun Kuyruk (Long Tail)**: Grafiğin altındaki kategorilerin, uygulanabilirlik veya depo maliyetini düşürmek için tasfiye stratejileri açısından gözden geçirilmesi gerekebilir.

### 4.3 Sipariş Durumu Dağılımı

Platformun operasyonel sağlığı, sipariş durumlarına yansımaktadır.

![Sipariş Durumu Dağılımı](notebooks/output/order_status_distribution.png)

**Gözlemler**:

- **Teslimat Oranı**: 'Shipped' (Kargolandı) ve 'Delivered' (Teslim Edildi) durumları baskın olsa da, **'Cancelled' (İptal Edildi)** dilimi azımsanmayacak boyuttadır.
- **Aksiyon Öğesi**: İptal oranındaki %1-2'lik bir azalma bile önemli bir gelir geri kazanımıyla sonuçlanabilir. Kök neden analizi (Fiyat uyuşmazlığı? Stok tükenmesi? Uzun teslimat süresi?) önerilmektedir.

### 4.4 B2B ve B2C Analizi

Müşteri tabanı kompozisyonunu anlamak.

![B2B vs B2C](notebooks/output/b2b_vs_b2c.png)

**Analiz**:

- **Tüketici Odaklı**: Platform ezici bir çoğunlukla B2C (İşletmeden Tüketiciye) odaklıdır.
- **B2B Potansiyeli**: İşlem sayısında küçük olsa da, B2B siparişleri genellikle daha yüksek Ortalama Sipariş Değerine (AOV) sahiptir. Özel bir B2B portalı veya toplu alım teşvikleri bu segmenti besleyebilir.

### 4.5 Coğrafi Analiz

![Coğrafi Analiz](notebooks/output/geographic_analysis.png)

**Lojistik Etkiler**:

- Satışlar belirli eyaletlerde/şehirlerde yoğunlaşmıştır. Bu veriler **Depo yerleşimi** kararlarını yönlendirmelidir. Envanteri bu yüksek talep bölgelerine daha yakın konumlandırmak, nakliye maliyetlerini ve teslimat sürelerini azaltacak, böylece müşteri memnuniyetini artıracak ve muhtemelen iptalleri azaltacaktır.

## 5. Satış Tahmin Modeli

### Modelleme Stratejisi

Amaç, özelliklerine dayanarak belirli bir işlem için **Satış Tutarını (Sales Amount)** tahmin edebilen bir regresyon modeli oluşturmaktı. Bu, gelir tahmini için temel bir adımdır.

**Algoritma**: Doğrusal Regresyon (Linear Regression - Spark MLlib aracılığıyla).

### Özellik Mühendisliği Hattı (Pipeline)

Modelin tahmin gücü, girdi özelliklerinin kalitesine bağlıdır. Özel bir vektör tasarladık:

1.  **Zaman Bazlı**: `Month` (Ay), `Year` (Yıl), `Day` (Gün), `DayOfWeek` (Haftanın Günü), `Quarter` (Çeyrek).
2.  **Türetilmiş**: `is_weekend` (Hafta sonu mu - İkili), `is_holiday_season` (Tatil sezonu mu - İkili - Kasım/Aralık hedefli).
3.  **Ürün**: `Category` (İndekslenmiş), `Size` (İndekslenmiş).
4.  **Operasyonel**: `Status` (İndekslenmiş), `Qty` (Miktar), `B2B` (İkili).

Bu özellikler yoğun bir vektörde birleştirildi ve tekdüze etki sağlamak için `StandardScaler` kullanılarak ölçeklendi.

### Model Performansı ve Değerlendirme

Model, görülmemiş test verileri (%30 ayrım) üzerinde değerlendirildi.

- **RMSE (Kök Ortalama Kare Hatası): ~253.05**
  - _Anlamı_: Modelin tahminleri genellikle gerçek işlem değerinden ±253 para birimi kadar sapmaktadır. Ürünlerin fiyat aralığı göz önüne alındığında (muhtemelen 500-2000), bu orta düzeyde bir hata payıdır.
- **R2 Skoru: ~0.1066**
  - _Yorum_: Model, varyansın yaklaşık **%10.7**'sini açıklamaktadır.
  - _Bağlam_: Tüketici davranış verilerinde, ölçülmeyen dış faktörlerin (Kullanıcı niyeti, estetik, pazarlama baskısı, o andaki rakip fiyatlandırması) etkisi nedeniyle düşük R2 skorları yaygındır. Ancak %10, `Category` ve `Mevsimselliğin` önemli olduğunu, ancak fiyat/satış tutarının _tek_ belirleyicileri olmadığını göstermektedir.

![Gerçek ve Tahmin Edilen Karşılaştırması](notebooks/output/actual_vs_predicted.png)
_(Gerçek değerlere karşı tahminlerin dağılımını görselleştiren dağılım grafiği)_

## 6. Sonuç ve Öneriler

Bu proje, e-ticaret satışlarını analiz etmek ve modellemek için ölçeklenebilir bir Büyük Veri hattını başarıyla uygulamıştır.

### Stratejik Öneriler:

1.  **Envanter Optimizasyonu**: Mevsimsel artışı yakalamak için 2. Çeyrek (Nisan-Haziran) öncesinde 'Setler' ve 'Kurtalar' stoklarını yoğun bir şekilde artırın.
2.  **İptal Ekibi**: Durum Dağılımında görülen yüksek iptal hacminin belirli nedenlerine yönelik derinlemesine bir analiz yaptırın.
3.  **Veri Zenginleştirme**: Satış Tahmin Modelini (şu anda R2 ~0.11) geliştirmek için aşağıdaki gibi harici veri kaynaklarını entegre edin:
    - **Pazarlama Harcamaları**: Belirli günlerde/kategorilerde reklam harcaması.
    - **Rakip Fiyatlandırması**: Gerçek zamanlı fiyat takibi.
    - **Müşteri Demografisi**: Yaş, Cinsiyet, önceki satın alma geçmişi.

### Gelecek Çalışmalar

- Doğrusal olmayan ilişkileri yakalamak için **Gradient Boosted Trees (GBTs)** veya **Random Forest** regresörlerini uygulayın.
- İşlem başına tahmin yerine günlük gelir tahmini için özel olarak bir **Zaman Serisi Tahmin modeli (ARIMA veya Prophet)** geliştirin.
