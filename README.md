# 🚀 Gelişmiş Sıralama Algoritmaları Karşılaştırma Arayüzü

Modern sıralama algoritmalarını interaktif olarak görselleştirin ve performanslarını karşılaştırın.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.19%2B-FF4B4B?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📖 Proje Hakkında

Bu uygulama, 6 farklı gelişmiş sıralama algoritmasını görselleştirmenize ve performanslarını karşılaştırmanıza olanak tanır. Streamlit framework'ü kullanılarak geliştirilmiş modern ve interaktif bir web uygulamasıdır.

### ✨ Özellikler

- 🎬 **Gerçek zamanlı animasyonlar** - Algoritmaların adım adım çalışmasını izleyin
- 📊 **Performans analizi** - Zaman, bellek ve karşılaştırma sayısı metrikleri
- 🔬 **Çoklu veri türleri** - Rastgele, sıralı, ters sıralı ve kısmen sıralı veri testleri
- 📈 **İnteraktif grafikler** - Plotly ile detaylı görselleştirmeler
- 🎨 **Modern UI** - Karanlık tema ve responsive tasarım
- 💾 **CSV dışa aktarma** - Sonuçlarınızı kaydedin


## 📥 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri

### Adımlar

```bash
# 1. Depoyu klonlayın
git clone https://github.com/kullaniciadi/algoritma_karsilastirma.git
cd algoritma_karsilastirma

# 2. Sanal ortam oluşturun (önerilen)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Uygulamayı çalıştırın
streamlit run app.py
```

Uygulama `http://localhost:8501` adresinde açılacaktır.

---

## 🎮 Kullanım

1. **Yan panel**'den veri türü ve boyutunu seçin
2. Test etmek istediğiniz **algoritmaları** işaretleyin
3. **Animasyon hızını** ayarlayın
4. **"ANALİZİ BAŞLAT"** butonuna tıklayın
5. Sonuçları **4 farklı sekmede** inceleyin:
   - 📈 **Animasyonlar** - Algoritmaların çalışmasını izleyin
   - 🔍 **Performans** - Detaylı metrikler ve karşılaştırmalar
   - 📚 **Algoritma Detayları** - Her algoritma hakkında bilgi
   - 📊 **Veri Analizi** - Veri dağılımları ve istatistikler

---

## 📁 Proje Yapısı

```
algoritma_karsilastirma/
├── app.py                      # Ana uygulama
├── requirements.txt            # Bağımlılıklar
├── algorithms/                 # Algoritma implementasyonları
├── utils/                      # Yardımcı araçlar (data_generator, metrics, visualizer)
├── views/                      # UI bileşenleri
├── animation_utils.py          # Animasyon fonksiyonları
├── data/                       # Örnek veri dosyaları
└── results/                    # Analiz sonuçları
```



---

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Geliştirici

**Hüriye Yıldırım**

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!

