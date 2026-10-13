import os
import sys
import subprocess
import markdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE_DIR, "technical_report.md")
HTML_PATH = os.path.join(BASE_DIR, "report.html")
PDF_PATH = os.path.join(BASE_DIR, "TeamName_Report.pdf")

def generate():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    body_html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Technical Report — Human-vs-System-in-the-Loop-Apertus</title>
    <style>
        @page {{
            size: A4;
            margin: 16mm 14mm 16mm 14mm;
        }}
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            h2 {{
                page-break-after: avoid;
            }}
            table, pre, blockquote {{
                page-break-inside: avoid;
            }}
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.55;
            color: #1e293b;
            margin: 0;
            padding: 0;
            background: #ffffff;
        }}
        h1 {{
            font-size: 19pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0 0 6px 0;
            letter-spacing: -0.02em;
            line-height: 1.2;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 8px;
        }}
        h2 {{
            font-size: 12.5pt;
            font-weight: 700;
            color: #1e3a8a;
            margin: 18px 0 8px 0;
            letter-spacing: -0.01em;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
        }}
        h3 {{
            font-size: 10.5pt;
            font-weight: 600;
            color: #334155;
            margin: 12px 0 6px 0;
        }}
        p {{
            margin: 0 0 8px 0;
        }}
        ul, ol {{
            margin: 0 0 10px 0;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 3px;
        }}
        blockquote {{
            margin: 8px 0 14px 0;
            padding: 8px 14px;
            background: #f8fafc;
            border-left: 4px solid #2563eb;
            color: #334155;
            font-size: 9.5pt;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 14px 0;
            font-size: 8.5pt;
        }}
        th, td {{
            padding: 6px 8px;
            text-align: left;
            border: 1px solid #cbd5e1;
        }}
        th {{
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }}
        tr:nth-child(even) {{
            background: #f8fafc;
        }}
        code {{
            font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
            font-size: 8.5pt;
            background: #f1f5f9;
            padding: 1px 4px;
            border-radius: 3px;
            color: #0f172a;
        }}
        pre {{
            background: #0f172a;
            color: #f8fafc;
            padding: 10px 14px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 10px 0;
            font-size: 8pt;
            line-height: 1.4;
        }}
        pre code {{
            background: transparent;
            color: #f8fafc;
            padding: 0;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 14px 0;
        }}
        strong {{
            color: #0f172a;
            font-weight: 600;
        }}
        .header-meta {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 14px;
            font-size: 9pt;
        }}
    </style>
</head>
<body>
{body_html}
</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ Generated HTML report: {HTML_PATH}")

    # Invoke Edge to print PDF
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_PATH}",
        "--no-pdf-header-footer",
        HTML_PATH,
    ]
    print(f"🚀 Printing to PDF using Microsoft Edge...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(PDF_PATH):
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"🎉 Successfully generated PDF: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print(f"❌ Failed to generate PDF: {result.stderr}")

if __name__ == "__main__":
    generate()
