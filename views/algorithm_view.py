"""
Algoritma Detayları Görünüm Modülü

Bu modül, algoritma detaylarını ve bilgilerini görüntülemek için fonksiyonlar içerir.
"""

import streamlit as st
import pandas as pd
from algorithms.timsort import timsort
from algorithms.introsort import introsort
from algorithms.radixsort import radixsort
from algorithms.cache_oblivious import cache_oblivious_sort
from algorithms.adaptive_mergesort import adaptive_mergesort
from algorithms.smoothsort import smoothsort

# Algoritma bilgileri - Her algoritma için tutarlı renkler
ALGORITHM_INFO = {
    "TimSort": {
        "func": timsort,
        "description": "Python'un varsayılan sıralama algoritmasıdır. MergeSort ve InsertionSort'un avantajlarını birleştirir. Özellikle kısmen sıralı verilerde çok etkilidir.",
        "best_case": "O(n)",
        "avg_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "adım_sayısı": "Düşük",
        "bellek_kullanımı": "Orta",
        "kararlılık": "Kararlı",
        "özellik": "Adaptif",
        "yıl": "2002",
        "yaratıcı": "Tim Peters",
        "renk": "#3399FF",  # Her algoritmaya özgü renk
        "ikon": "🔄",
        "plot_color": "#3399FF"  # Plotly grafiklerinde tutarlı renk için
    },
    "IntroSort": {
        "func": introsort,
        "description": "QuickSort'un en kötü durum performansını iyileştirmek için QuickSort, HeapSort ve InsertionSort'u birleştirir. En kötü durum senaryolarında bile iyi performans gösterir.",
        "best_case": "O(n log n)",
        "avg_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "adım_sayısı": "Orta",
        "bellek_kullanımı": "Düşük",
        "kararlılık": "Kararsız",
        "özellik": "Hibrit",
        "yıl": "1997",
        "yaratıcı": "David Musser",
        "renk": "#FF4081",
        "ikon": "⚡",
        "plot_color": "#FF4081"
    },
    "RadixSort": {
        "func": radixsort,
        "description": "Sayıları basamak basamak sıralayan karşılaştırma yapmadan çalışan bir algoritma. Özellikle tam sayı dizilerinde çok etkilidir.",
        "best_case": "O(nk)",
        "avg_case": "O(nk)",
        "worst_case": "O(nk)",
        "adım_sayısı": "Düşük",
        "bellek_kullanımı": "Yüksek",
        "kararlılık": "Kararlı",
        "özellik": "Karşılaştırmasız",
        "yıl": "1887",
        "yaratıcı": "Herman Hollerith",
        "renk": "#00C853",
        "ikon": "🔢",
        "plot_color": "#00C853"
    },
    "Cache-Oblivious": {
        "func": cache_oblivious_sort,
        "description": "Bellek hiyerarşisi hakkında özel bilgi olmadan tüm bellek seviyeleri için verimli çalışır. Modern işlemcilerin önbellek yapısından faydalanır.",
        "best_case": "O(n log n)",
        "avg_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "adım_sayısı": "Orta",
        "bellek_kullanımı": "Düşük",
        "kararlılık": "Kararlı",
        "özellik": "Önbellek verimli",
        "yıl": "1999",
        "yaratıcı": "Harald Prokop",
        "renk": "#2196F3",
        "ikon": "💾",
        "plot_color": "#2196F3"
    },
    "Adaptive MergeSort": {
        "func": adaptive_mergesort,
        "description": "MergeSort'un bir varyasyonu, kısmen sıralı dizilerde daha iyi performans gösterir. Veri setindeki mevcut sıralama özelliklerini tespit edip kullanır.",
        "best_case": "O(n)",
        "avg_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "adım_sayısı": "Düşük-Orta",
        "bellek_kullanımı": "Orta",
        "kararlılık": "Kararlı",
        "özellik": "Adaptif",
        "yıl": "1993",
        "yaratıcı": "Peter McIlroy",
        "renk": "#FF9800",
        "ikon": "📊",
        "plot_color": "#FF9800"
    },
    "SmoothSort": {
        "func": smoothsort,
        "description": "HeapSort'un bir varyasyonudur ve Leonardo sayılarını kullanır. Kısmen sıralı dizilerde daha verimli çalışır, teorik olarak en iyi durumda doğrusal zamanda çalışabilir.",
        "best_case": "O(n)",
        "avg_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "adım_sayısı": "Orta-Yüksek",
        "bellek_kullanımı": "Düşük",
        "kararlılık": "Kararsız",
        "özellik": "Adaptif",
        "yıl": "1981",
        "yaratıcı": "Edsger Dijkstra",
        "renk": "#9c27b0",
        "ikon": "🧩",
        "plot_color": "#9c27b0"
    }
}

