# 🎬 Drameter

**Smart screenplay timing tool for filmmakers. Not marketers.**

Drameter estimates the runtime of a screenplay by analyzing its structure, dialogue, action, and pacing cues like `(beat)`. It’s built for screenwriters, directors, and editors who want a scene-by-scene breakdown of timing — not just a generic words-per-minute estimate.

I built this because I tend to write action-heavy scripts, which complicates time estimation. It's not perfect, but I do believe it's more accurate than the minute-per-page standard. I also found other online tools to be either:  
1) Annoying, or  
2) Geared toward people writing scripts for YouTube videos (no shade).

---

## ✨ Features

- 🗂️ Scene-by-scene analysis from `INT.` / `EXT.` headings  
- 🗣️ Differentiates between dialogue and action blocks  
- ⏱️ Estimates time using customizable words-per-minute (WPM)  
- 🎭 Adds time for `(beat)` pauses in dialogue (beat-aware timing)  
- 📄 Accepts screenplays as PDF files  
- 📤 CSV export with optional custom path  
- 🕒 Auto-names CSV reports using script name + timestamp  
- 🧪 Includes sample scripts and a test runner  

---

## 📦 Requirements

- Python 3.8+
- [`pdfplumber`](https://pypi.org/project/pdfplumber/)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the analyzer from the CLI:

```bash
python run_test.py path/to/your_script.pdf
```

Add `--export` to generate a CSV:

```bash
python run_test.py path/to/your_script.pdf --export
```

Use `--export-path` to choose a custom filename:

```bash
python run_test.py path/to/your_script.pdf --export --export-path my_output.csv
```

By default, CSV filenames include the script name and timestamp:

```
outputs/report_MyScript_20250814_143622.csv
```

---

Sample output:

```
Scene 1: INT. LIVING ROOM - NIGHT
  Dialogue: 23w  |  Action: 18w  |  Beats: 2
  ⏱ Estimated time: 41.3s

🎬 Total scenes analyzed: 6
⏳ Estimated total runtime: 4m 35s
📄 CSV report saved to outputs/report_MyScript_20250814_143622.csv
```

---

## 📁 Project Structure

```text
drameter/
├── drameter.py             # Core script parser and estimator
├── run_test.py             # CLI runner
├── requirements.txt
├── examples/
│   └── sample_script.pdf   # A short screenplay to test
```

---

## 🛠 Roadmap (Planned Features)

### 🎬 For Filmmakers & ADs
- [ ] Production-friendly CSV export (scene tags: INT/EXT, location, DAY/NIGHT)
- [ ] Auto-tagging of scenes (e.g. dialogue-heavy, action, silent)
- [ ] Support for scene length ranges (e.g. short, medium, long)
- [ ] Day-out-of-days-like summary (for shoot planning)

### 🧰 Tools & Interfaces
- [ ] CLI improvements (custom WPM, beat duration via flags)
- [ ] GUI or lightweight web version (Drag-and-drop PDF → breakdown)
- [ ] VS Code extension or local previewer

### 🧠 AI / Smart Analysis
- [ ] Tone/genre-aware pacing heuristics (e.g. drama vs comedy)
- [ ] Text-to-speech rhythm playback
- [ ] Pacing graph / emotional curve visualization

### 📄 Format Support
- [ ] Fountain `.fountain` parser
- [ ] Final Draft `.fdx` parser

---

## 🧠 Why “Drameter”?

Like a thermometer for drama. It doesn’t just count words. It measures rhythm, pacing, and pause.

---

## 🪪 License

MIT

---

## 👤 Author

**Madeline O'Leary**  
[github.com/madoleary](https://github.com/madoleary)
