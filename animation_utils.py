"""
Animasyon Yardımcı Modülü

Bu modül, sıralama algoritmaları için animasyon oluşturmaya yardımcı fonksiyonlar içerir.
Geliştirilmiş animasyon desteği, renkler ve performans optimizasyonları eklenmiştir.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import time
from typing import List, Dict, Tuple, Any, Optional, Union

# Tutarlı renk şeması - Algoritma renklerini burada tanımlayalım (app.py ile uyumlu olması için)
ALGORITHM_COLORS = {
    "TimSort": "#3399FF",
    "IntroSort": "#FF4081",
    "RadixSort": "#00C853",
    "Cache-Oblivious": "#2196F3",
    "Adaptive MergeSort": "#FF9800",
    "SmoothSort": "#9c27b0"
}

# Varsayılan renk seti
DEFAULT_COLORS = px.colors.qualitative.Plotly

def create_sorting_animation_plotly(algo_name: str, data: List[int], states: List[List[int]], 
                                   speed_factor: int = 1) -> Tuple[go.Figure, int]:
    """
    Plotly ile sıralama animasyonu oluşturur.
    
    Args:
        algo_name: Algoritma adı
        data: Başlangıç verileri
        states: Algoritmanın ara durumlarının listesi
        speed_factor: Animasyon hızı çarpanı (1-100 arası değer)
        
    Returns:
        (Figure, steps_count): Animasyon grafiği ve adım sayısı
    """
    # Optimizasyon: Çok büyük veri setleri için durumları örnekle
    states = sample_states(states)
    
    # Temel grafik ve ilgili bileşenleri oluştur
    fig = go.Figure()
    frames = []
    
    # Algoritma için özel rengi kullan veya varsayılana dön
    base_color = ALGORITHM_COLORS.get(algo_name, DEFAULT_COLORS[0])
    highlight_color = DEFAULT_COLORS[1]  # Değişen elemanlar için vurgu rengi
    
    # Her durum için bir frame ekle
    for i, state in enumerate(states):
        # Renklendirme için dizinin önceki durumuyla karşılaştır
        colors = []
        
        if i > 0:
            prev_state = states[i-1]
            for j, val in enumerate(state):
                if j < len(prev_state) and val != prev_state[j]:
                    # Değişen elemanlar için farklı renk
                    colors.append(highlight_color)
                else:
                    colors.append(base_color)
        else:
            colors = [base_color] * len(state)  # İlk durum için hepsi temel renk
        
        # Frame oluştur
        frame = go.Frame(
            data=[go.Bar(
                x=list(range(len(state))),
                y=state,
                marker_color=colors,
                marker_line_color='rgba(0,0,0,0.3)',
                marker_line_width=1,
                name=f'Adım {i}'
            )],
            name=f'Adım {i}'
        )
        frames.append(frame)
    
    # İlk durumu grafik olarak ekle
    fig.add_trace(go.Bar(
        x=list(range(len(states[0]))),
        y=states[0],
        marker_color=base_color,
        marker_line_color='rgba(0,0,0,0.3)',
        marker_line_width=1,
        name='Başlangıç'
    ))
    
    # Frame'leri ekle
    fig.frames = frames
    
    # Animasyon kontrollerini ayarla
    animation_duration = calculate_animation_duration(speed_factor)
    
    # Slider ve kontrol butonlarını oluştur
    sliders, updatemenus = create_animation_controls(frames, animation_duration)
    
    # Grafik görünümünü güncelleştir
    fig.update_layout(
        title=dict(
            text=f'{algo_name} Algoritması',
            font=dict(size=18, color='white'),
            x=0.5,  # Başlığı ortala
            xanchor='center'
        ),
        autosize=True,
        height=400,
        updatemenus=updatemenus,
        sliders=sliders,
        xaxis=dict(
            title="Dizi İndeksi",
            gridcolor='rgba(255,255,255,0.1)',
            title_font=dict(color='rgba(255,255,255,0.7)'),
            tickfont=dict(color='rgba(255,255,255,0.7)')
        ),
        yaxis=dict(
            title="Değer",
            gridcolor='rgba(255,255,255,0.1)',
            title_font=dict(color='rgba(255,255,255,0.7)'),
            tickfont=dict(color='rgba(255,255,255,0.7)')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=13, color='white'),
        margin=dict(l=50, r=30, t=80, b=50),
    )
    
    return fig, len(states)

def create_animation_controls(frames: List[go.Frame], animation_duration: int) -> Tuple[List[Dict], List[Dict]]:
    """
    Animasyon kontrollerini (slider ve butonlar) oluşturur.
    
    Args:
        frames: Animasyon kareleri
        animation_duration: Kare başına milisaniye cinsinden süre
        
    Returns:
        (sliders, updatemenus): Slider ve kontrol menüleri
    """
    # Çubukları animasyon kaydırıcıyla kontrol etmek için yardımcı fonksiyon
    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }
    
    # Slider oluştur
    sliders = [{
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [[f.name], frame_args(animation_duration)],
                "label": str(k),
                "method": "animate",
            }
            for k, f in enumerate(frames)
        ],
    }]
    
    # Oynat/Durdur butonları oluştur
    updatemenus = [{
        "buttons": [
            {
                "args": [None, frame_args(animation_duration)],
                "label": "▶️ Oynat",
                "method": "animate",
            },
            {
                "args": [[None], frame_args(0)],
                "label": "⏸️ Durdur",
                "method": "animate",
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 70},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "y": 0,
        "bgcolor": "rgba(51, 153, 255, 0.1)",
        "bordercolor": "rgba(51, 153, 255, 0.3)",
        "font": {"color": "white"}
    }]
    
    return sliders, updatemenus

def calculate_animation_duration(speed_factor: int) -> int:
    """
    Hız faktörüne göre animasyon süresini hesaplar.
    
    Args:
        speed_factor: 1-100 arası hız değeri (100 = en hızlı)
        
    Returns:
        int: Milisaniye cinsinden animasyon süresi (düşük = daha hızlı)
    """
    # Hız faktörünü sınırla (1-100 arası)
    speed_factor = max(1, min(100, speed_factor))
    
    # Animasyon süresini hesapla (tersi orantılı: düşük süre = yüksek hız)
    # 1-100 aralığındaki hız değerini 500-50 aralığındaki süreye dönüştür
    return 500 - ((speed_factor - 1) * 450 // 99)

def sample_states(states: List[List[int]], max_states: int = 100) -> List[List[int]]:
    """
    Çok uzun durum listelerini daha yönetilebilir bir boyuta örnekler.
    Bu, animasyon performansını iyileştirir.
    
    Args:
        states: Tüm algoritmik durumlar listesi
        max_states: Maksimum durum sayısı (varsayılan: 100)
        
    Returns:
        List[List[int]]: Örneklenmiş durumlar
    """
    if len(states) <= max_states:
        return states
    
    # İlk ve son durumu her zaman dahil et, aradakileri örnekle
    if len(states) > max_states:
        step = len(states) // max_states
        
        # İlk ve son durumu ve önemli ara durumları seç
        sampled = [states[0]]  # Her zaman ilk durumu al
        
        # Ara durumlar için örnekleme yap
        indices = list(range(1, len(states) - 1, step))
        sampled.extend([states[i] for i in indices])
        
        if indices and indices[-1] < len(states) - 1:
            sampled.append(states[-1])  # Son durumu ekle
        
        return sampled
    
    return states

def create_sorting_animation_comparison(algorithms: Dict[str, callable], data: List[int], 
                                      speed_factor: int = 1) -> go.Figure:
    """
    Birden fazla algoritmanın yan yana animasyonunu oluşturur.
    
    Args:
        algorithms: Algoritma adı ve fonksiyon çiftleri
        data: Sıralanacak veri
        speed_factor: Animasyon hızı çarpanı
        
    Returns:
        plotly.graph_objects.Figure: Karşılaştırmalı animasyon grafiği
    """
    # Her algoritma için durumları topla
    all_states = {}
    max_steps = 0
    
    for algo_name, algo_func in algorithms.items():
        sorted_data, states = algo_func(data.copy(), collect_states=True)
        
        # Optimizasyon: Çok uzun durumları örnekle
        states = sample_states(states)
        
        all_states[algo_name] = states
        max_steps = max(max_steps, len(states))
    
    # Alt grafikleri oluştur
    fig = make_subplots(
        rows=len(algorithms), 
        cols=1,
        subplot_titles=[f"{algo_name}" for algo_name in algorithms.keys()],
        vertical_spacing=0.1
    )
    
    # Her algoritma için başlangıç grafikleri
    for i, (algo_name, states) in enumerate(all_states.items()):
        # Algoritma için özel rengi kullan veya varsayılana dön
        color = ALGORITHM_COLORS.get(algo_name, DEFAULT_COLORS[i % len(DEFAULT_COLORS)])
        
        fig.add_trace(
            go.Bar(
                x=list(range(len(states[0]))),
                y=states[0],
                marker_color=color,
                marker_line_color='rgba(255,255,255,0.3)',
                marker_line_width=1,
                name=algo_name
            ),
            row=i+1, col=1
        )
    
    # Frame'leri oluştur
    frames = []
    
    for step in range(max_steps):
        frame_data = []
        
        for i, (algo_name, states) in enumerate(all_states.items()):
            # Eğer algoritma bu adımda bittiyse, son durumu kullan
            current_step = min(step, len(states) - 1)
            
            # Algoritma için özel rengi kullan
            color = ALGORITHM_COLORS.get(algo_name, DEFAULT_COLORS[i % len(DEFAULT_COLORS)])
            
            frame_data.append(
                go.Bar(
                    x=list(range(len(states[current_step]))),
                    y=states[current_step],
                    marker_color=color,
                    marker_line_color='rgba(255,255,255,0.3)',
                    marker_line_width=1,
                    name=algo_name
                )
            )
        
        frames.append(go.Frame(data=frame_data, name=f'Adım {step}'))
    
    fig.frames = frames
    
    # Animasyon hızını ayarla
    animation_duration = calculate_animation_duration(speed_factor)
    
    # Oynat/Durdur butonları ekle
    fig.update_layout(
        title=dict(
            text='Algoritma Karşılaştırması',
            font=dict(size=20, color='white'),
            x=0.5
        ),
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": animation_duration, "redraw": True}, "fromcurrent": True}],
                    "label": "▶️ Oynat",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    "label": "⏸️ Durdur",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 10},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "y": 0,
            "bgcolor": "rgba(51, 153, 255, 0.1)",
            "bordercolor": "rgba(51, 153, 255, 0.3)",
            "font": {"color": "white"}
        }],
        sliders=[{
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], {"frame": {"duration": animation_duration, "redraw": True}, "mode": "immediate"}],
                    "label": str(k),
                    "method": "animate"
                }
                for k, f in enumerate(frames)
            ]
        }],
        height=250 * len(algorithms),
        margin=dict(l=50, r=50, t=100, b=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Y ekseni başlıklarını ayarla
    for i in range(len(algorithms)):
        fig.update_yaxes(
            title_text="Değer", 
            row=i+1, 
            col=1, 
            gridcolor='rgba(255,255,255,0.1)',
            title_font=dict(color='rgba(255,255,255,0.7)'),
            tickfont=dict(color='rgba(255,255,255,0.7)')
        )
        fig.update_xaxes(
            title_text="Dizi İndeksi", 
            row=i+1, 
            col=1, 
            gridcolor='rgba(255,255,255,0.1)',
            title_font=dict(color='rgba(255,255,255,0.7)'),
            tickfont=dict(color='rgba(255,255,255,0.7)')
        )
    
    return fig

def create_algorithm_step_visualization(states: List[List[int]], step_idx: int, 
                                      title: str) -> go.Figure:
    """
    Algoritmanın belirli bir adımını görselleştirir.
    
    Args:
        states: Algoritmanın ara durumlarının listesi
        step_idx: Görselleştirilecek adım indeksi
        title: Grafik başlığı
        
    Returns:
        plotly.graph_objects.Figure: Statik grafik
    """
    if step_idx >= len(states):
        step_idx = len(states) - 1
    
    state = states[step_idx]
    
    fig = px.bar(
        x=list(range(len(state))),
        y=state,
        title=f"{title} - Adım {step_idx}",
        labels={'x': 'Dizi İndeksi', 'y': 'Değer'},
        color_discrete_sequence=[ALGORITHM_COLORS.get("TimSort", DEFAULT_COLORS[0])]
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=14, color='white'),
        margin=dict(l=60, r=40, t=80, b=60),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig

def get_algorithm_statistics(states: List[List[int]]) -> Dict[str, Any]:
    """
    Algoritmanın istatistiklerini hesaplar.
    
    Args:
        states: Algoritmanın ara durumlarının listesi
        
    Returns:
        dict: İstatistikler (adım sayısı, yer değiştirme sayısı, doğru sıralanmış mı)
    """
    # Adım sayısı
    step_count = len(states)
    
    # Yer değiştirme sayısı
    swap_count = 0
    
    # Karşılaştırma sayısı (tahmini)
    comparison_count = 0
    
    # Ara durumlar arasındaki değişimleri say
    for i in range(1, len(states)):
        prev_state = states[i-1]
        curr_state = states[i]
        
        # İki durum arasında değişen eleman sayısını say
        changes_in_step = 0
        for j in range(min(len(prev_state), len(curr_state))):
            if prev_state[j] != curr_state[j]:
                changes_in_step += 1
        
        swap_count += changes_in_step
        
        # Tahmini karşılaştırma sayısı (her adımda en az bir karşılaştırma yapılır)
        # Bu yaklaşık bir tahmindir ve gerçek algoritmaya göre değişebilir
        comparison_count += max(1, changes_in_step * 2)
    
    # İlk ve son durumu kontrol et
    initial_state = states[0]
    final_state = states[-1]
    sorted_correctly = sorted(initial_state) == final_state
    
    # Sıralama süresi analizi (varsayılan değerler, gerçek süre ölçümü için kullanılmaz)
    time_complexity = "O(n log n)"  # varsayılan
    if step_count < len(states[0]):
        time_complexity = "O(n)" # Çok hızlı sıralama
    elif step_count > len(states[0]) * len(states[0]):
        time_complexity = "O(n²)" # Yavaş sıralama
    
    return {
        "step_count": step_count,
        "swap_count": swap_count,
        "comparison_count": comparison_count,
        "sorted_correctly": sorted_correctly,
        "time_complexity": time_complexity
    }

def generate_performance_badges(stats: Dict[str, Any], data_size: int, 
                              data_type: str, color: str = "#3399FF") -> str:
    """
    Algoritma performans istatistikleri için HTML rozetleri oluşturur.
    
    Args:
        stats: get_algorithm_statistics'ten alınan istatistikler
        data_size: Veri boyutu
        data_type: Veri tipi açıklaması
        color: Rozet rengi (hex)
        
    Returns:
        str: HTML rozet kodu
    """
    badges = []
    
    # Adım sayısı rozeti
    badges.append(
        f"""
    <div style="display:inline-flex;align-items:center;background:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.1);
               padding:6px 10px;border-radius:16px;margin-right:8px;margin-bottom:8px;">
        <span style="margin-right:6px;font-size:14px;">👣</span>
        <div style="display:flex;flex-direction:column;">
            <span style="font-size:14px;font-weight:600;color:white;">{stats['step_count']} adım</span>
            <span style="font-size:10px;color:rgba(255,255,255,0.7);">Toplam işlem</span>
        </div>
    </div>
    """)
    
    # Karşılaştırma sayısı rozeti
    badges.append(f"""
    <div style="display:inline-flex;align-items:center;background:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.1);
               padding:6px 10px;border-radius:16px;margin-right:8px;margin-bottom:8px;">
        <span style="margin-right:6px;font-size:14px;">🔄</span>
        <div style="display:flex;flex-direction:column;">
            <span style="font-size:14px;font-weight:600;color:white;">{stats['swap_count']} değişim</span>
            <span style="font-size:10px;color:rgba(255,255,255,0.7);">Elemanlar arası</span>
        </div>
    </div>
    """)
    
    # Veri boyutu rozeti
    badges.append(f"""
    <div style="display:inline-flex;align-items:center;background:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.1);
               padding:6px 10px;border-radius:16px;margin-right:8px;margin-bottom:8px;">
        <span style="margin-right:6px;font-size:14px;">📊</span>
        <div style="display:flex;flex-direction:column;">
            <span style="font-size:14px;font-weight:600;color:white;">{data_size} eleman</span>
            <span style="font-size:10px;color:rgba(255,255,255,0.7);">{data_type}</span>
        </div>
    </div>
    """)
    
    return "".join(badges)

def create_color_legend(algorithm_info: Dict[str, Dict]) -> str:
    """
    Algoritma renkleri için bir renk efsanesi (legend) HTML'i oluşturur.
    
    Args:
        algorithm_info: Algoritma bilgilerini içeren sözlük
        
    Returns:
        str: HTML renk efsanesi kodu
    """
    legend_items = []
    
    for algo_name, info in algorithm_info.items():
        color = info.get("plot_color", ALGORITHM_COLORS.get(algo_name, DEFAULT_COLORS[0]))
        icon = info.get("ikon", "")
        
        legend_items.append(f"""
        <div style="display:inline-flex;align-items:center;margin-right:15px;margin-bottom:10px;">
            <div style="width:12px;height:12px;border-radius:50%;background:{color};margin-right:8px;"></div>
            <span style="font-size:14px;color:white;">{icon} {algo_name}</span>
        </div>
        """)
    
    # Renk efsanesini bir container içine yerleştir
    legend_html = f"""
    <div style="display:flex;flex-wrap:wrap;justify-content:center;margin:15px 0;padding:10px;
                background:rgba(0,0,0,0.2);border-radius:8px;">
        {''.join(legend_items)}
    </div>
    """
    
    return legend_html

if __name__ == "__main__":
    # Test verileri
    import numpy as np
    
    test_data = np.random.randint(0, 100, 20).tolist()
    
    # Animasyon testi
    fig = create_algorithm_step_visualization([test_data, sorted(test_data)], 1, "Test")
    fig.write_html("test_animation.html")
    
    print("Test animasyonu oluşturuldu: test_animation.html")