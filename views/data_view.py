"""
Veri Analizi Görünüm Modülü

Bu modül, veri üretimi ve analizini göstermek için fonksiyonlar içerir.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_generator import generate_random_data, generate_nearly_sorted_data
from utils.data_generator import generate_sorted_data, generate_reverse_sorted_data
from . import VERI_TURLERI

def generate_data_by_type(data_type, size):
    """
    Belirtilen türe göre veri oluşturur
    
    Args:
        data_type: Veri türü
        size: Veri boyutu
        
    Returns:
        Oluşturulan veri listesi
    """
    if data_type not in VERI_TURLERI:
        st.error(f"Geçersiz veri türü: {data_type}")
        return None
    
    # Veri türüne göre uygun fonksiyonu çağır
    if data_type == "random":
        return generate_random_data(size)
    elif data_type == "nearly_sorted":
        return generate_nearly_sorted_data(size)
    elif data_type == "sorted":
        return generate_sorted_data(size)
    elif data_type == "reverse_sorted":
        return generate_reverse_sorted_data(size)
    
    # Eğer hiçbir durum eşleşmezse None döndür
    return None

def show_data_analysis(data_size):
    """
    Veri üretimi ve istatistikler sekmesinin içeriğini gösterir
    
    Args:
        data_size: Veri boyutu
    """
    # Sayfa göstergesi (aktif sekme)
    st.markdown('<span class="page-indicator"><span class="page-indicator-icon">📊</span> Veri Analizi</span>', unsafe_allow_html=True)
    
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
            data = generate_data_by_type(dtype, data_size)
            all_data_types[dtype] = data
            
            st.markdown(f"<h4 style='color: var(--accent1); margin-top: 25px;'>{info['desc']}</h4>", unsafe_allow_html=True)
            
            # Veri gösterimi için iki sütuna böl
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**İlk 10 eleman:**")
                st.json(data[:10])
            
            with col2:
                # Veri dağılımını göster - Tema renklerine uyumlu
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