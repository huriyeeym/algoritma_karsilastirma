"""
Görselleştirme Modülü

Bu modül, algoritma karşılaştırma sonuçlarını görselleştirmek için fonksiyonlar içerir.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_comparison_chart(results_df, metric_col):
    """
    Algoritma karşılaştırma grafiği oluşturur.
    
    Args:
        results_df (pandas.DataFrame): Karşılaştırma sonuçları
        metric_col (str): Karşılaştırılacak metrik sütunu
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    # Sütun grafiği oluştur
    fig = px.bar(
        results_df.reset_index(),
        x='index',
        y=metric_col,
        color='index',
        labels={'index': 'Algoritma', metric_col: metric_col},
        title=f"Algoritma Karşılaştırması: {metric_col}"
    )
    
    # Görünümü ayarla
    fig.update_layout(
        xaxis_title="Algoritma",
        yaxis_title=metric_col,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def create_comparison_chart_melted(results_df, metric, data_types=None):
    """
    Uzun formatta (melted) algoritma karşılaştırma grafiği oluşturur.
    
    Args:
        results_df (pandas.DataFrame): Karşılaştırma sonuçları
        metric (str): Karşılaştırılacak metrik ('time', 'memory', 'comparisons')
        data_types (list, optional): Dahil edilecek veri türleri
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    # Sütun isimlerini analiz et ve veri tiplerini çıkar
    if data_types is None:
        data_types = set()
        for col in results_df.columns:
            if col.endswith(f"_{metric}"):
                data_type = col.replace(f"_{metric}", "")
                data_types.add(data_type)
    
    # İlgili sütunları seç
    relevant_cols = [f"{dt}_{metric}" for dt in data_types]
    df_subset = results_df[relevant_cols].copy()
    
    # Daha iyi görünen sütun isimleri oluştur
    df_subset.columns = [col.replace(f"_{metric}", "") for col in df_subset.columns]
    
    # Uzun forma dönüştür
    df_melted = df_subset.reset_index().melt(
        id_vars="index", 
        var_name="Veri Türü", 
        value_name=metric
    )
    
    # Sütun grafiği oluştur
    fig = px.bar(
        df_melted,
        x="index",
        y=metric,
        color="Veri Türü",
        barmode="group",
        labels={"index": "Algoritma", metric: metric.capitalize()},
        title=f"Algoritma Karşılaştırması: {metric.capitalize()}"
    )
    
    # Görünümü ayarla
    fig.update_layout(
        xaxis_title="Algoritma",
        yaxis_title=metric.capitalize(),
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title="Veri Türü"
    )
    
    return fig

def create_bar_chart(results_df, metric_cols):
    """
    Çoklu metrik karşılaştırma grafiği oluşturur.
    
    Args:
        results_df (pandas.DataFrame): Karşılaştırma sonuçları
        metric_cols (list): Karşılaştırılacak metrik sütunları
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    fig = go.Figure()
    
    for metric in metric_cols:
        # Her metrik için bir çubuk serisi ekle
        fig.add_trace(
            go.Bar(
                x=results_df.index,
                y=results_df[metric],
                name=metric
            )
        )
    
    # Görünümü ayarla
    fig.update_layout(
        title="Algoritma Performans Karşılaştırması",
        xaxis_title="Algoritma",
        yaxis_title="Değer",
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_line_chart(results_by_size, algorithms, metric_col):
    """
    Veri boyutuna göre performans değişimi grafiği oluşturur.
    
    Args:
        results_by_size (dict): Farklı veri boyutları için sonuçlar
        algorithms (list): Karşılaştırılacak algoritmalar
        metric_col (str): Karşılaştırılacak metrik
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    fig = go.Figure()
    
    sizes = sorted(results_by_size.keys())
    
    for algo in algorithms:
        # Her algoritma için değerler
        values = [results_by_size[size].loc[algo, metric_col] for size in sizes]
        
        # Çizgi ekle
        fig.add_trace(
            go.Scatter(
                x=sizes,
                y=values,
                mode='lines+markers',
                name=algo
            )
        )
    
    # Görünümü ayarla
    fig.update_layout(
        title=f"Veri Boyutuna Göre {metric_col} Değişimi",
        xaxis_title="Veri Boyutu",
        yaxis_title=metric_col,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # X ekseni logaritmik
    fig.update_xaxes(type="log")
    
    return fig

def create_heatmap(algorithms, data_types, metric_results, metric_name):
    """
    Veri tipi ve algoritma bazında performans ısı haritası oluşturur.
    
    Args:
        algorithms (list): Algoritma listesi
        data_types (list): Veri tipi listesi
        metric_results (dict): Ölçüm sonuçları
        metric_name (str): Metrik adı
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    # Isı haritası için veri matrisi oluştur
    z_values = []
    
    for algo in algorithms:
        row = []
        for data_type in data_types:
            key = f"{algo}_{data_type}"
            if key in metric_results:
                row.append(metric_results[key])
            else:
                row.append(0)
        z_values.append(row)
    
    # Isı haritası oluştur
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=data_types,
        y=algorithms,
        colorscale='Viridis'
    ))
    
    # Görünümü ayarla
    fig.update_layout(
        title=f"Algoritma ve Veri Tipi Bazında {metric_name} Isı Haritası",
        xaxis_title="Veri Tipi",
        yaxis_title="Algoritma"
    )
    
    return fig

