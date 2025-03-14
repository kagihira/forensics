import os
import subprocess

def extract_files_from_e01(e01_path, output_folder):
    """Извлекает файлы из `.E01` в указанную папку"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    partition_cmd = ["mmls", e01_path]
    result = subprocess.run(partition_cmd, capture_output=True, text=True)

    start_sector = None
    for line in result.stdout.splitlines():
        if "NTFS" in line or "FAT" in line:
            parts = line.split()
            start_sector = parts[2]
            break

    if start_sector is None:
        print("❌ Ошибка: Раздел не найден")
        return False

    recover_cmd = ["tsk_recover", "-a", "-o", start_sector, e01_path, output_folder]
    try:
        subprocess.run(recover_cmd, check=True)
        print(f"✅ Файлы извлечены в {output_folder}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при извлечении: {e.stderr}")
        return False
