"""
Performans Karşılaştırma Görünüm Modülü

Bu modül, algoritmaların performansını karşılaştırmak için fonksiyonlar içerir.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from utils.metrics import measure_time, measure_memory, measure_comparisons
from .algorithm_view import ALGORITHM_INFO
from . import VERI_TURLERI

def show_performance_comparison(data, data_type, algorithms):
    """
    Performans karşılaştırma sekmesinin içeriğini gösterir
    
    Args:
        data: Sıralanacak veri
        data_type: Veri türü
        algorithms: Seçilen algoritmaların sözlüğü
    """
    # Sayfa göstergesi (aktif sekme)
    st.markdown('<span class="page-indicator"><span class="page-indicator-icon">🔍</span> Performans Karşılaştırması</span>', unsafe_allow_html=True)
    
    if data is not None:
        st.markdown("""
        <div class="performance-container">
            <div class="premium-subheader">Performans Karşılaştırması</div>
        """, unsafe_allow_html=True)
        
        # Seçilen algoritmaları çalıştır ve performansı ölç
        selected_algos = [algo for algo, selected in algorithms.items() if selected]
        
        if not selected_algos:
            st.warning("Lütfen en az bir algoritma seçin!")
        else:
            # Performans sonuçlarını topla
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
            df_results = pd.DataFrame(results).set_index("algorithm")
            
            # En iyi değerleri bul
            min_time = df_results['time'].min()
            min_memory = df_results['memory'].min()
            min_comp = df_results['comparisons'].min()
            max_time = df_results['time'].max() 
            max_memory = df_results['memory'].max()
            max_comp = df_results['comparisons'].max()
            
            # Özet istatistikler
            st.markdown('<div class="premium-subheader">Performans Özeti</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="dashboard-metrics">', unsafe_allow_html=True)
            
            # En hızlı algoritma - Görsel olarak zenginleştirilmiş
            min_time_algo = df_results['time'].idxmin()
            min_time = df_results.loc[min_time_algo, 'time']
            st.markdown(f"""
            <div class="metric-card speed">
                <div class="animated-icon">⚡</div>
                <div class="metric-label">EN HIZLI ALGORİTMA</div>
                <div class="metric-value">{min_time_algo}</div>
                {create_star_rating(df_results.loc[min_time_algo, 'time'], max_time, 'lower')}
                <div class="metric-sublabel">{min_time:.6f} saniye</div>
            </div>
            """, unsafe_allow_html=True)
            
            # En az bellek kullanan - Görsel olarak zenginleştirilmiş
            min_memory_algo = df_results['memory'].idxmin()
            min_memory = df_results.loc[min_memory_algo, 'memory']
            st.markdown(f"""
            <div class="metric-card memory">
                <div class="animated-icon">💾</div>
                <div class="metric-label">EN AZ BELLEK KULLANAN</div>
                <div class="metric-value">{min_memory_algo}</div>
                {create_star_rating(df_results.loc[min_memory_algo, 'memory'], max_memory, 'lower')}
                <div class="metric-sublabel">{min_memory:.6f} MB</div>
            </div>
            """, unsafe_allow_html=True)
            
            # En az karşılaştırma yapan - Görsel olarak zenginleştirilmiş
            min_comp_algo = df_results['comparisons'].idxmin()
            min_comp = df_results.loc[min_comp_algo, 'comparisons']
            st.markdown(f"""
            <div class="metric-card comparison">
                <div class="animated-icon">🔢</div>
                <div class="metric-label">EN AZ KARŞILAŞTIRMA YAPAN</div>
                <div class="metric-value">{min_comp_algo}</div>
                {create_star_rating(df_results.loc[min_comp_algo, 'comparisons'], max_comp, 'lower')}
                <div class="metric-sublabel">{min_comp} karşılaştırma</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ortalama adım sayısı - Görsel olarak zenginleştirilmiş
            avg_steps = df_results.index.size
            st.markdown(f"""
            <div class="metric-card count">
                <div class="animated-icon">📊</div>
                <div class="metric-label">ÖLÇÜLEN ALGORİTMA SAYISI</div>
                <div class="metric-value">{avg_steps}</div>
                <div class="star-rating">
                    <span class="star">★</span>
                    <span class="star">★</span>
                    <span class="star">★</span>
                    <span class="star">★</span>
                    <span class="star">★</span>
                </div>
                <div class="metric-sublabel">Toplam test edilen</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Performans grafiklerini göster
            st.markdown('<div class="premium-line"></div>', unsafe_allow_html=True)
            st.markdown('<div class="premium-subheader">Detaylı Grafikler</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("<div class='premium-subheader-sm'>⏱️ Çalışma Süresi Karşılaştırması</div>", unsafe_allow_html=True)
                
                # Tutarlı renk kullanımı için renk haritası
                color_map = {}
                for algo in selected_algos:
                    color_map[algo] = ALGORITHM_INFO[algo]["plot_color"]
                
                fig_time = px.bar(
                    df_results.reset_index(),
                    x="algorithm",
                    y="time",
                    color="algorithm",
                    color_discrete_map=color_map,  # Tutarlı renkler
                    labels={"algorithm": "Algoritma", "time": "Süre (saniye)"},
                    title="Çalışma Süresi"
                )
                fig_time.update_layout(
                    xaxis_title="Algoritma", 
                    yaxis_title="Süre (saniye)", 
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E0E0E0'),
                    margin=dict(l=40, r=40, t=50, b=40)
                )
                st.plotly_chart(fig_time, use_container_width=True)
                
                # Grafik açıklaması eklendi
                st.markdown("""
                <div class="chart-description">
                    <strong>Ölçüm Birimi:</strong> Saniye cinsinden çalışma süresi | 
                    <strong>Düşük değerler</strong> daha iyi performansı gösterir.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("<div class='premium-subheader-sm'>💾 Bellek Kullanımı Karşılaştırması</div>", unsafe_allow_html=True)
                fig_memory = px.bar(
                    df_results.reset_index(),
                    x="algorithm",
                    y="memory",
                    color="algorithm",
                    color_discrete_map=color_map,  # Tutarlı renkler
                    labels={"algorithm": "Algoritma", "memory": "Bellek (MB)"},
                    title="Bellek Kullanımı"
                )
                fig_memory.update_layout(
                    xaxis_title="Algoritma", 
                    yaxis_title="Bellek (MB)", 
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E0E0E0'),
                    margin=dict(l=40, r=40, t=50, b=40)
                )
                st.plotly_chart(fig_memory, use_container_width=True)
                
                # Grafik açıklaması eklendi
                st.markdown("""
                <div class="chart-description">
                    <strong>Ölçüm Birimi:</strong> Megabayt (MB) cinsinden bellek kullanımı | 
                    <strong>Düşük değerler</strong> daha verimli bellek kullanımını gösterir.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Karşılaştırma sayısı
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='premium-subheader-sm'>🔢 Karşılaştırma Sayısı</div>", unsafe_allow_html=True)
            fig_comp = px.bar(
                df_results.reset_index(),
                x="algorithm",
                y="comparisons",
                color="algorithm",
                color_discrete_map=color_map,  # Tutarlı renkler
                labels={"algorithm": "Algoritma", "comparisons": "Karşılaştırma Sayısı"},
                title="Karşılaştırma Sayısı"
            )
            fig_comp.update_layout(
                xaxis_title="Algoritma", 
                yaxis_title="Karşılaştırma Sayısı", 
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0E0E0'),
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Grafik açıklaması eklendi
            st.markdown("""
            <div class="chart-description">
                <strong>Not:</strong> RadixSort karşılaştırma yapmadan çalışan bir algoritmadır, bu nedenle karşılaştırma sayısı diğerlerinden farklı olabilir.
                <strong>Düşük değerler</strong> daha az işlem yapıldığını gösterir.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Sonuçları tablo olarak göster
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.markdown("<div class='premium-card-title'>📋 Detaylı Sonuçlar</div>", unsafe_allow_html=True)
            
            # Tabloyu göster
            st.dataframe(df_results.style.format({
                'time': '{:.6f} sn',
                'memory': '{:.6f} MB',
                'comparisons': '{:,d}',  # Binlik ayırıcılı sayı formatı
            }).background_gradient(cmap='viridis', axis=0))
            
            # Tablo açıklaması
            st.markdown("""
            <div class="info-box">
                <div class="info-box-title">
                    <span class="info-box-icon">ℹ️</span> Tablo Hakkında
                </div>
                <p>Tablodaki renkler, her sütun için en iyi (koyu) ve en kötü (açık) değerleri gösterir. Koyu renkli hücreler daha iyi performansı temsil eder.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def measure_algorithm_performance(algo_name, algo_func, data):
    """
    Algoritmanın performansını ölçer
    
    Args:
        algo_name: Algoritma adı
        algo_func: Sıralama algoritması fonksiyonu
        data: Sıralanacak veri
        
    Returns:
        Performans ölçüm sonuçları sözlüğü
    """
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

def create_star_rating(value, max_val, mode='lower'):
    """
    Ters veya düz yıldız derecelendirmesi oluşturur (düşük ya da yüksek değerler iyi)
    
    Args:
        value: Derecelendirilecek değer
        max_val: Maksimum değer
        mode: 'lower' (düşük değerler iyi) veya 'higher' (yüksek değerler iyi)
        
    Returns:
        HTML formatında yıldız derecelendirmesi
    """
    # Normalize edilmiş değer (0-5 arası) - Hesapla
    if mode == 'lower':  # Düşük değerler daha iyi
        normalized = max(0, min(5, 5 * (1 - (value / max_val))))
    else:  # Yüksek değerler daha iyi
        normalized = max(0, min(5, 5 * (value / max_val)))
    
    # Tam yıldız sayısı
    full_stars = int(normalized)
    
    # Yarım yıldız var mı?
    half_star = normalized - full_stars >= 0.5
    
    # Boş yıldız sayısı
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    # HTML oluştur
    stars_html = '<div class="star-rating">'
    
    # Dolu yıldızlar
    for _ in range(full_stars):
        stars_html += '<span class="star">★</span>'
    
    # Yarım yıldız
    if half_star:
        stars_html += '<span class="star">✭</span>'
    
    # Boş yıldızlar
    for _ in range(empty_stars):
        stars_html += '<span class="star" style="opacity: 0.3">★</span>'
    
    stars_html += '</div>'
    
    return stars_html