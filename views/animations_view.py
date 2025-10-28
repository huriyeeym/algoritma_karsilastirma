"""
Animasyon Görünümü Modülü

Bu modül, sıralama algoritmaları için Streamlit arayüzündeki animasyon görünümünü yönetir.
Responsive tasarım, performans optimizasyonları ve daha iyi kullanıcı deneyimi sunar.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Any, Optional, Union
import time

# Animasyon yardımcılarını import et
from animation_utils import (
    create_sorting_animation_plotly, 
    create_sorting_animation_comparison,
    create_algorithm_step_visualization,
    get_algorithm_statistics,
    generate_performance_badges,
    create_color_legend,
    ALGORITHM_COLORS
)

# CSS stil tanımlamaları
def load_animation_css():
    """Animasyon görünümü için CSS stillerini yükler"""
    st.markdown("""
    <style>
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
    
    .animation-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        z-index: 1;
    }
    
    /* Algoritma Renk Kodlaması - Kart Üst Kenar Renkleri */
    .animation-card.timsort::before {
        background: #3399FF;
    }
    
    .animation-card.introsort::before {
        background: #FF4081;
    }
    
    .animation-card.radixsort::before {
        background: #00C853;
    }
    
    .animation-card.cache-oblivious::before {
        background: #2196F3;
    }
    
    .animation-card.adaptive-mergesort::before {
        background: #FF9800;
    }
    
    .animation-card.smoothsort::before {
        background: #9c27b0;
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
    
    /* Mobil Uyumluluk */
    @media (max-width: 768px) {
        .animation-card {
            padding: 15px;
        }
        
        .card-title {
            font-size: 16px;
        }
        
        .stat-box {
            min-width: 100px;
            padding: 8px;
        }
        
        .stat-value {
            font-size: 18px;
        }
        
        .legend-container {
            flex-direction: column;
            align-items: flex-start;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_animations_tab(selected_algos: List[str], data: List[int], data_type: str, 
                      data_size: int, animation_speed: int, algorithm_info: Dict[str, Dict]):
    """
    Animasyonlar sekmesinin içeriğini gösterir.
    
    Args:
        selected_algos: Seçilen algoritma adlarının listesi
        data: Sıralanacak veri
        data_type: Veri tipi tanımı
        data_size: Veri boyutu
        animation_speed: Animasyon hızı (1-100)
        algorithm_info: Algoritma bilgilerinin sözlüğü
    """
    # CSS stillerini yükle
    load_animation_css()
    
    # Uyarılar ve optimizasyon ipuçları
    if len(selected_algos) > 4:
        st.warning(f"{len(selected_algos)} algoritma seçtiniz. Performans için ilk 4'ü gösterilecektir.")
        display_algos = selected_algos[:4]
        st.info("Daha fazla algoritma görmek için, sayfayı ikiye bölerek inceleyebilirsiniz.")
    elif len(selected_algos) == 0:
        st.warning("Lütfen en az bir algoritma seçin!")
        return
    else:
        display_algos = selected_algos
    
    # Veri türü bilgisi
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:10px;margin-bottom:20px;text-align:center;">
        <span style="font-weight:600;color:white;">{data_type}</span> türünde 
        <span style="font-weight:600;color:white;">{data_size}</span> elemanlı veri
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive görünüm için dinamik grid
    create_responsive_animation_grid(display_algos, data, data_type, data_size, 
                                   animation_speed, algorithm_info)
    
    # Karşılaştırmalı görünüm (isteğe bağlı)
    if len(display_algos) > 1:
        with st.expander("Karşılaştırmalı Animasyon Görünümü", expanded=False):
            st.markdown("<div class='comparison-title'>Algoritmaları Yan Yana Karşılaştır</div>", 
                       unsafe_allow_html=True)
            
            # Karşılaştırmalı animasyon için algoritma fonksiyonlarını topla
            algo_funcs = {name: algorithm_info[name]["func"] for name in display_algos}
            
            # Karşılaştırmalı animasyon oluştur
            compare_fig = create_sorting_animation_comparison(algo_funcs, data.copy(), animation_speed)
            st.plotly_chart(compare_fig, use_container_width=True)

def create_responsive_animation_grid(algos: List[str], data: List[int], data_type: str, 
                                   data_size: int, animation_speed: int, 
                                   algorithm_info: Dict[str, Dict]):
    """
    Algoritma animasyonları için responsive grid düzeni oluşturur.
    
    Args:
        algos: Gösterilecek algoritma adları
        data: Sıralanacak veri
        data_type: Veri tipi tanımı
        data_size: Veri boyutu
        animation_speed: Animasyon hızı (1-100)
        algorithm_info: Algoritma bilgilerinin sözlüğü
    """
    # Grid yapısını belirle
    cols_per_row = 2 if len(algos) > 1 else 1
    
    # Algoritmaları satır satır yerleştir
    for i in range(0, len(algos), cols_per_row):
        cols = st.columns(min(cols_per_row, len(algos) - i))
        
        for j in range(min(cols_per_row, len(algos) - i)):
            algo_idx = i + j
            if algo_idx < len(algos):
                with cols[j]:
                    show_algorithm_animation_card(
                        algos[algo_idx], 
                        data.copy(), 
                        data_type,
                        data_size,
                        animation_speed,
                        algorithm_info
                    )

def show_algorithm_animation_card(algo_name: str, data: List[int], data_type: str, 
                                data_size: int, animation_speed: int, 
                                algorithm_info: Dict[str, Dict]):
    """
    Tek bir algoritma için animasyon kartı gösterir.
    
    Args:
        algo_name: Algoritma adı
        data: Sıralanacak veri
        data_type: Veri tipi tanımı
        data_size: Veri boyutu
        animation_speed: Animasyon hızı (1-100)
        algorithm_info: Algoritma bilgilerinin sözlüğü
    """
    # Algoritma bilgilerini al
    algo_info = algorithm_info[algo_name]
    algo_func = algo_info["func"]
    
    # CSS sınıfı için algoritma adını biçimlendir
    css_class = algo_name.lower().replace(' ', '-').replace('_', '-')
    
    # Kart başlangıcı
    st.markdown(f"""
    <div class="animation-card {css_class}">
        <div class="card-header">
            <span class="algo-icon">{algo_info["ikon"]}</span>
            <h3 class="card-title">{algo_name}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Animasyon oluştur
    fig, steps = create_sorting_animation_plotly(
        algo_name, 
        data, 
        algo_func(data.copy(), collect_states=True)[1],
        animation_speed
    )
    
    # Grafiği göster
    st.plotly_chart(fig, use_container_width=True)
    
    # İstatistikleri hesapla
    stats = get_algorithm_statistics(algo_func(data.copy(), collect_states=True)[1])
    
    # İstatistikleri göster
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{stats['step_count']}</div>
            <div class="stat-label">Adım Sayısı</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{stats['swap_count']}</div>
            <div class="stat-label">Değişim</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{algo_info["özellik"]}</div>
            <div class="stat-label">Özellik</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Algoritma karmaşıklığı
    st.markdown(f"""
    <div style="margin:15px 0;text-align:center;">
        <span style="background:rgba(51,153,255,0.1);padding:5px 12px;border-radius:20px;
                    font-size:14px;font-weight:600;">
            {algo_info["best_case"]} → {algo_info["worst_case"]}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Performans rozetleri
    badges_html = generate_performance_badges(
        stats, 
        data_size, 
        data_type, 
        ALGORITHM_COLORS.get(algo_name, "#3399FF")
    )
    st.markdown(f'<div class="badge-container">{badges_html}</div>', unsafe_allow_html=True)
    
    # Animasyon kontrolleri (sadece görsel, işlevsellik için Plotly düğmeleri kullanılır)
    st.markdown("""
    <div class="animation-controls">
        <div class="control-button">⏮️</div>
        <div class="control-button" style="background:rgba(51,153,255,0.3);transform:scale(1.2);">▶️</div>
        <div class="control-button">⏹️</div>
        <div class="control-button">⏭️</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Kart sonu
    st.markdown("</div>", unsafe_allow_html=True)

def show_algorithm_performance_comparison(selected_algos: List[str], results_df: pd.DataFrame):
    """
    Algoritmaların performans karşılaştırması görünümünü gösterir.
    
    Args:
        selected_algos: Seçilen algoritma adlarının listesi
        results_df: Performans sonuçlarını içeren DataFrame
    """
    # CSS stillerini yükle
    load_animation_css()
    
    if results_df.empty or len(selected_algos) == 0:
        st.warning("Performans verileri bulunamadı. Lütfen önce analiz çalıştırın.")
        return
    
    # En iyi performansa sahip algoritmaları bul
    best_time_algo = results_df['time'].idxmin() if 'time' in results_df.columns else None
    best_memory_algo = results_df['memory'].idxmin() if 'memory' in results_df.columns else None
    best_comp_algo = results_df['comparisons'].idxmin() if 'comparisons' in results_df.columns else None
    
    # Sonuçları göster
    st.markdown("""
    <div class="comparison-container">
        <div class="comparison-title">Algoritma Performans Özeti</div>
    """, unsafe_allow_html=True)
    
    # Performans rozetleri
    if best_time_algo:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align:center;padding:20px;background:rgba(51,153,255,0.1);border-radius:16px;">
                <div style="font-size:24px;margin-bottom:10px;">⚡</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.7);">EN HIZLI</div>
                <div style="font-size:20px;font-weight:700;margin:10px 0;">{best_time_algo}</div>
                <div style="font-size:16px;color:#3399FF;">{results_df.loc[best_time_algo, 'time']:.6f} saniye</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="text-align:center;padding:20px;background:rgba(76,175,80,0.1);border-radius:16px;">
                <div style="font-size:24px;margin-bottom:10px;">💾</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.7);">EN AZ BELLEK</div>
                <div style="font-size:20px;font-weight:700;margin:10px 0;">{best_memory_algo}</div>
                <div style="font-size:16px;color:#4CAF50;">{results_df.loc[best_memory_algo, 'memory']:.6f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div style="text-align:center;padding:20px;background:rgba(255,64,129,0.1);border-radius:16px;">
                <div style="font-size:24px;margin-bottom:10px;">🔢</div>
                <div style="font-size:14px;color:rgba(255,255,255,0.7);">EN AZ KARŞILAŞTIRMA</div>
                <div style="font-size:20px;font-weight:700;margin:10px 0;">{best_comp_algo}</div>
                <div style="font-size:16px;color:#FF4081;">{results_df.loc[best_comp_algo, 'comparisons']} adet</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Sonuçları tablo olarak göster
    st.dataframe(
        results_df.style.format({
            'time': '{:.6f} sn',
            'memory': '{:.6f} MB',
            'comparisons': '{:,d}',
        }).background_gradient(cmap='viridis', axis=0),
        use_container_width=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_algorithm_details(algo_name: str, algorithm_info: Dict[str, Dict]):
    """
    Seçilen algoritmanın detaylarını görüntüler.
    
    Args:
        algo_name: Algoritma adı
        algorithm_info: Algoritma bilgilerinin sözlüğü
    """
    # CSS stillerini yükle
    load_animation_css()
    
    # Algoritma bilgilerini al
    algo_info = algorithm_info.get(algo_name)
    
    if not algo_info:
        st.warning(f"{algo_name} bilgileri bulunamadı.")
        return
    
    # CSS sınıfı için algoritma adını biçimlendir
    css_class = algo_name.lower().replace(' ', '-').replace('_', '-')
    
    # Algoritma detay kartı
    st.markdown(f"""
    <div class="animation-card {css_class}" style="padding:30px;">
        <div class="card-header" style="margin-bottom:25px;">
            <span class="algo-icon" style="font-size:30px;">{algo_info["ikon"]}</span>
            <h3 class="card-title" style="font-size:24px;">{algo_name}</h3>
        </div>
        
        <p style="color:rgba(255,255,255,0.8);line-height:1.6;margin-bottom:20px;font-size:16px;">
            {algo_info["description"]}
        </p>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:15px;margin:25px 0;">
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">En İyi Durum</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["best_case"]}</div>
            </div>
            
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">Ortalama Durum</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["avg_case"]}</div>
            </div>
            
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">En Kötü Durum</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["worst_case"]}</div>
            </div>
            
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">Kararlılık</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["kararlılık"]}</div>
            </div>
            
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">Özellik</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["özellik"]}</div>
            </div>
            
            <div style="background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;">
                <div style="font-size:14px;color:rgba(255,255,255,0.6);">Geliştirilme Yılı</div>
                <div style="font-size:20px;font-weight:700;margin-top:5px;">{algo_info["yıl"]}</div>
            </div>
        </div>
        
        <div style="background:rgba(51,153,255,0.1);padding:15px;border-radius:12px;margin-top:25px;border-left:3px solid {ALGORITHM_COLORS.get(algo_name, '#3399FF')};">
            <div style="font-weight:600;margin-bottom:8px;">💡 Uygulama Alanları</div>
            <div style="color:rgba(255,255,255,0.8);line-height:1.5;">
                Bu algoritma özellikle {get_algorithm_use_cases(algo_name)} için uygundur.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_algorithm_use_cases(algo_name: str) -> str:
    """
    Algoritmanın uygulama alanlarını döndürür.
    
    Args:
        algo_name: Algoritma adı
        
    Returns:
        str: Uygulama alanları açıklaması
    """
    # Algoritmalara göre uygulama alanları
    use_cases = {
        "TimSort": "kısmen sıralı veriler, Python ve Java uygulamaları, büyük veri setleri",
        "IntroSort": "genel amaçlı sıralama, C++ uygulamaları, en kötü durum garantisi gereken projeler",
        "RadixSort": "tam sayı dizileri, pozitif tam sayılar, karakter dizileri, IP adresleri",
        "Cache-Oblivious": "bellek hiyerarşisi optimizasyonu gereken sistemler, sunucu uygulamaları",
        "Adaptive MergeSort": "kısmen sıralı veriler, dağıtık sistemler, büyük veri yapıları",
        "SmoothSort": "kısmen sıralı veriler, bellek kısıtlı ortamlar, enerji verimli uygulamalar"
    }
    
    return use_cases.get(algo_name, "çeşitli sıralama gereksinimleri")

def show_empty_animation_state():
    """Henüz animasyon oluşturulmadığında gösterilecek mesaj"""
    st.info("Animasyonları görmek için sol menüden algoritma seçin ve 'ANALİZİ BAŞLAT' butonuna tıklayın.")
    
    st.markdown("""
    <div style="text-align:center;padding:40px;background:rgba(0,0,0,0.2);border-radius:16px;margin:30px 0;">
        <div style="font-size:48px;margin-bottom:20px;">📊</div>
        <h3 style="margin-bottom:15px;color:white;">Sıralama Algoritması Animasyonları</h3>
        <p style="color:rgba(255,255,255,0.7);">
            Bu modül sayesinde farklı sıralama algoritmalarının çalışma prensiplerini canlı animasyonlarla görebilirsiniz.
            Başlamak için parametreleri ayarlayın ve analizi başlatın.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_algorithm_animation_tips():
    """Animasyonlar hakkında ipuçları ve öneriler gösterir"""
    with st.expander("Animasyonlarla İlgili İpuçları", expanded=False):
        st.markdown("""
        ### Animasyon İpuçları
        
        * **Hız Ayarı**: Animasyon hızını sol menüdeki kaydırıcı ile ayarlayabilirsiniz.
        * **Adım Adım İzleme**: Her animasyonun altındaki kaydırıcı ile belirli bir adımda durabilirsiniz.
        * **Renk Kodları**: Değişen elemanlar kırmızı ile gösterilir. Bu, her adımda hangi elemanların yer değiştirdiğini gösterir.
        * **Optimize Edilmiş Görünüm**: Büyük veri setleri için animasyonlar otomatik olarak optimize edilir.
        * **Karşılaştırma**: Birden fazla algoritma seçtiğinizde, karşılaştırmalı görünümü kullanabilirsiniz.
        
        #### En İyi Performans İçin
        * 1000'den büyük veri setleri için animasyonlar yavaşlayabilir.
        * Mobil cihazlarda en fazla 2 algoritma gösterimi önerilir.
        * Animasyonu durdurarak belirli adımları daha detaylı inceleyebilirsiniz.
        """)