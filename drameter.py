import re # Python’s regular expression module, used to match scene headings, dialogue blocks, and (beat)s
import pdfplumber # A library to extract text from PDF files. Keeps screenplay format intact
import csv # exporting scene data to CSV

DEFAULT_WPM = 130  # Words per minute (typical for screen dialogue)
BEAT_DURATION_SECONDS = 1.5  # Default duration per (beat)

# Class to represent one scene from a screenplay.
class Scene:
    def __init__(self, heading, content):
        self.heading = heading.strip()
        self.content = content.strip()
        self.dialogue_words = 0
        self.action_words = 0
        self.beat_count = 0
        self.estimated_seconds = 0

    # Calculates the dialogue vs. action word count and estimates the scene’s time
    def analyze(self):
        # Find dialogue blocks (lines after all-caps names), joins them into a single string
        # This assumes dialogue is always in all caps and follows a character name
        # Example: "JOHN\nHello there.\nMARY\nHi!"
        dialogue_blocks = re.findall(r'^[A-Z0-9 ]{3,}(?:\n.+)+', self.content, re.MULTILINE)
        dialogue = " ".join(dialogue_blocks)

        # Action = everything not part of dialogue
        # Removes dialogue blocks from the content — what’s left is considered action (scene description, movement, etc.)
        # This is a simple heuristic and may not cover all screenplay formats
        # Example: "INT. HOUSE - DAY\nJohn enters the room.\nMARY\nHi!"
        # Here, "John enters the room." is considered action.
        action = re.sub(r'^[A-Z0-9 ]{3,}(?:\n.+)+', '', self.content, flags=re.MULTILINE)

        # Counts how many words are in the dialogue and action parts
        # Uses split() to count words, which is a simple way to handle whitespace
        # Note: This does not handle punctuation or special characters, which may affect word count
        self.dialogue_words = len(dialogue.split())
        self.action_words = len(action.split())

        # Finds all instances of (beat) in dialogue (case-insensitive) and stores how many there are.
        # This is a common notation in screenplays to indicate a pause or beat in dialogue
        # Example: "JOHN\nHello there. (beat)\nMARY\nHi!"
        # Here, "(beat)" indicates a pause after "Hello there."
        # The beat count is multiplied by a default duration to estimate time spent on beats
        # This is a simple heuristic and may not cover all screenplay formats
        self.beat_count = len(re.findall(r'\(beat\)', dialogue, flags=re.IGNORECASE))
        # Calculates how much total time (beat)s add to the scene.
        # Each (beat) is assumed to take BEAT_DURATION_SECONDS seconds
        beat_time = self.beat_count * BEAT_DURATION_SECONDS

        # Calculates total words in the scene and applies a multiplier based on dialogue vs. action
        # If dialogue words are greater than or equal to action words, assume a more conversational tone
        # Dialogue-heavy scenes are faster → 0.8
        # If action words are greater, assume a more dramatic tone
        # Action-heavy scenes are slower → 1.2
        total_words = self.dialogue_words + self.action_words
        tone_multiplier = 0.8 if self.dialogue_words >= self.action_words else 1.2

        # base_time: converts words into time using WPM and tone multiplier
        # Adds beat time to calculate the final estimated scene time
        base_time = (total_words / DEFAULT_WPM) * 60 * tone_multiplier
        self.estimated_seconds = base_time + beat_time

    # Converts scene data into a dictionary for easy access and printing
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

# Splits the entire screenplay text into individual scenes
def parse_script(text):
    # Split script into scenes at INT./EXT. headings (keep headings)
    scene_chunks = re.split(r'\n(?=INT\.|EXT\.)', text)
    scenes = []

    # Starts building a list of Scene objects
    # Each scene chunk is expected to have a heading and content
    # The heading is the first line, and the rest is considered content
    for chunk in scene_chunks:
        # Splits each scene into its heading and the content (everything else in the scene
        lines = chunk.strip().split('\n', 1)
        if len(lines) == 2:
            heading, content = lines
            # Creates a Scene object, analyzes it, and adds it to the list
            scene = Scene(heading, content)
            scene.analyze()
            scenes.append(scene)

    return scenes

# Adds up all the scene times to get the total runtime estimate for the full script
def total_runtime(scenes):
    return sum(scene.estimated_seconds for scene in scenes)

# Reads text from a screenplay PDF
# Goes page by page, extracts text, and joins it all together with line breaks
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