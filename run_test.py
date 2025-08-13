import argparse
from drameter import extract_text_from_pdf, parse_script, total_runtime

def main():
    parser = argparse.ArgumentParser(description="Estimate screenplay runtime from a PDF.")
    parser.add_argument("pdf_path", type=str, help="Path to your screenplay PDF file")

    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    scenes = parse_script(text)

    for i, scene in enumerate(scenes):
        print(f"Scene {i+1}:")
        print(scene.to_dict())
        print()

    total_minutes = total_runtime(scenes) / 60
    print(f"Estimated total runtime: {total_minutes:.2f} minutes")

if __name__ == "__main__":
    main()