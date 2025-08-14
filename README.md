# 🎬 Drameter

**Smart screenplay timing tool for filmmakers. Not marketers.**

Drameter estimates the runtime of a screenplay by analyzing its structure, dialogue, action, and pacing cues like `(beat)`. It’s built for screenwriters, directors, and editors who want a scene-by-scene breakdown of timing, not just a generic words-per-minute estimate.

I built this because I tend to write action-heavy scripts, which complicates time estimation. It's not perfect, but I do believe it's more accurate than the minute-per-page standard. I also found other online tools to be:  
1) Annoying,  
2) Geared towards people writing scripts for YouTube videos (no shade).

---

## ✨ Features

- 🗂️ Scene-by-scene analysis based on `INT.` / `EXT.` headings  
- 🗣️ Distinguishes between dialogue and action blocks  
- ⏱️ Estimates time using customizable words-per-minute  
- 🎭 Adds time for `(beat)` pauses in dialogue  
- 📄 Accepts screenplays as PDF files  
- 🧪 Includes sample scripts (a dumb one and a real one) and test runner  

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

```bash
python run_test.py examples/sample_script.pdf
```

You’ll get output like:

```
Scene 1:
{'scene_heading': 'INT. LIVING ROOM - NIGHT', 'dialogue_words': 23, 'action_words': 18, 'beats': 2, 'estimated_seconds': 41.3}

Scene 2:
{'scene_heading': 'EXT. CITY STREET - LATER', 'dialogue_words': 16, 'action_words': 12, 'beats': 1, 'estimated_seconds': 33.8}

Estimated total runtime: 1.25 minutes
```

---

## 📁 Project Structure

```
drameter/
├── drameter.py             # Core script parser and estimator
├── run_test.py             # Script to test with a sample screenplay
├── requirements.txt
├── examples/
│   └── sample_script.pdf   # A short screenplay to test
```

---

## 🛠 Roadmap (Planned Features)

- [ ] CSV export for timing breakdowns  
- [ ] CLI tool with options (e.g. WPM, beat duration)
- [ ] Lightweight web application  
- [ ] Text-to-speech playback (rhythm check)  
- [ ] Visual pacing graphs  
- [ ] Fountain / FDX format support  

---

## 🧠 Why “Drameter”?

Like a thermometer for drama.  It doesn’t just count words. It measures rhythm, pacing, and pause.

---

## 🪪 License

MIT — free to use, modify, or integrate in your workflow.

---

## 👤 Author

Madeline O'Leary
