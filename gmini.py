import google.generativeai as genai
import os
from dotenv import load_dotenv
import csv

load_dotenv()

genai.configure(api_key=os.environ['GEMINI_API_KEY1'])

def labeling(news_headline):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(f"bayangkan kamu seorang pakar di bidang finance Klasifikasikan judul berita berikut menjadi positif netral atau negatif {news_headline} berikan jawaban satu kata saja")
    return response.text

def labeling_from_csv(csv_file):
    labeled_data = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            news_headline = row[0]  # Assuming the headline is in the first column
            label = labeling(news_headline)
            labeled_data.append((news_headline, label))

    return labeled_data

def write_to_csv(output_file, labeled_data):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Judul Berita', 'Label'])
        writer.writerows(labeled_data)

# Contoh penggunaan:
csv_file = 'data/data.csv'  # Ganti dengan nama file CSV yang sesuai
output_file = 'data/labeled1_data.csv'  # Nama file CSV output
labeled_data = labeling_from_csv(csv_file)

# Menulis data ke dalam file CSV baru
write_to_csv(output_file, labeled_data)

# Menampilkan hasil
for headline, label in labeled_data:
    print(f"Judul Berita: {headline}")
    print(f"Label: {label}")
    print(output_file)
