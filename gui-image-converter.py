from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

def convert_image_format(input_path, output_path, output_format):
    try:
        with Image.open(input_path) as img:
            if output_format.lower() in ['jpeg', 'jpg'] and img.mode in ['RGBA', 'LA', 'P']:
                img = img.convert('RGB')
            img.save(output_path, output_format.upper(), quality=85)  # Adjust quality for JPEG
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def process_file(filename, input_folder, output_folder, output_format):
    input_path = os.path.join(input_folder, filename)
    base, _ = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{base}.{output_format.lower()}")

    try:
        input_size = os.path.getsize(input_path)
        convert_image_format(input_path, output_path, output_format)
        output_size = os.path.getsize(output_path)
        size_change = ((output_size - input_size) / input_size) * 100
        return (filename, format_size(input_size), os.path.basename(output_path), format_size(output_size), f"{size_change:.2f}%")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return None

def batch_convert_image_format(input_folder, output_folder, output_format):
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp"]
    files = [f for f in os.listdir(input_folder) if os.path.splitext(f)[1].lower() in valid_extensions]

    if not files:
        print("No valid image files found in the input folder.")
        return

    total_files = len(files)
    file_info = []

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda f: process_file(f, input_folder, output_folder, output_format), files))

    for i, result in enumerate(results):
        if result:
            file_info.append(result)
        print_progress_bar(i + 1, total_files, prefix='Progress:', suffix='Complete', length=50)

    print("\nConversion Summary:")
    print(f"{'Input File':<30} {'Input Size':<15} {'Output File':<30} {'Output Size':<15} {'Size Change (%)':<15}")
    print("-" * 105)
    for info in file_info:
        print(f"{info[0]:<30} {info[1]:<15} {info[2]:<30} {info[3]:<15} {info[4]:<15}")

def get_output_format():
    formats = ["jpeg", "png", "bmp", "tiff", "gif", "webp"]
    print("Select the output format:")
    for i, fmt in enumerate(formats, 1):
        print(f"{i}. {fmt.upper()}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your desired format: "))
            if 1 <= choice <= len(formats):
                clear_console()
                return formats[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Example usage
input_folder = "./input"
output_folder = "./output"
output_format = get_output_format()  # Get the output format via user selection

batch_convert_image_format(input_folder, output_folder, output_format)
