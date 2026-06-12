import json

def save_dataset(dataset, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

def merge_json_files(file1, file2, output_file):
    with open(file1, encoding="utf-8") as f1:
        data1 = json.load(f1)

    with open(file2, encoding="utf-8") as f2:
        data2 = json.load(f2)

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(data1 + data2, out, indent=2, ensure_ascii=False)