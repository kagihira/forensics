import os
import subprocess
import shutil

def extract_files_from_e01(e01_path: str, device_id: str) -> bool:
    ewf_mount = "/tmp/ewf_mount"
    output_folder = os.path.abspath(f"data/{device_id}")
    print(">>>> Сохраняем в:", output_folder)

    # Очистим и подготовим точки
    if os.path.exists(ewf_mount):
        try:
            subprocess.run(["umount", ewf_mount], check=True)
        except:
            subprocess.run(["fusermount", "-u", ewf_mount], check=False)
        shutil.rmtree(ewf_mount)
    os.makedirs(ewf_mount, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # 1. Монтируем образ
    try:
        subprocess.run(["ewfmount", e01_path, ewf_mount], check=True)
        print("✅ EWF-контейнер смонтирован")
    except Exception as e:
        print(f"❌ Ошибка ewfmount: {e}")
        return False

    raw_image = os.path.join(ewf_mount, "ewf1")

    # 2. Получаем разделы
    result = subprocess.run(["mmls", raw_image], capture_output=True, text=True)
    sectors = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) > 2 and any(fs in line for fs in ("NTFS", "FAT", "exFAT", "EXT", "HFS")):
            sectors.append(parts[2])
    if not sectors:
        print("Раздел не найден, пробуем сектор 0")
        sectors = ["0"]

    # 3. Пробуем вытаскивать
    for sector in sectors:
        try:
            subprocess.run(["tsk_recover", "-a", "-o", sector, raw_image, output_folder], check=True)
            print(f"✅ Файлы извлечены в {output_folder}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ tsk_recover не сработал: {e}")
            continue

    print("❌ Не удалось извлечь файлы ни с одного раздела")
    return False
