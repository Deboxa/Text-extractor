import os
import sys
from datetime import datetime

# --- settings ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# make folder by day (YearMonthDay) and file by time (HHoursMMinutesSSeconds)
now = datetime.now()
day_folder = now.strftime("%Y%m%d")
file_name = now.strftime("H%HM%MS%S.txt")

OUT_DIR = os.path.join(SCRIPT_DIR, "results", day_folder)
os.makedirs(OUT_DIR, exist_ok=True)

OUTPUT = os.path.join(OUT_DIR, file_name)

# limits
MAX_LINES = 1000
MAX_BYTES = 2 * 1024 * 1024

# skip these folders for the TXT file (but they will still be shown in console)
IGNORE_DIRS = {
    '.git', 'results', 'node_modules', 'venv', '.venv', '__pycache__',
    'build', 'dist', 'out', '.idea', '.vscode'
}

# skip these file extensions for the TXT file
BINARY_EXT = {
    '.exe', '.dll', '.sys', '.bin', '.so', '.dylib', '.o', '.obj',
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.tif', '.tiff',
    '.pdf', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
    '.mp3', '.mp4', '.avi', '.mkv', '.mov', '.wav', '.flac', '.ogg',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.pyc', '.class', '.jar', '.iso', '.db', '.sqlite', '.msi', '.ttf', '.otf',
}

# check if file is binary
def is_binary(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in BINARY_EXT:
        return True
    try:
        with open(path, 'rb') as f:
            chunk = f.read(2048)
    except Exception:
        return True
    return b'\x00' in chunk

# read text file
def read_text(path):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return None, "[size]"
    except Exception:
        return None, "[err]"

    for enc in ('utf-8', 'cp1251', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc) as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= MAX_LINES:
                        return None, "[lines]"
                    lines.append(line)
                return ''.join(lines), ""
        except UnicodeDecodeError:
            continue
        except Exception:
            return None, "[err]"
    return None, "[err]"

def main():
    ROOT = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_DIR
    
    out_abs = os.path.abspath(OUTPUT)
    script_abs = os.path.abspath(__file__)
    
    added_files = []
    skipped_files = []
    total_lines = 0

    # --- print legend ---
    print("=== LEGEND ===")
    print("[tmp]   - temporary file")
    print("[dir]   - inside ignored folder")
    print("[self]  - script or output file")
    print("[bin]   - binary file")
    print("[size]  - file too large (over 2MB)")
    print("[lines] - too many lines (over 1000)")
    print("[err]   - read error / unknown encoding")
    print("==============\n")

    # open output file
    with open(OUTPUT, 'w', encoding='utf-8', newline='\n') as out:
        
        # walk through ALL folders (no dirnames pruning here)
        for dirpath, dirnames, filenames in os.walk(ROOT):
            
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                fabs = os.path.abspath(fpath)

                # 1. Check for temp files (live for 0.001 sec)
                if fname.startswith('~$') or fname.endswith(('.tmp', '.temp', '.swp', '.swo')):
                    skipped_files.append((fpath, "[tmp]"))
                    continue

                # 2. Check if file is inside ignored folders (e.g. .git, node_modules)
                path_parts = set(fpath.split(os.sep))
                if path_parts.intersection(IGNORE_DIRS):
                    skipped_files.append((fpath, "[dir]"))
                    continue

                # 3. Skip script itself and output file
                if fabs == out_abs or fabs == script_abs:
                    skipped_files.append((fpath, "[self]"))
                    continue

                # 4. Skip binary files
                if is_binary(fpath):
                    skipped_files.append((fpath, "[bin]"))
                    continue

                # 5. Check size, lines and read content
                content, reason = read_text(fpath)
                if content is None:
                    skipped_files.append((fpath, reason))
                    continue

                # --- if all checks passed, write to txt ---
                text_block = "=" * 70 + "\n" + f"File: {fpath}\n" + "=" * 70 + "\n" + content
                if not content.endswith('\n'):
                    text_block += '\n'
                text_block += '\n\n'
                
                out.write(text_block)
                total_lines += text_block.count('\n')
                added_files.append(fpath)

    # --- CONSOLE OUTPUT & ALIGNMENT ---
    
    # calculate max width for alignment based on the longest list
    max_count = max(len(added_files), len(skipped_files))
    width = len(str(max_count)) if max_count > 0 else 1
    
    # print all added (+)
    for i, fpath in enumerate(added_files, 1):
        print(f"{i:>{width}}[+] {fpath}")
        
    # print empty line separator
    print("\n")

    # print all skipped (-) with micro reasons right after [-]
    for i, (fpath, reason) in enumerate(skipped_files, 1):
        print(f"{i:>{width}}[-] {reason} {fpath}")

    # final stats
    file_size_bytes = os.path.getsize(OUTPUT)
    file_size_kb = file_size_bytes / 1024
    total_files = len(added_files) + len(skipped_files)

    print("\n=== DONE ===")
    print(f"Total files seen: {total_files}")
    print(f"Files added to txt: {len(added_files)}")
    print(f"Files skipped: {len(skipped_files)}")
    print(f"Total lines in txt: {total_lines}")
    print(f"Output size: {file_size_kb:.2f} KB")
    print(f"Output saved to: {OUTPUT}")

if __name__ == "__main__":
    main()