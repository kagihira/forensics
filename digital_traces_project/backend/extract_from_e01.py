import os
import subprocess

EXTRACTED_DIR = "data"

def extract_files_from_e01(e01_path, output_folder=EXTRACTED_DIR):
    """Извлекает файлы из .E01 с помощью `tsk_recover` (без `ewfmount`)"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 1️⃣ Определяем разделы
    partition_cmd = ["mmls", e01_path]
    result = subprocess.run(partition_cmd, capture_output=True, text=True)

    start_sector = None
    for line in result.stdout.splitlines():
        if "NTFS" in line or "FAT" in line:
            parts = line.split()
            start_sector = parts[2]  # Берём номер первого сектора
            break

    if start_sector is None:
        print("❌ Ошибка: Раздел не найден")
        return False

    # 2️⃣ Извлекаем файлы с `tsk_recover`
    recover_cmd = ["tsk_recover", "-a", "-o", start_sector, e01_path, output_folder]
    try:
        subprocess.run(recover_cmd, check=True)
        print(f"✅ Файлы извлечены в {output_folder}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при извлечении: {e.stderr}")
        return False
