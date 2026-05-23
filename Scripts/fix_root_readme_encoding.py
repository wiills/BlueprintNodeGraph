
# -*- coding: utf-8 -*-
"""Fix encoding issues for root README.md and README_CN.md."""
from pathlib import Path
import chardet

ROOT = Path(__file__).resolve().parents[1]


def detect_encoding(path: Path) -&gt; tuple[str | None, float]:
    """Detect file encoding using chardet."""
    raw = path.read_bytes()
    result = chardet.detect(raw)
    return result["encoding"], result["confidence"]


def try_fix_file(path: Path) -&gt; bool:
    """Try to fix file encoding by trying common encodings."""
    raw = path.read_bytes()
    
    # Common encodings to try
    encodings = [
        "utf-8",
        "gbk",
        "gb2312",
        "gb18030",
        "big5",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
    ]
    
    for enc in encodings:
        try:
            text = raw.decode(enc)
            # Check if decoding makes sense (few replacement chars)
            if text.count("\ufffd") &lt; len(text) * 0.01:
                # Write back as UTF-8
                path.write_text(text, encoding="utf-8", newline="\n")
                print(f"{path.name}: fixed using {enc}")
                return True
        except UnicodeDecodeError:
            continue
    
    print(f"{path.name}: could not fix encoding")
    return False


if __name__ == "__main__":
    files = [
        ROOT / "README.md",
        ROOT / "README_CN.md",
    ]
    
    print("Checking and fixing root README files...")
    for file_path in files:
        if file_path.exists():
            enc, conf = detect_encoding(file_path)
            print(f"{file_path.name}: detected encoding={enc}, confidence={conf:.2f}")
            try_fix_file(file_path)
        else:
            print(f"{file_path.name}: not found")
    
    print("\nDone.")
