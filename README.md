# 🔍 Macro Detector

Tool CLI berbasis Python untuk analisis macro pada file Office — cocok untuk keperluan **malware analysis** dan **forensics**.

---

## 📦 Requirements

- Python 3.8+
- pip

---

## ⚙️ Instalasi

### 1. Clone / Download project

```bash
git clone https://github.com/username/detect-macro-file.git
cd detect-macro-file
```

### 2. Buat virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
oletools
```

---

## 🚀 Penggunaan

```bash
python main.py
```

Akan muncul menu interaktif:

```
=== Macro Detector ===
1. Scan a file for macros
2. Exit
Enter your choice:
```

Pilih **1** → masukkan path file → tool akan otomatis:

1. Validasi file (path, tipe, ukuran)
2. Extract VBA macro
3. Deteksi IOC (Indicators of Compromise)
4. Hitung entropy
5. Opsional export report ke JSON

---

## 📁 Format File yang Didukung

| Extension | Keterangan |
|-----------|------------|
| `.docm`   | Word Macro-Enabled Document |
| `.xlsm`   | Excel Macro-Enabled Workbook |
| `.pptm`   | PowerPoint Macro-Enabled Presentation |

---

## 🧪 Testing dengan Sample File

Project ini sudah include file `Macro-File.docm` untuk keperluan testing.

File tersebut mengandung macro:

```vb
Sub AutoOpen()
    Shell "powershell.exe -EncodedCommand ZQBjAGgAbwAgAEgAZQBsAGwAbwAgAEYAcgBvAG0AIABNAGEAYwByAG8A"
End Sub
```

> ⚠️ File ini **tidak berbahaya** — hanya untuk keperluan testing tool ini.

### Cara testing:

```bash
python main.py
```

```
Enter your choice: 1
Enter the file path to scan: ./Macro-File.docm
```

### Expected output:

```
Scanning file: ./Macro-File.docm
✅ Macro ditemukan !

File: Macro-File.docm
Stream Path: VBA/Module1
VBA Filename: Module1.bas
VBA Code:
Sub AutoOpen()
    Shell "powershell.exe -EncodedCommand ZQBjAGgA..."
End Sub

🔍 Mendeteksi IOC...

[!] Kategori: Execution
✅ IOC Terdeteksi: Shell, PowerShell

[!] Kategori: Persistence
✅ IOC Terdeteksi: AutoOpen

📊 Entropy: 5.2341 (Medium)

Export report? (y/n): y
Enter output JSON filename (e.g., report.json): result.json
✅ Report JSON disimpan: reports/result.json
```

---

## 📊 Fitur

### 1. Extract VBA Macro
Membaca dan menampilkan isi kode VBA dari file Office secara in-memory (tidak menulis ulang file ke disk).

### 2. IOC Detection
Mendeteksi suspicious keywords berdasarkan kategori:

| Kategori | Contoh Keyword |
|----------|----------------|
| Execution | `Shell`, `WScript`, `PowerShell`, `CreateObject` |
| Persistence | `AutoOpen`, `AutoClose`, `Document_Open` |
| Network | `URLDownloadToFile`, `WinHttp`, `XMLHTTP` |
| Filesystem | `FileSystemObject`, `Kill`, `FileCopy` |
| Registry | `RegWrite`, `RegRead`, `HKEY` |
| Obfuscation | `Chr(`, `Base64`, `StrReverse` |

### 3. Entropy Analysis
Mengukur tingkat randomness kode VBA menggunakan **Shannon Entropy**:

| Score | Level | Indikasi |
|-------|-------|----------|
| < 3.5 | Low | Kode normal |
| 3.5 - 4.5 | Medium | Perlu diperiksa |
| > 4.5 | High | Kemungkinan obfuscated/encrypted |

### 4. Export Report (JSON)
Hasil analisis dapat diekspor ke file `.json` di folder `reports/`.

Contoh struktur report:

```json
{
    "file": "Macro-File.docm",
    "results": {
        "Module1.bas": {
            "ioc": {
                "execution": ["Shell", "PowerShell"],
                "persistence": ["AutoOpen"]
            },
            "entropy": {
                "score": 5.2341,
                "level": "Medium"
            },
            "vba_code": "Sub AutoOpen()..."
        }
    }
}
```

---

## 🛠️ Tools yang Digunakan

| Tool | Fungsi |
|------|--------|
| [oletools](https://github.com/decalage2/oletools) | Extract & analisis VBA macro dari file Office |
| `math` (stdlib) | Kalkulasi Shannon Entropy |
| `json` (stdlib) | Export report ke format JSON |
| `os` (stdlib) | Validasi file path & ukuran |

---

## 📝 Struktur Project

```
detect-macro-file/
├── main.py              # Entry point + semua logic
├── requirements.txt     # Dependencies
├── Macro-File.docm      # Sample file untuk testing
├── reports/             # Output JSON report (auto-created)
└── README.md
```

---

## ⚠️ Disclaimer

Tool ini dibuat untuk keperluan **edukasi** dan **malware analysis** secara legal. Jangan gunakan untuk menganalisis file tanpa izin pemiliknya.