def create_radar_chart(results_df, metrics, normalize=True):
    """
    Algoritmaların çoklu metrik karşılaştırması için radar grafiği oluşturur.
    
    Args:
        results_df (pandas.DataFrame): Karşılaştırma sonuçları
        metrics (list): Metrik listesi
        normalize (bool): Değerleri normalize et (0-1 aralığına getir)
        
    Returns:
        plotly.graph_objects.Figure: Oluşturulan grafik
    """
    # Veriyi hazırla
    df = results_df.copy()
    
    # Değerleri normalize et (isteğe bağlı)
    if normalize:
        for metric in metrics:
            if metric in df.columns:
                max_val = df[metric].max()
                if max_val > 0:  # Sıfıra bölme hatasını önle
                    df[metric] = df[metric] / max_val
    
    # Radar grafiği oluştur
    fig = go.Figure()
    
    for algo in df.index:
        values = df.loc[algo, metrics].tolist()
        # Kapalı bir şekil için ilk değeri sona da ekle
        values.append(values[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],  # Şekli kapatmak için
            fill='toself',
            name=algo
        ))
    
    # Görünümü ayarla
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1] if normalize else None
            )
        ),
        title="Algoritma Performans Karşılaştırması (Radar Grafiği)",
        showlegend=True
    )
    
    return fig

def create_streamlit_comparison_dashboard(results_df, metrics):
    """
    Streamlit için tüm karşılaştırma grafiklerini içeren bir dashboard oluşturur.
    
    Args:
        results_df (pandas.DataFrame): Karşılaştırma sonuçları
        metrics (list): Metrik listesi
        
    Returns:
        dict: Grafik nesneleri sözlüğü
    """
    charts = {}
    
    # Her metrik için çubuk grafik
    for metric in metrics:
        # Veri tiplerini analiz et
        data_types = set()
        for col in results_df.columns:
            if col.endswith(f"_{metric}"):
                data_type = col.replace(f"_{metric}", "")
                data_types.add(data_type)
        
        # Birden fazla veri tipi varsa melted grafik kullan
        if len(data_types) > 1:
            charts[f"{metric}_bar"] = create_comparison_chart_melted(results_df, metric)
        else:
            # Tek bir veri tipi varsa normal grafik kullan
            metric_col = next(col for col in results_df.columns if col.endswith(f"_{metric}"))
            charts[f"{metric}_bar"] = create_comparison_chart(results_df, metric_col)
    
    # Radar grafiği
    if len(metrics) > 1:
        charts["radar"] = create_radar_chart(results_df, metrics)
    
    # Çoklu metrik karşılaştırma grafiği
    if len(metrics) > 1:
        charts["multiple_metrics"] = create_bar_chart(results_df, metrics)
    
    return charts

if __name__ == "__main__":
    # Test için örnek veri
    data = {
        'TimSort': {'time': 0.0012, 'memory': 2.3, 'comparisons': 1200},
        'IntroSort': {'time': 0.0015, 'memory': 1.8, 'comparisons': 1500},
        'RadixSort': {'time': 0.0010, 'memory': 3.2, 'comparisons': 800},
        'Cache-Oblivious': {'time': 0.0018, 'memory': 1.5, 'comparisons': 1800}
    }
    
    # DataFrame oluştur
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Örnek grafik oluştur ve göster
    fig1 = create_comparison_chart(df, 'time')
    fig2 = create_radar_chart(df, ['time', 'memory', 'comparisons'])
    
    # Grafikleri HTML dosyaları olarak kaydet
    fig1.write_html("results/time_comparison.html")
    fig2.write_html("results/radar_comparison.html")
    
    print("Örnek grafikler oluşturuldu ve kaydedildi.")
    
    # Farklı veri tipleri için test
    multi_data = {
        'TimSort': {'Random_time': 0.0012, 'Sorted_time': 0.0005, 'Random_memory': 2.3, 'Sorted_memory': 2.0},
        'IntroSort': {'Random_time': 0.0015, 'Sorted_time': 0.0008, 'Random_memory': 1.8, 'Sorted_memory': 1.5},
        'RadixSort': {'Random_time': 0.0010, 'Sorted_time': 0.0010, 'Random_memory': 3.2, 'Sorted_memory': 3.0}
    }
    
    # Multi DataFrame oluştur
    multi_df = pd.DataFrame.from_dict(multi_data, orient='index')
    
    # Melted grafik oluştur
    fig3 = create_comparison_chart_melted(multi_df, 'time')
    fig3.write_html("results/melted_comparison.html")