import re
import pdfplumber
import csv

DEFAULT_WPM = 130  # Words per minute (typical for screen dialogue)
BEAT_DURATION_SECONDS = 1.5  # Default duration per (beat)

# Reused regex pattern for dialogue blocks
DIALOGUE_BLOCK_PATTERN = r'^[A-Z0-9 ]{3,}(?:\n.+)+'

# Complexity thresholds
DIALOGUE_DOMINANT_THRESHOLD = 0.6
ACTION_DOMINANT_THRESHOLD = 0.4
LONG_SCENE_WORDS = 300

COMPLEXITY_TYPES = {
    "dialogue": "dialogue-heavy",
    "action": "action-heavy",
    "balanced": "balanced",
    "empty": "empty",
    "unknown": "unknown"
}

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
        self.complexity = COMPLEXITY_TYPES["unknown"]  # Will be determined during analysis
        self.scene_type = None
        self.location = None
        self.time_of_day = None

    def analyze(self, wpm=DEFAULT_WPM, beat_duration=BEAT_DURATION_SECONDS):
        self.parse_heading()
        # Extract dialogue blocks
        dialogue_blocks = re.findall(DIALOGUE_BLOCK_PATTERN, self.content, re.MULTILINE)
        dialogue = " ".join(dialogue_blocks)

        # Everything else is action
        action = re.sub(DIALOGUE_BLOCK_PATTERN, '', self.content, flags=re.MULTILINE)

        # Word counts
        self.dialogue_words = len(dialogue.split())
        self.action_words = len(action.split())
        total_words = self.dialogue_words + self.action_words

        # Early exit for empty scenes
        if total_words == 0:
            self.complexity = COMPLEXITY_TYPES["empty"]
            self.estimated_seconds = 0
            return

        # Determine pacing bias
        ratio = self.dialogue_words / total_words
        if ratio >= DIALOGUE_DOMINANT_THRESHOLD:
            base_complexity = COMPLEXITY_TYPES["dialogue"]
        elif ratio <= ACTION_DOMINANT_THRESHOLD:
            base_complexity = COMPLEXITY_TYPES["action"]
        else:
            base_complexity = COMPLEXITY_TYPES["balanced"]

        # Optional tag for long scenes
        is_long = total_words > LONG_SCENE_WORDS
        self.complexity = f"{base_complexity} (long)" if is_long else base_complexity

        # Beat timing
        self.beat_count = len(re.findall(r'\(beat\)', dialogue, flags=re.IGNORECASE))
        beat_time = self.beat_count * beat_duration

        # Adjust pacing multiplier
        tone_multiplier = 0.8 if self.dialogue_words >= self.action_words else 1.2
        base_time = (total_words / wpm) * 60 * tone_multiplier

        self.estimated_seconds = base_time + beat_time

    def to_dict(self):
        return {
            "scene_heading": self.heading,
            "scene_type": self.scene_type,
            "location": self.location,
            "time_of_day": self.time_of_day,
            "dialogue_words": self.dialogue_words,
            "action_words": self.action_words,
            "beats": self.beat_count,
            "estimated_seconds": round(self.estimated_seconds, 1),
            "complexity": self.complexity
        }
    
    def parse_heading(self):
        """
        Parses the scene heading into type (INT/EXT), location, and time of day.
        Handles edge cases: dash variants, spacing issues, missing time, INT/EXT hybrids.
        """
        raw_heading = self.heading.strip().upper()

        # Normalize punctuation
        normalized = re.sub(r'[–—]|--', '-', raw_heading)
        normalized = re.sub(r'\s*-\s*', ' - ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        # Handle INT/EXT hybrids
        hybrid_match = re.match(r'^(INT\s*\.?\s*/\s*EXT\s*\.?|EXT\s*\.?\s*/\s*INT\s*\.?)\s+(.*)', normalized)
        if hybrid_match:
            self.scene_type = "INT/EXT"
            remainder = hybrid_match.group(2)
        else:
            std_match = re.match(r'^(INT|EXT)[.]?\s*(.*)', normalized)
            if std_match:
                self.scene_type = std_match.group(1)
                remainder = std_match.group(2)
            else:
                self.scene_type = "UNKNOWN"
                self.location = raw_heading
                self.time_of_day = "UNKNOWN"
                return

        # Split into location and time
        if ' - ' in remainder:
            parts = remainder.rsplit(' - ', 1)
            location = parts[0].strip().strip('-').strip()
            time_of_day = parts[1].strip() if parts[1].strip() else "UNKNOWN"
        else:
            location = remainder.strip().strip('-').strip()
            time_of_day = "UNKNOWN"

        self.location = re.sub(r'\s+', ' ', location)
        self.time_of_day = re.sub(r'\s+', ' ', time_of_day)


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
    if not scenes:
        print("⚠️ No scenes to export.")
        return

    # Use keys from the first scene as base fieldnames
    first_row = scenes[0].to_dict()
    fieldnames = ["scene_number"] + list(first_row.keys())

    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i, scene in enumerate(scenes):
            row = {"scene_number": i + 1, **scene.to_dict()}
            writer.writerow(row)