import google.generativeai as genai
import os
from dotenv import load_dotenv
import csv
import time
import itertools

# Load environment variables
load_dotenv()

# Configure the generative model
genai.configure(api_key=os.environ['GEMINI_API_KEY_v6'])

# Function to label a single news headline
def labeling(news_headline):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(
        f"bayangkan kamu seorang pakar di bidang finance. Klasifikasikan judul berita berikut menjadi positif, netral, atau negatif: {news_headline}. Berikan jawaban satu kata saja."
    )
    return response.text.strip()

# Function to process a batch of news headlines from a CSV file
def labeling_from_csv(csv_file, start_index, batch_size=3):
    labeled_data = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in itertools.islice(reader, start_index, start_index + batch_size):
            news_headline = row[0]  # Assuming the headline is in the first column
            label = labeling(news_headline)
            labeled_data.append((news_headline, label))

    return labeled_data

# Function to write labeled data to a CSV file
def write_to_csv(output_file, labeled_data):
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(labeled_data)

# Function to save the last processed index
def save_last_index(file_name, last_index):
    with open(file_name, 'w') as file:
        file.write(str(last_index))

# Function to load the last processed index
def load_last_index(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return int(file.read().strip())
    return 0

# Main loop to process data every minute
def main_loop(csv_file, output_file, index_file, batch_size=3, interval=60):
    start_index = load_last_index(index_file)
    while True:
        labeled_data = labeling_from_csv(csv_file, start_index, batch_size)
        if not labeled_data:
            print("No more data to process.")
            break
        
        write_to_csv(output_file, labeled_data)
        start_index += batch_size
        save_last_index(index_file, start_index)
        
        # Display the results
        for headline, label in labeled_data:
            print(f"Judul Berita: {headline}")
            print(f"Label: {label}")
        
        # Sleep for the specified interval (in seconds)
        time.sleep(interval)

# Example usage
csv_file = 'data/april_2024_v3.csv'  # Replace with the name of your input CSV file
output_file = 'label_data/Lebel_April_2024_v3.csv'  # Name of the output CSV file
index_file = 'data/last_index_v3.txt'  # File to store the last processed index

# Write header to output file only once if the file does not exist
if not os.path.exists(output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Judul Berita', 'Label'])

# Start the main loop
main_loop(csv_file, output_file, index_file)
