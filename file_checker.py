import hashlib
import os

def calculate_file_hash(filepath):
    """Dosyanın SHA-256 dijital parmak izini hesaplar."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def verify_integrity(filepath, expected_hash):
    """Dosyanın güncel hali ile beklenen hash değerini karşılaştırır."""
    current_hash = calculate_file_hash(filepath)
    if current_hash is None:
        print(f"[HATA] '{filepath}' dosyası bulunamadı.")
        return False
    
    print(f"Mevcut SHA-256: {current_hash}")
    print(f"Beklenen SHA-256: {expected_hash}")
    
    if current_hash == expected_hash:
        print("[BAŞARILI] Dosya bütünlüğü korundu. Dosyada herhangi bir değişiklik yok.")
        return True
    else:
        print("[UYARI] Dosya değiştirilmiş! Dijital parmak izi eşleşmiyor.")
        return False

if __name__ == "__main__":
    # Test için örnek bir dosya oluşturalım
    test_file = "ornek_delil.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Gizli adli bilişim kayıt raporu.")

    print("--- 1. Adım: Dosya Oluşturuldu ve Hash Alınıyor ---")
    original_hash = calculate_file_hash(test_file)
    print(f"İlk Hash Değeri: {original_hash}\n")

    print("--- 2. Adım: Dosya Bütünlüğü Doğrulanıyor ---")
    verify_integrity(test_file, original_hash)
    print()

    print("--- 3. Adım: Dosyaya Müdahale Ediliyor (Değişiklik Testi) ---")
    with open(test_file, "a", encoding="utf-8") as f:
        f.write(" İzinsiz eklenen veri!")
    
    # Tekrar kontrol:
    verify_integrity(test_file, original_hash)

    # Temizlik
    if os.path.exists(test_file):
        os.remove(test_file)
