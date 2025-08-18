# 🎬 Drameter

**Smart screenplay timing tool for filmmakers. Not marketers.**

Drameter estimates the runtime of a screenplay by analyzing its structure, dialogue, action, and pacing cues like `(beat)`. It’s built for screenwriters, directors, and editors who want a scene-by-scene breakdown of timing, as opposed to a generic words-per-minute estimate.

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
- [x] Production-friendly CSV export (scene tags: INT/EXT, location, DAY/NIGHT)
- [ ] Auto-tagging of scenes (e.g. dialogue-heavy, action, silent)
- [ ] Support for scene length ranges (e.g. short, medium, long)
- [ ] Day-out-of-days-like summary (for shoot planning)

### 🧰 Tools & Interfaces
- [x] CLI improvements (custom WPM, beat duration via flags)
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

## 🤔 What This Tool *Is* — and *Isn’t*

Let's be clear: the actual timing of a scene is ultimately determined by the director, the actors’ performances, the editor’s cuts, and the rhythm of the final film. No one likes long shots and slow, pregnant dialogue more than me. Drameter is absolutely not intended to flatten these artistic decisions in the name of "efficiency".

So, is a tool like Drameter presumptuous?

💡 I hope not, so I strive to position it correctly.

---

✅ **Think of Drameter as:**

🛠 A pre-creative planning tool

It gives writers, directors, and editors a first-pass estimate. That is, a starting point for discussing and shaping rhythm.  
Like a table read for your structure.

It’s not claiming:

> “Your scene will last exactly 42.3 seconds.”

It’s saying:

> “Given your structure, this scene reads like a ~40-second moment, unless you make it longer or shorter in performance.”

---

🎬 **Real-world analogy**

Storyboards don’t dictate camera angles. They suggest them.  
Beat sheets don’t define tone. They scaffold it.  
Drameter doesn’t replace a director. It informs them with baseline data.

---

🎯 **Who actually benefits from Drameter?**
- Writers wondering: “Is this third act bloated? Is there redundancy between action and dialogue?”
- Directors prepping a shoot with limited days
- Editors checking if a film’s rhythm has unexpected dead zones
- Producers estimating page count to screen time
- Anyone doing a first table read or animated pre-vis

---

## 🎬 Why Drameter Is Valuable to Assistant Directors

⏱ **1. Helps with Scheduling**

ADs often need to:
- Break the script into scenes
- Estimate how long each will take to shoot
- Create shooting schedules and call sheets

Drameter gives them:
- A first-pass runtime estimate per scene
- Faster script breakdowns without having to eyeball every line
- Insight into pace-heavy vs. dialogue-heavy scenes, which affect setup times, blocking complexity, and performance rhythm

Think of it as a “pre-breakdown timing assistant” for ADs prepping a stripboard.

---

🧮 **2. Assists with Day-Out-of-Days and Shooting Ratios**

If a film is aiming for 8 pages/day or 5 minutes of screen time/day, Drameter gives a clearer view of what that means.

Scene 14 may be one page but run 90 seconds because of long beats and dense action. That extra 30 seconds adds up fast, considering an excess of three minutes could necessitate another whole shooting day!

---

⚠️ **3. Flags Complex Scenes Early**

Scenes with lots of action, long beats, or high word counts per page may require more shoot time, even if they’re short on paper.

Drameter gives early warning signs.

---

✅ **Drameter Helps ADs Answer:**
- How many scenes can we realistically shoot today?
- Is this scene more complicated than it looks?
- Do we need to budget more time for certain blocks?
- Is the script consistent in pacing across acts?

---

## 👥 Who Is This For?

🎬 Screenwriters, to better understand scene pacing  
🎭 Directors, to assess emotional rhythm  
🗂 Assistant Directors, to aid in pre-scheduling and stripboarding  
🎞 Editors, to forecast cuts and dead zones  
📈 Producers, to predict total runtime beyond page count

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
