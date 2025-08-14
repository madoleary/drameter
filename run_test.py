import argparse
import os
from drameter import export_to_csv, extract_text_from_pdf, parse_script, total_runtime
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Estimate screenplay runtime from a PDF.")
    parser.add_argument("pdf_path", type=str, help="Path to your screenplay PDF file")
    parser.add_argument("--export", action="store_true", help="Export results to CSV")
    parser.add_argument(
        "--export-path",
        type=str,
        default="outputs/report.csv",
        help="Custom output path for CSV export (default: outputs/report.csv)"
    )

    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    scenes = parse_script(text)

    for i, scene in enumerate(scenes):
        print(f"Scene {i+1}:")
        print(scene.to_dict(index=i+1))
        print()

    total_seconds = total_runtime(scenes)
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    print(f"Total scenes analyzed: {len(scenes)}")
    print(f"Estimated total runtime: {minutes}m {seconds}s")

    if args.export:
        export_path = args.export_path

        # If user is using the default path, auto-append filename + timestamp
        if export_path == "outputs/report.csv":
            # Extract just the base script name (no extension)
            script_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"outputs/report_{script_name}_{timestamp}.csv"

        # Ensure the export directory exists
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        export_to_csv(scenes, export_path)
        print(f"📄 CSV report saved to {export_path}")

if __name__ == "__main__":
    main()