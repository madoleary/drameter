import re
import pdfplumber
import csv

DEFAULT_WPM = 130  # Words per minute (typical for screen dialogue)
BEAT_DURATION_SECONDS = 1.5  # Default duration per (beat)

# Reused regex pattern for dialogue blocks
DIALOGUE_BLOCK_PATTERN = r'^[A-Z0-9 ]{3,}(?:\n.+)+'

class Scene:
    """
    Represents a single screenplay scene.
    Extracts dialogue, action, and (beat) data to estimate runtime.
    """
    def __init__(self, heading, content):
        self.heading = heading.strip()
        self.content = content.strip()
        self.dialogue_words = 0
        self.action_words = 0
        self.beat_count = 0
        self.estimated_seconds = 0

    def analyze(self, wpm=DEFAULT_WPM, beat_duration=BEAT_DURATION_SECONDS):
        # Find dialogue blocks (lines after all-caps names)
        dialogue_blocks = re.findall(DIALOGUE_BLOCK_PATTERN, self.content, re.MULTILINE)
        dialogue = " ".join(dialogue_blocks)

        # Action = everything not part of dialogue
        action = re.sub(DIALOGUE_BLOCK_PATTERN, '', self.content, flags=re.MULTILINE)

        # Count words
        self.dialogue_words = len(dialogue.split())
        self.action_words = len(action.split())

        # Count (beat) pauses
        self.beat_count = len(re.findall(r'\(beat\)', dialogue, flags=re.IGNORECASE))
        beat_time = self.beat_count * beat_duration

        # Adjust pacing based on tone
        total_words = self.dialogue_words + self.action_words
        tone_multiplier = 0.8 if self.dialogue_words >= self.action_words else 1.2

        base_time = (total_words / wpm) * 60 * tone_multiplier
        self.estimated_seconds = base_time + beat_time

    def to_dict(self, index=None):
        scene_dict = {
            "scene_heading": self.heading,
            "dialogue_words": self.dialogue_words,
            "action_words": self.action_words,
            "beats": self.beat_count,
            "estimated_seconds": round(self.estimated_seconds, 1)
        }
        if index is not None:
            scene_dict["scene_number"] = index
        return scene_dict


def parse_script(text, wpm=DEFAULT_WPM, beat_duration=BEAT_DURATION_SECONDS):
    # Split script into scenes at INT./EXT. headings
    scene_chunks = re.split(r'\n(?=INT\.|EXT\.)', text)
    scenes = []

    for chunk in scene_chunks:
        # Splits each scene into its heading and content (everything else in the scene)
        lines = chunk.strip().split('\n', 1)
        if len(lines) == 2:
            heading, content = lines
            scene = Scene(heading, content)
            scene.analyze(wpm=wpm, beat_duration=beat_duration)
            scenes.append(scene)

    return scenes


def total_runtime(scenes):
    return sum(scene.estimated_seconds for scene in scenes)


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ''
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + '\n'
    return all_text


def export_to_csv(scenes, output_path="drameter_report.csv"):
    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "scene_number", "scene_heading", "dialogue_words", "action_words", "beats", "estimated_seconds"
        ])
        writer.writeheader()
        for i, scene in enumerate(scenes):
            writer.writerow(scene.to_dict(index=i + 1))