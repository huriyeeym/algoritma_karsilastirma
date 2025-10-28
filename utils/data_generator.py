"""
Veri Üreteci Modülü

Bu modül, sıralama algoritmaları için çeşitli test verileri üretir.
"""

import random
import json
from pathlib import Path

def generate_random_data(size, min_val=0, max_val=1000):
    """
    Belirtilen boyutta rastgele tam sayı dizisi oluşturur.
    
    Args:
        size (int): Dizinin boyutu
        min_val (int): Minimum değer
        max_val (int): Maksimum değer
        
    Returns:
        list: Rastgele tam sayılardan oluşan liste
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def generate_nearly_sorted_data(size, swap_percent=5):
    """
    Kısmen sıralanmış veri oluşturur.
    
    Args:
        size (int): Dizinin boyutu
        swap_percent (int): Karıştırılacak yüzde (0-100 arası)
        
    Returns:
        list: Kısmen sıralı liste
    """
    # Güvenlik kontrolü
    swap_percent = min(100, max(0, swap_percent))
    
    # Önce sıralı bir dizi oluştur
    data = list(range(size))
    
    # Belirtilen yüzdeye göre rastgele elemanları değiştir
    num_swaps = int(size * swap_percent / 100)
    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        data[i], data[j] = data[j], data[i]
    
    return data

def generate_reverse_sorted_data(size):
    """
    Ters sıralı veri oluşturur.
    
    Args:
        size (int): Dizinin boyutu
        
    Returns:
        list: Ters sıralı liste
    """
    return list(range(size, 0, -1))

def generate_sorted_data(size):
    """
    Sıralı veri oluşturur (rastgele veriyi sıralayarak).
    
    Args:
        size (int): Dizinin boyutu
        
    Returns:
        list: Sıralı liste
    """
    data = generate_random_data(size)
    data.sort()
    return data

# Veri türleri ve ilgili üreteç fonksiyonları
VERI_TURLERI = {
    "random": {
        "func": generate_random_data,
        "desc": "Rastgele Veri",
        "file": "sample_inputs.json"
    },
    "nearly_sorted": {
        "func": generate_nearly_sorted_data,
        "desc": "Kısmen Sıralı Veri",
        "file": "nearly_sorted.json"
    },
    "sorted": {
        "func": generate_sorted_data,
        "desc": "Sıralı Veri",
        "file": "sorted_data.json"
    },
    "reverse_sorted": {
        "func": generate_reverse_sorted_data,
        "desc": "Ters Sıralı Veri",
        "file": "reverse_sorted.json"
    }
}

def save_data_to_json(data, filename):
    """
    Veriyi JSON dosyasına kaydeder.
    
    Args:
        data (list): Kaydedilecek veri
        filename (str): Dosya adı
    """
    directory = Path("data")
    directory.mkdir(exist_ok=True)
    
    file_path = directory / filename
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return file_path

def load_data_from_json(filename):
    """
    Veriyi JSON dosyasından yükler.
    
    Args:
        filename (str): Dosya adı
        
    Returns:
        list: Yüklenen veri veya None (dosya bulunamadıysa)
    """
    file_path = Path("data") / filename
    
    if not file_path.exists():
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_data_by_type(data_type, size):
    """
    Belirtilen türe göre veri oluşturur.
    
    Args:
        data_type (str): Veri türü ('random', 'nearly_sorted', 'sorted', 'reverse_sorted')
        size (int): Veri boyutu
    
    Returns:
        list: Oluşturulan veri listesi
    """
    if data_type not in VERI_TURLERI:
        raise ValueError(f"Geçersiz veri türü: {data_type}. Geçerli türler: {list(VERI_TURLERI.keys())}")
    
    return VERI_TURLERI[data_type]["func"](size)

# Örnek verileri oluştur ve kaydet
def generate_sample_data(size=1000):
    """
    Örnek veri setleri oluşturur ve kaydeder.
    
    Args:
        size (int, optional): Her veri setinin boyutu. Varsayılan 1000.
    
    Returns:
        dict: Oluşturulan veri setleri sözlüğü
    """
    result = {}
    
    # Tüm veri türleri için veri oluştur ve kaydet
    for data_type, info in VERI_TURLERI.items():
        data = info["func"](size)
        file_path = save_data_to_json(data, info["file"])
        
        result[data_type] = {
            "data": data,
            "path": str(file_path),
            "size": size,
            "desc": info["desc"]
        }
    
    return result

if __name__ == "__main__":
    import argparse
    
    # Komut satırı argümanlarını işle
    parser = argparse.ArgumentParser(description='Algoritma karşılaştırması için örnek veri setleri oluştur')
    parser.add_argument('--size', type=int, default=1000, help='Oluşturulacak veri setlerinin boyutu (varsayılan: 1000)')
    parser.add_argument('--type', choices=VERI_TURLERI.keys(), default=None, 
                        help='Sadece belirtilen türde veri oluştur (varsayılan: tüm türler)')
    args = parser.parse_args()
    
    # Tek bir veri türü mü yoksa tümü mü oluşturulacak
    if args.type:
        data = generate_data_by_type(args.type, args.size)
        file_path = save_data_to_json(data, VERI_TURLERI[args.type]["file"])
        print(f"{VERI_TURLERI[args.type]['desc']} başarıyla oluşturuldu! (Boyut: {args.size})")
        print(f"Oluşturulan dosya: {file_path}")
    else:
        # Tüm veri türlerini oluştur
        data = generate_sample_data(args.size)
        print(f"Örnek veriler başarıyla oluşturuldu! (Boyut: {args.size})")
        print(f"Oluşturulan dosyalar:")
        for key, value in data.items():
            print(f"  - {VERI_TURLERI[key]['desc']}: {value['path']}")