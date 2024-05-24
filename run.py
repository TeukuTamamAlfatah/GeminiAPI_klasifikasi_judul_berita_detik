# import os

# # Menjalankan program pertama
# os.system("python gemini_v1.py")

# # Menjalankan program kedua
# os.system("python gemini_v2.py")

# # Menjalankan program ketiga
# os.system("python gemini_v3.py")

# # Menjalankan program emapat
# os.system("python gemini_v4.py")

# # Menjalankan program lima
# os.system("python gemini_v5.py")

# # Menjalankan program lima
# os.system("python gemini_v6.py")

import concurrent.futures

# Fungsi untuk menjalankan skrip Python
def run_script(script_name):
    import subprocess
    subprocess.run(["python", script_name])

# Daftar nama skrip yang akan dijalankan
scripts = ["gemini_v4.py", "gemini_v5.py", "gemini_v6.py"]

# Menjalankan semua skrip secara bersamaan
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_script, scripts)

print("Semua skrip telah dijalankan secara bersamaan.")