def show_algorithm_details():
    """Algoritma detayları sekmesinin içeriğini gösterir"""
    # Sayfa göstergesi (aktif sekme)
    st.markdown('<span class="page-indicator"><span class="page-indicator-icon">📚</span> Algoritma Detayları</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-container">
        <div class="premium-subheader">Algoritma Bilgileri</div>
    """, unsafe_allow_html=True)
    
    # Karşılaştırma tablosu - Görsel iyileştirmelerle
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<div class='premium-card-title'>🔍 Algoritma Karşılaştırma Tablosu</div>", unsafe_allow_html=True)
    
    # Algoritma bilgi kutusu
    st.markdown("""
    <div class="info-box">
        <div class="info-box-title">
            <span class="info-box-icon">💡</span> Karşılaştırma Tablosu
        </div>
        <p>Aşağıdaki tablo, tüm algoritmaların temel özelliklerini bir arada gösterir. Sütun başlıklarına tıklayarak sıralama yapabilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Algoritmaları tablo olarak göster - İkonları içeren zenginleştirilmiş versiyon
    algo_data = []
    for algo_name, info in ALGORITHM_INFO.items():
        algo_data.append({
            "Algoritma": f"{info['ikon']} {algo_name}",
            "En İyi Durum": info["best_case"],
            "Ortalama Durum": info["avg_case"],
            "En Kötü Durum": info["worst_case"],
            "Adım Sayısı": info["adım_sayısı"],
            "Bellek Kullanımı": info["bellek_kullanımı"],
            "Kararlılık": info["kararlılık"],
            "Özellik": info["özellik"],
            "Yıl": info["yıl"],
            "Yaratıcı": info["yaratıcı"]
        })
    
    # Veriyi DataFrame'e dönüştür
    algo_df = pd.DataFrame(algo_data)
    
    # Tabloyu göster
    st.dataframe(algo_df.set_index("Algoritma"), width=1200)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Her algoritma için detaylı bilgi kartları
    st.markdown('<div class="premium-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-subheader">Algoritma Detayları</div>', unsafe_allow_html=True)
    
    # Algoritma arama ve filtreleme - Modernize edilmiş
    st.markdown("""
    <div style="position: relative; margin-bottom: 30px;">
        <div style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: var(--accent1); font-size: 1.2rem;">🔍</div>
        <input type="text" id="algo-search" placeholder="Algoritma adı ara..." style="width: 100%; padding: 12px 20px 12px 45px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; font-size: 1rem; color: white;">
    </div>
    """, unsafe_allow_html=True)
    
    algo_search = st.text_input("", key="algo_search_input", label_visibility="collapsed")
    
    # Her algoritma için bilgi kartı oluştur - CSS sınıfları eklenmiş
    filtered_algos = [algo for algo in ALGORITHM_INFO.keys() if algo_search.lower() in algo.lower()]
    
    if not filtered_algos:
        st.info("Arama kriterine uygun algoritma bulunamadı!")
    else:
        st.markdown("<div class='mui-card-grid'>", unsafe_allow_html=True)
        
        for i, algo_name in enumerate(filtered_algos):
            info = ALGORITHM_INFO[algo_name]
            css_class = algo_name.lower().replace(' ', '-').replace('-', '-')
            
            st.markdown(f"""
            <div class="algo-card {css_class}">
                <h3>{info["ikon"]} {algo_name}</h3>
                <p>{info["description"]}</p>
                <div class="algo-property">
                    <span class="property-name">En İyi Durum:</span>
                    <span class="property-value">{info["best_case"]}</span>
                </div>
                <div class="algo-property">
                    <span class="property-name">Ortalama Durum:</span>
                    <span class="property-value">{info["avg_case"]}</span>
                </div>
                <div class="algo-property">
                    <span class="property-name">En Kötü Durum:</span>
                    <span class="property-value">{info["worst_case"]}</span>
                </div>
                <div class="algo-property">
                    <span class="property-name">Kararlılık:</span>
                    <span class="property-value">{info["kararlılık"]}</span>
                </div>
                <div class="algo-property">
                    <span class="property-name">Yaratıcı:</span>
                    <span class="property-value">{info["yaratıcı"]} ({info["yıl"]})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
                
    # Algoritma çalışma prensipleri
    st.markdown('<div class="premium-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-subheader">Çalışma Prensipleri</div>', unsafe_allow_html=True)
    
    # Algoritma seç
    selected_algo = st.selectbox("Algoritma seçin:", list(ALGORITHM_INFO.keys()), key="algo_select")
    
    # Tooltip bilgi balonu eklendi
    st.markdown("""
    <div class="tooltip-container">
        <span>Algoritmanın detaylarını incelemek için seçim yapın</span>
        <span class="tooltip-icon">i</span>
        <span class="tooltip-text">Her algoritmanın çalışma prensiplerini adım adım görebilirsiniz. Ayrıca "flip card" özelliği ile performans profilini inceleyebilirsiniz.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Seçilen algoritmanın çalışma prensibini açıkla - Görsel olarak zenginleştirilmiş
    if selected_algo == "TimSort":
        st.markdown("""
        <div class="premium-card">
            <div class="premium-card-title">🔄 TimSort Nasıl Çalışır?</div>
            <div class="step-card">
                <span class="step-number">1</span>
                <span class="step-title">Veriyi Alt Dizilere Böl</span>
                <div class="step-content">
                    TimSort, önce diziyi minrun adı verilen küçük alt dizilere böler. Minrun değeri, dizinin boyutuna bağlı olarak hesaplanır ve genellikle 32-64 arasındadır.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">2</span>
                <span class="step-title">Alt Dizileri Sırala</span>
                <div class="step-content">
                    Her alt dizi, Insertion Sort algoritması kullanılarak sıralanır. Insertion Sort küçük diziler için oldukça verimlidir.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">3</span>
                <span class="step-title">Alt Dizileri Birleştir</span>
                <div class="step-content">
                    Sıralanmış alt diziler, Merge Sort tekniği kullanılarak birleştirilir. Bu süreçte, "galloping" adı verilen bir optimizasyon kullanılarak, bazı durumlarda gereksiz karşılaştırmalar önlenir.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">4</span>
                <span class="step-title">Uyarlamalı Strateji</span>
                <div class="step-content">
                    TimSort, verideki mevcut sıralama düzenine adapte olabilir. Sıralı "run"ları tespit edip kullanarak performansını artırır. Bu nedenle kısmen sıralı verilerde çok verimlidir.
                </div>
            </div>
            
            <div class="info-box">
                <div class="info-box-title">
                    <span class="info-box-icon">💡</span> Uygulama Alanları
                </div>
                <p>TimSort, Python, Java, Android ve birçok modern programlama dilinde varsayılan sıralama algoritması olarak kullanılır. Özellikle uygulama verilerinde, veritabanı sonuçlarında ve metin dosyalarında sıralama yapmak için idealdir.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3D Flip Kart - Modernize edilmiş
        st.markdown("""
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div class="flip-card-title">🔄 TimSort</div>
                    <p style="margin: 15px 0; color: rgba(255, 255, 255, 0.7);">Fare ile üzerine gelin!</p>
                    <span class="complexity-badge">O(n log n)</span>
                </div>
                <div class="flip-card-back">
                    <div class="flip-card-title">⭐ Performans Profili</div>
                    <div class="premium-badge badge-primary">En İyi: O(n)</div>
                    <div class="premium-badge badge-secondary">Ortalama: O(n log n)</div>
                    <div class="premium-badge badge-tertiary">En Kötü: O(n log n)</div>
                    <p style="margin-top: 15px; color: white;">Kısmen sıralı dizilerde çok hızlı!</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif selected_algo == "IntroSort":
        st.markdown("""
        <div class="premium-card">
            <div class="premium-card-title">⚡ IntroSort Nasıl Çalışır?</div>
            <div class="step-card">
                <span class="step-number">1</span>
                <span class="step-title">QuickSort ile Başla</span>
                <div class="step-content">
                    IntroSort, öncelikle QuickSort algoritmasını kullanmaya başlar. QuickSort genel durumlarda hızlı performans gösterir.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">2</span>
                <span class="step-title">Derinlik Kontrolü</span>
                <div class="step-content">
                    Algoritma, rekürsif çağrıların derinliğini izler. Eğer derinlik belirli bir eşiği (genellikle 2*log2(n)) aşarsa, QuickSort'un en kötü durum senaryosuyla karşılaşıldığı düşünülür.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">3</span>
                <span class="step-title">HeapSort'a Geçiş</span>
                <div class="step-content">
                    Maksimum derinliğe ulaşıldığında, algoritma QuickSort'tan HeapSort'a geçer. HeapSort, en kötü durumda bile O(n log n) performans garantisi sağlar.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">4</span>
                <span class="step-title">Küçük Diziler İçin InsertionSort</span>
                <div class="step-content">
                    Alt dizilerin boyutu belirli bir eşiğin (genellikle 16) altına düştüğünde, InsertionSort kullanılır. InsertionSort küçük dizilerde çok verimlidir.
                </div>
            </div>
            
            <div class="info-box">
                <div class="info-box-title">
                    <span class="info-box-icon">💡</span> Uygulama Alanları
                </div>
                <p>IntroSort, C++ STL'in std::sort fonksiyonunda kullanılır. Genel amaçlı sıralama ihtiyaçları için her durumda iyi performans gösterir. Özellikle performans hassasiyeti olan uygulamalarda tercih edilir.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3D Flip Kart - Modernize edilmiş
        st.markdown("""
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div class="flip-card-title">⚡ IntroSort</div>
                    <p style="margin: 15px 0; color: rgba(255, 255, 255, 0.7);">Fare ile üzerine gelin!</p>
                    <span class="complexity-badge">O(n log n)</span>
                </div>
                <div class="flip-card-back">
                    <div class="flip-card-title">⭐ Performans Profili</div>
                    <div class="premium-badge badge-secondary">En İyi: O(n log n)</div>
                    <div class="premium-badge badge-secondary">Ortalama: O(n log n)</div>
                    <div class="premium-badge badge-secondary">En Kötü: O(n log n)</div>
                    <p style="margin-top: 15px; color: white;">Garantili bir performans sağlar!</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif selected_algo == "RadixSort":
        st.markdown("""
        <div class="premium-card">
            <div class="premium-card-title">🔢 RadixSort Nasıl Çalışır?</div>
            <div class="step-card">
                <span class="step-number">1</span>
                <span class="step-title">Basamaklara Göre Sırala</span>
                <div class="step-content">
                    RadixSort, sayıları basamak basamak sıralar. En düşük basamaktan (birler) başlayarak en yüksek basamağa doğru ilerler.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">2</span>
                <span class="step-title">Counting Sort Kullan</span>
                <div class="step-content">
                    Her basamak için Counting Sort uygulanır. Bu, her basamağın değerine göre sayıları sıralar (0-9 arası).
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">3</span>
                <span class="step-title">Sıralı Hali Güncelle</span>
                <div class="step-content">
                    Her basamak sıralamasından sonra, dizinin güncel hali bir sonraki basamak sıralaması için kullanılır.
                </div>
            </div>
            <div class="step-card">
                <span class="step-number">4</span>
                <span class="step-title">Tüm Basamaklar İçin Tekrarla</span>
                <div class="step-content">
                    Bu işlem, en büyük sayının tüm basamakları sıralanana kadar devam eder.
                </div>
            </div>
            
            <div class="info-box">
                <div class="info-box-title">
                    <span class="info-box-icon">💡</span> Uygulama Alanları
                </div>
                <p>RadixSort, özellikle tam sayı dizilerinde ve sabit boyutlu verilerde (örneğin IP adresleri, tarihler, posta kodları) etkilidir. Büyük veri setlerinde veya paralel işleme gerektiren uygulamalarda da tercih edilebilir.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3D Flip Kart - Modernize edilmiş
        st.markdown("""
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div class="flip-card-title">🔢 RadixSort</div>
                    <p style="margin: 15px 0; color: rgba(255, 255, 255, 0.7);">Fare ile üzerine gelin!</p>
                    <span class="complexity-badge">O(nk)</span>
                </div>
                <div class="flip-card-back">
                    <div class="flip-card-title">⭐ Performans Profili</div>
                    <div class="premium-badge badge-primary">En İyi: O(nk)</div>
                    <div class="premium-badge badge-secondary">Ortalama: O(nk)</div>
                    <div class="premium-badge badge-tertiary">En Kötü: O(nk)</div>
                    <p style="margin-top: 15px; color: white;">Tam sayı dizilerinde süper performans!</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)