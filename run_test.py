import argparse
import os
from datetime import datetime

from drameter import (
    export_to_csv,
    extract_text_from_pdf,
    parse_script,
    total_runtime,
)

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
    parser.add_argument("--wpm", type=int, default=130, help="Words per minute (default: 130)")
    parser.add_argument("--beat", type=float, default=1.5, help="Seconds per (beat) pause (default: 1.5)")

    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    scenes = parse_script(text, wpm=args.wpm, beat_duration=args.beat)

    # Track scenes missing time of day
    missing_time_scenes = [s for s in scenes if getattr(s, "_has_missing_time_of_day", False)]

    print(f"\n📄 Loaded {len(scenes)} scenes from {args.pdf_path}\n")

    for i, scene in enumerate(scenes):
        s = scene.to_dict()
        scene_number = i + 1
        print(f"Scene {scene_number}: {s['scene_heading']}")
        print(f"  Type: {s['scene_type']}  |  Location: {s['location']}  |  Time: {s['time_of_day']}")
        print(f"  Dialogue: {s['dialogue_words']}w  |  Action: {s['action_words']}w  |  Beats: {s['beats']}")
        print(f"  Complexity: {s['complexity']}")
        print(f"  ⏱ Estimated time: {s['estimated_seconds']}s\n")

    total_seconds = total_runtime(scenes)
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    print(f"🎬 Total scenes analyzed: {len(scenes)}")
    print(f"⏳ Estimated total runtime: {minutes}m {seconds}s\n")

    if missing_time_scenes:
        print("⚠️ Warning: These EXT. scenes are missing a time of day:")
        for scene in missing_time_scenes:
            print(f"  • {scene.heading}")
        print()

    if args.export:
        export_path = args.export_path

        if export_path == "outputs/report.csv":
            script_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"outputs/report_{script_name}_{timestamp}.csv"

        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        export_to_csv(scenes, export_path)
        print(f"📄 CSV report saved to {export_path}")

if __name__ == "__main__":
    main()