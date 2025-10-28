"""
Sıralama Algoritmaları Karşılaştırma Uygulaması - İleri Düzey Premium MUI Tasarım

Bu uygulama, modern sıralama algoritmalarını görselleştirmeyi ve performanslarını
karşılaştırmayı sağlar.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time
from pathlib import Path

# Modül importu sorununu çözmek için proje kök dizinini path'e ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)  # Mevcut dizini en öncelikli yap

# Animasyon ve yardımcı modülleri import et
from animation_utils import (
    create_sorting_animation_plotly, 
    get_algorithm_statistics,
    create_color_legend,
    ALGORITHM_COLORS
)
from views.animations_view import (
    show_animations_tab, 
    show_empty_animation_state,
    show_algorithm_performance_comparison,
    display_algorithm_details
)

# Algoritma modüllerini import et
from algorithms.timsort import timsort
from algorithms.introsort import introsort
from algorithms.radixsort import radixsort
from algorithms.cache_oblivious import cache_oblivious_sort
from algorithms.adaptive_mergesort import adaptive_mergesort
from algorithms.smoothsort import smoothsort

# Yardımcı fonksiyonları import et
from utils.data_generator import generate_random_data, generate_nearly_sorted_data
from utils.metrics import measure_time, measure_memory, measure_comparisons
from utils.visualizer import create_comparison_chart, create_bar_chart, create_comparison_chart_melted

# Veri tipi bilgileri
VERI_TURLERI = {
    "random": {
        "func": generate_random_data,
        "desc": "Rastgele Veri"
    },
    "nearly_sorted": {
        "func": generate_nearly_sorted_data,
        "desc": "Kısmen Sıralı Veri"
    },
    "sorted": {
        "func": lambda size: sorted(generate_random_data(size)),
        "desc": "Sıralı Veri"
    },
    "reverse_sorted": {
        "func": lambda size: sorted(generate_random_data(size), reverse=True),
        "desc": "Ters Sıralı Veri"
    }
}

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
        "ikon": "🧩",
        "plot_color": "#9c27b0"
    }
}

# Session state için gerekli fonksiyonları tanımla
def initialize_session_state():
    """Session state değişkenlerini başlat"""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "animations"
    if 'algorithm_results' not in st.session_state:
        st.session_state.algorithm_results = {}
    if 'performance_results' not in st.session_state:
        st.session_state.performance_results = pd.DataFrame()

# Veri oluşturma fonksiyonu
def generate_data_by_type(data_type, size):
    """Belirtilen türe göre veri oluşturur."""
    if data_type not in VERI_TURLERI:
        st.error(f"Geçersiz veri türü: {data_type}")
        return None
    
    return VERI_TURLERI[data_type]["func"](size)

# Performans ölçüm fonksiyonu
def measure_algorithm_performance(algo_name, algo_func, data):
    """Algoritmanın performansını ölçer."""
    # Performans ölçümleri
    time_result = measure_time(algo_func, data.copy())
    memory_result = measure_memory(algo_func, data.copy())
    comparisons_result = measure_comparisons(algo_func, data.copy())
    
    return {
        "algorithm": algo_name,
        "time": time_result,
        "memory": memory_result,
        "comparisons": comparisons_result
    }

# Performans analizi fonksiyonu
def run_performance_analysis(data, selected_algos):
    """Seçilen algoritmalar için performans analizi yapar"""
    results = []
    
    with st.spinner("Performans ölçümleri yapılıyor..."):
        for algo_name in selected_algos:
            perf = measure_algorithm_performance(
                algo_name, 
                ALGORITHM_INFO[algo_name]["func"], 
                data.copy()
            )
            results.append(perf)
    
    # Sonuçları DataFrame'e dönüştür
    if results:
        return pd.DataFrame(results).set_index("algorithm")
    else:
        return pd.DataFrame()

# Sayfa header'ını göstermek için yardımcı fonksiyon
def display_page_header(tab_name, icon):
    """Sayfa başlığını göster"""
    st.markdown(f'<span class="page-indicator"><span class="page-indicator-icon">{icon}</span> {tab_name}</span>', 
               unsafe_allow_html=True)

# CSS stilleri tek bir yerde toplandı
def load_app_styles():
    """Tüm uygulama stillerini yükle"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Temel değişkenler */
    :root {
        /* Ana Tema Renkleri */
        --primary-dark: #0A1929;
        --primary-medium: #132F4C;
        --primary-light: #173A5E;
        
        /* Algoritma Renkleri (Tutarlılık) */
        --algo-timsort: #3399FF;
        --algo-introsort: #FF4081;
        --algo-radixsort: #00C853;
        --algo-cache-oblivious: #2196F3;
        --algo-adaptive-mergesort: #FF9800;
        --algo-smoothsort: #9c27b0;
        
        /* Vurgu Renkleri */
        --accent1: #3399FF;
        --accent2: #00C853;
        --accent3: #FF4081;
        --neon-text: #66EFFF;
        --purple-accent: #9c27b0;
        --gold-accent: #f6ad37;
        
        /* Metin Renkleri */
        --text-primary: rgba(255, 255, 255, 0.95);
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-disabled: rgba(255, 255, 255, 0.5);
        --text-hint: rgba(255, 255, 255, 0.4);
        
        /* Arka Plan & Kenar Çizgisi */
        --border-subtle: rgba(255, 255, 255, 0.12);
        --card-bg: linear-gradient(145deg, rgba(19, 47, 76, 0.7), rgba(11, 26, 42, 0.9));
        --card-border: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(240,240,255,0.12) 100%);
        --sidebar-bg: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary-medium) 100%);
        --highlight-shadow: 0 0 15px rgba(51, 153, 255, 0.5), 0 0 30px rgba(51, 153, 255, 0.3);
        
        /* Boşluk & Kenarlık Değişkenleri */
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 16px;
        --spacing-lg: 24px;
        --spacing-xl: 32px;
        --spacing-xxl: 48px;
        --border-radius-sm: 8px;
        --border-radius-md: 12px;
        --border-radius-lg: 16px;
        --border-radius-xl: 24px;
        
        /* Animasyon değişkenleri */
        --transition-smooth: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1.2);
    }
    
    /* Ana Stilller ve Yazı Tipi Tanımlamaları */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-primary);
        background-color: var(--primary-dark);
        scroll-behavior: smooth;
    }
    
    /* Streamlit ana konteyner stillerini geçersiz kıl */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium)) !important;
    }
    
    /* Premium Container */
    .premium-container {
        position: relative;
        padding: var(--spacing-xl);
        background: var(--primary-dark);
        margin-bottom: var(--spacing-xl);
        border-radius: var(--border-radius-lg);
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Animasyonlu gradient arka plan */
    .premium-container:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent3), var(--accent1));
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        z-index: 1;
    }
    
    /* Premium Başlık - Boyutları standartlaştırıldı */
    .premium-header {
        position: relative;
        display: inline-block;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: var(--spacing-xl);
        text-align: left;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, var(--accent1), var(--neon-text));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        padding-bottom: var(--spacing-sm);
        position: relative;
        line-height: 1.1;
        transform-style: preserve-3d;
        transition: var(--transition-smooth);
    }
    
    /* Tutarlı Alt Başlık */
    .premium-subheader {
        font-size: 1.75rem;
        font-weight: 700;
        margin: var(--spacing-lg) 0;
        color: var(--text-primary);
        padding-left: var(--spacing-md);
        border-left: 4px solid var(--accent1);
        line-height: 1.2;
    }
    
    .premium-subheader-sm {
        font-size: 1.3rem;
        font-weight: 600;
        margin: var(--spacing-md) 0;
        color: var(--text-primary);
        padding-left: var(--spacing-sm);
        border-left: 3px solid var(--accent1);
        line-height: 1.2;
    }
    
    /* Yapışkan Üst Navigasyon */
    .sticky-tabs-container {
        position: sticky;
        top: 0;
        z-index: 100;
        background: linear-gradient(to bottom, var(--primary-dark), rgba(10, 25, 41, 0.9));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: var(--spacing-md) var(--spacing-lg);
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: var(--spacing-xl);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .sticky-tabs {
        display: flex;
        justify-content: center;
        gap: var(--spacing-md);
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .sticky-tab {
        padding: var(--spacing-md) var(--spacing-lg);
        color: var(--text-secondary);
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: var(--transition-smooth);
        background: transparent;
        border: 1px solid transparent;
        text-align: center;
    }
    
    .sticky-tab:hover {
        color: var(--text-primary);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .sticky-tab.active {
        color: white;
        background: linear-gradient(90deg, var(--accent1), rgba(51, 153, 255, 0.7));
        box-shadow: 0 4px 15px rgba(51, 153, 255, 0.3);
    }
    
    /* Sidebar Grupları - Ayrılmış kategoriler */
    .sidebar .sidebar-content {
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border-subtle);
    }
    
    /* Sidebar Kategori Grubu */
    .sidebar-group {
        margin: var(--spacing-lg) 0;
        padding: var(--spacing-md);
        background: rgba(255, 255, 255, 0.03);
        border-radius: var(--border-radius-md);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar Başlık */
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--accent1);
        margin-bottom: var(--spacing-lg);
        padding-bottom: var(--spacing-md);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar Bölüm Başlığı */
    .sidebar-section {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: var(--spacing-lg) 0 var(--spacing-md);
    }
    
    /* Streamlit Button Override */
    .stButton button {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
        color: white !important;
        border: none !important;
        padding: var(--spacing-md) var(--spacing-lg) !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(51, 153, 255, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 7px 20px rgba(51, 153, 255, 0.5) !important;
    }
    
    /* Bilgi Kutusu */
    .info-box {
        padding: var(--spacing-md);
        background: rgba(255, 255, 255, 0.03);
        border-radius: var(--border-radius-md);
        border-left: 3px solid var(--accent1);
        margin: var(--spacing-md) 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .info-box-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--spacing-xs);
        display: flex;
        align-items: center;
    }
    
    .info-box-icon {
        margin-right: var(--spacing-xs);
        color: var(--accent1);
        font-size: 1.1rem;
    }
    
    /* Slider etiketi */
    .slider-label {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 5px;
    }
    
    .slider-label-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .slider-value {
        font-size: 0.85rem;
        color: var(--accent1);
        font-weight: 500;
        padding: 2px 8px;
        background: rgba(51, 153, 255, 0.1);
        border-radius: 30px;
    }
    
    /* Tema Değiştirici */
    .theme-switcher {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 200;
        background: rgba(19, 47, 76, 0.7);
        border-radius: 30px;
        padding: 5px;
        display: flex;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .theme-button {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin: 0 5px;
        cursor: pointer;
        transition: var(--transition-smooth);
        border: 2px solid transparent;
    }
    
    .theme-button:hover {
        transform: scale(1.2);
    }
    
    .theme-button.active {
        border-color: white;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .theme-dark {
        background: linear-gradient(135deg, #0A1929, #132F4C);
    }
    
    .theme-light {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    }
    
    .theme-blue {
        background: linear-gradient(135deg, #0D47A1, #1976D2);
    }
    
    .theme-purple {
        background: linear-gradient(135deg, #4A148C, #7B1FA2);
    }
    
    /* Sayfa göstergeleri */
    .page-indicator {
        display: inline-block;
        padding: 8px 15px;
        background: rgba(51, 153, 255, 0.1);
        border-radius: 30px;
        font-size: 0.9rem;
        color: var(--accent1);
        margin-bottom: var(--spacing-md);
        border: 1px solid rgba(51, 153, 255, 0.2);
    }
    
    .page-indicator-icon {
        margin-right: var(--spacing-xs);
    }
    
    /* Footer stil */
    .premium-footer {
        position: relative;
        width: 100%;
        padding: var(--spacing-md) 0;
        text-align: center;
        background: linear-gradient(180deg, rgba(10, 25, 41, 0), var(--primary-dark));
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: var(--spacing-xl);
    }
    
    /* Premium çizgi ayırıcı */
    .premium-line {
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.1), rgba(255,255,255,0));
        margin: var(--spacing-lg) 0;
    }
    
    /* Premium kart stilleri */
    .premium-card {
        background: var(--card-bg);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-lg);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .premium-card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--spacing-md);
        padding-bottom: var(--spacing-sm);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Metrik kartları */
    .dashboard-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: var(--spacing-md);
        margin: var(--spacing-lg) 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(19, 47, 76, 0.4), rgba(10, 25, 41, 0.8));
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-lg);
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
        transition: var(--transition-smooth);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card.speed {
        border-left: 3px solid var(--accent1);
    }
    
    .metric-card.memory {
        border-left: 3px solid var(--accent2);
    }
    
    .metric-card.comparison {
        border-left: 3px solid var(--accent3);
    }
    
    .metric-card.count {
        border-left: 3px solid var(--purple-accent);
    }
    
    .animated-icon {
        font-size: 2rem;
        margin-bottom: var(--spacing-sm);
        animation: pulse 2s infinite;
    }
    
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: var(--spacing-sm);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: var(--spacing-sm);
    }
    
    .metric-sublabel {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    /* Star rating system */
    .star-rating {
        display: flex;
        justify-content: center;
        margin: var(--spacing-xs) 0;
    }
    
    .star {
        color: var(--gold-accent);
        font-size: 1.2rem;
        margin: 0 var(--spacing-xs);
    }
    
    /* Animasyon Kartları */
    .animation-card {
        background: linear-gradient(145deg, rgba(19, 47, 76, 0.6), rgba(10, 25, 41, 0.9));
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .animation-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Algoritma Renk Kodlaması - Kart Üst Kenar Renkleri */
    .animation-card.timsort::before,
    .animation-card.introsort::before,
    .animation-card.radixsort::before,
    .animation-card.cache-oblivious::before,
    .animation-card.adaptive-mergesort::before,
    .animation-card.smoothsort::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        z-index: 1;
    }
    
    .animation-card.timsort::before {
        background: var(--algo-timsort);
    }
    
    .animation-card.introsort::before {
        background: var(--algo-introsort);
    }
    
    .animation-card.radixsort::before {
        background: var(--algo-radixsort);
    }
    
    .animation-card.cache-oblivious::before {
        background: var(--algo-cache-oblivious);
    }
    
    .animation-card.adaptive-mergesort::before {
        background: var(--algo-adaptive-mergesort);
    }
    
    .animation-card.smoothsort::before {
        background: var(--algo-smoothsort);
    }
    
    /* Kart Başlığı */
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .algo-icon {
        margin-right: 10px;
        font-size: 20px;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: white;
        margin: 0;
    }
    
    /* İstatistik Kutuları */
    .stats-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px 15px;
        text-align: center;
        flex: 1;
        min-width: 120px;
    }
    
    .stat-value {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
    }
    
    /* Performans Rozetleri */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 15px;
    }
    
    /* Animasyon Kontrolörleri */
    .animation-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
        padding: 10px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
    }
    
    .control-button {
        background: rgba(51, 153, 255, 0.2);
        border: 1px solid rgba(51, 153, 255, 0.3);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .control-button:hover {
        background: rgba(51, 153, 255, 0.4);
        transform: scale(1.1);
    }
    
    /* Renk Efsanesi */
    .legend-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin: 20px 0;
        gap: 15px;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
    }
    
    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .legend-text {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Karşılaştırma Görünümü */
    .comparison-container {
        background: linear-gradient(145deg, rgba(19, 47, 76, 0.5), rgba(10, 25, 41, 0.8));
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    }
    
    .comparison-title {
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
        color: white;
    }
    
    /* Grafik açıklaması */
    .chart-description {
        font-size: 0.85rem;
        color: var(--text-secondary);
        padding: var(--spacing-sm);
        background: rgba(0, 0, 0, 0.2);
        border-radius: var(--border-radius-sm);
        margin-top: var(--spacing-xs);
    }
    
    /* Tab Butonları Stilleri */
    div.stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        background-color: transparent !important;
        padding: 0 !important;
        margin-bottom: var(--spacing-md) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }
    
    div.stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 0 !important;
        padding: var(--spacing-md) var(--spacing-lg) !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        margin-right: 0 !important;
        position: relative !important;
        overflow: hidden !important;
        transition: var(--transition-smooth) !important;
    }
    
    div.stTabs [data-baseweb="tab"]::after {
        content: "" !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 50% !important;
        width: 0 !important;
        height: 3px !important;
        background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
        transition: var(--transition-smooth) !important;
        transform: translateX(-50%) !important;
        border-radius: 3px 3px 0 0 !important;
    }
    
    div.stTabs [data-baseweb="tab"]:hover::after {
        width: 30% !important;
    }
    
    div.stTabs [aria-selected="true"] {
        color: var(--accent1) !important;
        background-color: transparent !important;
    }
    
    div.stTabs [aria-selected="true"]::after {
        width: 100% !important;
    }
    
    div.stTabs [data-baseweb="tab-panel"] {
        background-color: transparent !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* Mobil Responsive */
    @media screen and (max-width: 992px) {
        .premium-header {
            font-size: 2rem;
        }
        
        .premium-subheader {
            font-size: 1.5rem;
        }
        
        .sticky-tabs {
            flex-wrap: wrap;
        }
        
        .sticky-tab {
            padding: var(--spacing-sm) var(--spacing-md);
            font-size: 0.85rem;
        }
    }
    
    @media screen and (max-width: 768px) {
        .premium-container {
            padding: var(--spacing-lg);
        }
        
        .premium-header {
            font-size: 1.75rem;
        }
        
        .premium-subheader {
            font-size: 1.3rem;
        }
    }
    
    @media screen and (max-width: 576px) {
        .premium-container {
            padding: var(--spacing-md);
        }
        
        .premium-header {
            font-size: 1.5rem;
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Sayfa yapılandırması
st.set_page_config(
    page_title="Algoritma Karşılaştırma",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state'i başlat
initialize_session_state()

# CSS stili yükle
load_app_styles()

# Tema Değiştirici
st.markdown("""
<div class="theme-switcher">
    <div class="theme-button theme-dark active" onclick="switchTheme('dark')"></div>
    <div class="theme-button theme-light" onclick="switchTheme('light')"></div>
    <div class="theme-button theme-blue" onclick="switchTheme('blue')"></div>
    <div class="theme-button theme-purple" onclick="switchTheme('purple')"></div>
</div>

<script>
function switchTheme(theme) {
    // Bu JavaScript fonksiyonu şimdilik sadece görsel olarak aktif butonu değiştirir
    document.querySelectorAll('.theme-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector('.theme-button.theme-' + theme).classList.add('active');
}
</script>
""", unsafe_allow_html=True)

# Özel başlık ve intro bölümü
st.markdown("""
<div class="premium-container">
    <h1 class="premium-header">Gelişmiş Sıralama Algoritmaları Karşılaştırması</h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 800px; margin-bottom: 25px; line-height: 1.7;">
        Bu interaktif dashboard, modern sıralama algoritmalarının performansını farklı veri türleri üzerinde analiz etmenizi sağlar. 
        Animasyonlar ve detaylı grafiklerle algoritmaların çalışma prensiplerini keşfedin.
    </p>
""", unsafe_allow_html=True)

# Dinamik renk efsanesi oluştur
legend_html = create_color_legend(ALGORITHM_INFO)
st.markdown(legend_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Sidebar tasarımı - Gruplara ayrılmış
with st.sidebar:
    st.markdown('<div class="sidebar-header">Parametreler</div>', unsafe_allow_html=True)
    
    # Veri tipi seçimi - Gruplandırılmış
    st.markdown('<div class="sidebar-group">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Veri Tipi</div>', unsafe_allow_html=True)
    data_type = st.selectbox(
        "Veri tipi seçin:",
        list(VERI_TURLERI.keys()),
        format_func=lambda x: VERI_TURLERI[x]["desc"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Veri boyutu seçimi - Gruplandırılmış
    st.markdown('<div class="sidebar-group">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Veri Boyutu</div>', unsafe_allow_html=True)
    data_size = st.slider("Veri boyutu:", 10, 1000, 100, 10)
    
    # Slider değeri gösterimi
    st.markdown(f"""
    <div class="slider-label">
        <span class="slider-label-text">Eleman sayısı</span>
        <span class="slider-value">{data_size}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Animasyon hızı - Gruplandırılmış
    st.markdown('<div class="sidebar-group">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Animasyon Ayarları</div>', unsafe_allow_html=True)
    animation_speed = st.slider("Animasyon hızı:", 1, 100, 50, 1)
    
    # Hız değeri gösterimi ve uyarı
    speed_text = "Orta Hız"
    if animation_speed < 30:
        speed_text = "Düşük Hız"
    elif animation_speed > 70:
        speed_text = "Yüksek Hız"
        
    st.markdown(f"""
    <div class="slider-label">
        <span class="slider-label-text">{speed_text}</span>
        <span class="slider-value">{animation_speed} fps</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Yüksek FPS uyarısı
    if animation_speed > 70:
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">
                <span class="info-box-icon">⚠️</span> Yüksek Hız Uyarısı
            </div>
            <p>Yüksek animasyon hızı bazı sistemlerde performans sorunlarına yol açabilir.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Algoritma seçimi - Gruplandırılmış
    st.markdown('<div class="sidebar-group">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Algoritmalar</div>', unsafe_allow_html=True)
    algorithms = {}
    for algo_name in ALGORITHM_INFO:
        algorithms[algo_name] = st.checkbox(
            f"{ALGORITHM_INFO[algo_name]['ikon']} {algo_name}", 
            value=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analiz butonu - Modernize edilmiş buton
    st.markdown("<br>", unsafe_allow_html=True)
    run_analysis = st.button("▶️ ANALİZİ BAŞLAT", help="Seçilen algoritmalarla analizi başlatır")
    
    # Ek bilgi kutusu
    st.markdown("""
    <div class="info-box">
        <div class="info-box-title">
            <span class="info-box-icon">ℹ️</span> Veri Türleri Hakkında
        </div>
        <p>Farklı veri türleri, algoritmaları çeşitli senaryolarda test etmenizi sağlar. Kısmen sıralı veri özellikle adaptif algoritmalar için idealdir.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # GitHub linki - Modernize edilmiş
    st.markdown("""
    <div style="margin-top: 30px; text-align: center;">
        <span style="display: inline-block; padding: 10px 15px; background: linear-gradient(135deg, rgba(51, 153, 255, 0.1), rgba(0, 200, 83, 0.1)); border-radius: 10px; border: 1px solid rgba(51, 153, 255, 0.2);">
            <span style="margin-right: 8px; font-size: 1.2rem;">🔮</span>
            <a href="https://github.com/yourusername/algoritma_karsilastirma" style="color: #3399FF; text-decoration: none; font-weight: 500;">GitHub Repository</a>
        </span>
    </div>
    """, unsafe_allow_html=True)

# Veriyi bir kere oluştur ve tüm sekmelerde kullan
if run_analysis or st.session_state.data is None:
    st.session_state.data = generate_data_by_type(data_type, data_size)
    
    # Seçilen algoritmaları al
    selected_algos = [algo for algo, selected in algorithms.items() if selected]
    
    # Performans analizi yap ve sakla
    if selected_algos:
        st.session_state.performance_results = run_performance_analysis(
            st.session_state.data, 
            selected_algos
        )

# Sekmeler oluştur
tab1, tab2, tab3, tab4 = st.tabs(["📈 Animasyonlar", "🔍 Performans", "📚 Algoritma Detayları", "📊 Veri Analizi"])

# Animasyonlar sekmesi içeriği
with tab1:
    # Sayfa göstergesi ekleniyor
    display_page_header("Animasyonlar", "📈")
    
    # Seçilen algoritmaları al
    selected_algos = [algo for algo, selected in algorithms.items() if selected]
    
    if run_analysis or st.session_state.data is not None:
        if selected_algos:
            # Animasyonları göster
            show_animations_tab(
                selected_algos=selected_algos,
                data=st.session_state.data,
                data_type=VERI_TURLERI[data_type]["desc"],
                data_size=data_size,
                animation_speed=animation_speed,
                algorithm_info=ALGORITHM_INFO
            )
        else:
            st.warning("Lütfen en az bir algoritma seçin!")
    else:
        # Boş durumu göster
        show_empty_animation_state()

# Performans karşılaştırma sekmesi içeriği
with tab2:
    # Sayfa göstergesi ekleniyor
    display_page_header("Performans Karşılaştırması", "🔍")
    
    if run_analysis or not st.session_state.performance_results.empty:
        # Performans karşılaştırmasını göster
        show_algorithm_performance_comparison(
            selected_algos=[algo for algo, selected in algorithms.items() if selected],
            results_df=st.session_state.performance_results
        )
    else:
        st.info("Algoritmaların performans karşılaştırmasını görmek için 'ANALİZİ BAŞLAT' butonuna tıklayın.")

# Algoritma Detayları sekmesi içeriği
with tab3:
    # Sayfa göstergesi ekleniyor
    display_page_header("Algoritma Detayları", "📚")
    
    # Algoritma seçimi ve detay görünümü
    selected_algo = st.selectbox(
        "Detaylarını görmek istediğiniz algoritmayı seçin:", 
        list(ALGORITHM_INFO.keys()),
        key="algorithm_details_select"
    )
    
    # Seçilen algoritmanın detaylarını göster
    display_algorithm_details(selected_algo, ALGORITHM_INFO)

# Veri Analizi sekmesi içeriği
with tab4:
    # Sayfa göstergesi ekleniyor
    display_page_header("Veri Analizi", "📊")
    
    st.markdown("""
    <div class="premium-container">
        <div class="premium-subheader">Veri Üretimi ve İstatistikler</div>
    """, unsafe_allow_html=True)
    
    # Veri üret butonu - İkonlu ve modernize edilmiş buton
    generate_data_btn = st.button("📊 VERİ OLUŞTUR VE İNCELE", help="Farklı veri türleri oluşturur ve analiz eder")
    
    if generate_data_btn:
        # Tüm veri türleri için örnekler oluştur
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<div class='premium-card-title'>📊 Veri Türleri Örnekleri</div>", unsafe_allow_html=True)
        
        # Açıklama kutusu
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">
                <span class="info-box-icon">ℹ️</span> Veri Türleri Hakkında
            </div>
            <p>Her veri türü, algoritmaların farklı durumlardaki performansını test etmek için kullanılır. Sıralanmış, kısmen sıralı veya rastgele veriler, farklı algoritmaların güçlü ve zayıf yanlarını gösterir.</p>
        </div>
        """, unsafe_allow_html=True)
        
        all_data_types = {}
        
        for dtype, info in VERI_TURLERI.items():
            data = info["func"](data_size)
            all_data_types[dtype] = data
            
            st.markdown(f"<h4 style='color: var(--accent1); margin-top: 25px;'>{info['desc']}</h4>", unsafe_allow_html=True)
            
            # Veri gösterimi için iki sütuna böl
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**İlk 10 eleman:**")
                st.json(data[:10])
            
            with col2:
                # Veri dağılımını göster - Tema renklerine uyumlu
                import plotly.express as px
                fig = px.histogram(
                    data, 
                    nbins=20, 
                    title=f"{info['desc']} Dağılımı",
                    labels={'value': 'Değer', 'count': 'Frekans'},
                    color_discrete_sequence=['#3399FF']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E0E0E0'),
                    margin=dict(l=40, r=40, t=50, b=40),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Grafik açıklaması eklendi
                st.markdown(f"""
                <div class="chart-description">
                    <strong>Dağılım:</strong> Bu histogram, {info['desc'].lower()} içindeki değerlerin dağılımını gösterir. 
                    X ekseni değerleri, Y ekseni ise frekansı gösterir.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="premium-line"></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Veri türleri karşılaştırması - Görsel iyileştirmelerle
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<div class='premium-card-title'>📈 Veri Türleri Karşılaştırması</div>", unsafe_allow_html=True)
        
        # Tüm veri türlerini tek grafikte göster
        data_comparison = []
        
        for dtype, info in VERI_TURLERI.items():
            for i, value in enumerate(all_data_types[dtype][:50]):  # İlk 50 elemanı al
                data_comparison.append({
                    "Veri Türü": info['desc'],
                    "Değer": value,
                    "Sıra": i
                })
        
        df_comparison = pd.DataFrame(data_comparison)
        
        fig = px.line(
            df_comparison, 
            x="Sıra", 
            y="Değer", 
            color="Veri Türü",
            title="Farklı Veri Türlerinin Dağılımı (İlk 50 Eleman)",
            labels={"Sıra": "Eleman Sırası", "Değer": "Değer"}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0'),
            margin=dict(l=40, r=40, t=50, b=40),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Grafik açıklaması eklendi
        st.markdown("""
        <div class="chart-description">
            <strong>Karşılaştırma:</strong> Bu grafik, farklı veri türlerinin ilk 50 elemanını karşılaştırır.
            Sıralı veriler düz bir çizgi oluştururken, rastgele veriler dağınık görünür.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer - Görsel olarak iyileştirilmiş
st.markdown("""
<div class="premium-footer">
    <p>Gelişmiş Sıralama Algoritmaları Karşılaştırma Aracı | &copy; 2025 | Hüriye Yıldırım</p>
</div>
""", unsafe_allow_html=True)