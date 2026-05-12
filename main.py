import os

SUSPICIOUS_KEYWORDS = {
    "execution": [
        "Shell", "WScript", "PowerShell", "cmd.exe", "CreateObject"
    ],
    "persistence": [
        "AutoOpen", "AutoClose", "AutoExec", "Document_Open", "Workbook_Open"
    ],
    "network": [
        "URLDownloadToFile", "WinHttp", "XMLHTTP", "InternetOpen"
    ],
    "filesystem": [
        "FileSystemObject", "Open", "Write", "Kill", "FileCopy"
    ],
    "registry": [
        "RegWrite", "RegRead", "HKEY", "regedit"
    ],
    "obfuscation": [
        "Chr(", "Asc(", "Base64", "Environ", "StrReverse"
    ]
}

def scanner(file_path):
    print(f"Scanning file: {file_path}")
    from oletools.olevba import VBA_Parser
    
    if not os.path.isfile(file_path):
        print("File tidak ditemukan !")
        return None
    if not file_path.lower().endswith(('.docm','.xlsm','.pptm')):
        print("File Type tidak didukung !")
        return None
    if os.path.getsize(file_path) == 0:  # 10 MB limit
        print("File Kosong !")
        return None
    
    try: 
        with open(file_path, 'rb') as f:
            data = f.read()
        vba_parser = VBA_Parser(file_path, data=data)
        print(f"Type: {vba_parser.type}")           # cek tipe file yang didetect
        print(f"Data size: {len(data)} bytes")
        if not vba_parser.detect_vba_macros():
            print("Tidak ada Macro ditemukan !")
            return None
        print("✅ Macro ditemukan !")
        macros = {}
        for (filename, stream_path, vba_filename, vba_code) in vba_parser.extract_macros():
            print(f"\nFile: {filename}")
            print(f"Stream Path: {stream_path}")
            print(f"VBA Filename: {vba_filename}")
            print("VBA Code:")
            print(vba_code)
            macros[vba_filename] = {
                "filename": filename,
                "stream_path": stream_path,
                "vba_filename": vba_filename,
                "vba_code": vba_code
            }
        
        return macros
    
    except Exception as e:
        print(f"Error opening file: {e}")
        return None

def detect_ioc(vba_code):
    print("\n🔍 Mendeteksi IOC...")
    found = {}
    for category, keywords in SUSPICIOUS_KEYWORDS.items():
        matches = []
        for keyword in keywords:
            if keyword.lower() in vba_code.lower():
                matches.append(keyword)
        if matches:
            print("✅ IOC Terdeteksi:") 
            print(f"\n[!] Kategori: {category.capitalize()}")
            found[category] = matches
        
    return found

def calculate_entropy(data):
    if not data:
        return 0.0
    
    import math
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1

    entropy = 0
    for freq in frequency.values():
        probability = freq / len(data)
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)

def entropy_level(ent):
    if ent < 3.5:
        return "Low"
    elif 3.5 <= ent < 4.5:
        return "Medium"
    else:
        return "High"

def export_json(data, output_name):
    import json
    output_path = "reports/" + output_name
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"✅ Report JSON disimpan: {output_path}")

def main():
    while True:
        print("\n=== Macro Detector ===")
        print("1. Scan a file for macros")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            file = scanner(input("Enter the file path to scan: "))
            if file:
                report = {}
                for vba_filename,module in file.items():
                    ioc = detect_ioc(module["vba_code"])
                    ent = calculate_entropy(module["vba_code"])
                    level = entropy_level(ent)
                    
                    if len(ioc) == 0:
                        print("❌ Tidak ada IOC yang mencurigakan ditemukan.")
                        
                    print(f"\n📊 Entropy: {ent} ({level})")
                    
                    report[vba_filename] = {
                        "ioc": ioc,
                        "entropy": {"score": ent, "level": level},
                        "vba_code": module["vba_code"]
                    }
                export = input("\nExport report? (y/n): ")
                if export.lower() == 'y':
                    output_name = input("Enter output JSON filename (e.g., report.json): ")
                    export_json({"file": file, "results": report}, output_name)
                
        elif choice == "2":
            print("Bye !")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":    main()