# 🛠 Drameter — Development TODOs

Organized by priority and user value.

---

## ✅ Immediate Next Steps

- [ ] Add CLI flags for:
  - [ ] Custom WPM (`--wpm`)
  - [ ] Custom beat duration (`--beat-seconds`)
- [ ] Improve CSV output:
  - [ ] Include scene number
  - [ ] Include INT/EXT and DAY/NIGHT tags
  - [ ] Show words-per-page and time-per-page
- [ ] Add verbosity control:
  - [ ] Summary-only option for console output
  - [ ] `--ad-mode` for stripped-down AD-friendly view

---

## 🧪 Medium-Term Goals

- [ ] Support `.fountain` screenplay files
- [ ] Support `.fdx` (Final Draft) files
- [ ] Auto-tag scenes:
  - [ ] Dialogue-heavy
  - [ ] Action-heavy
  - [ ] Silent
- [ ] Label scene durations:
  - [ ] Short (< 30s)
  - [ ] Medium (30s–2m)
  - [ ] Long (> 2m)

---

## 🎛️ Long-Term / Stretch Goals

- [ ] Visual pacing graph (timeline curve)
- [ ] Text-to-speech playback for rhythm testing
- [ ] AI tone/genre-aware modifiers
- [ ] Lightweight web GUI or drag-and-drop app
- [ ] VS Code extension (timing shown inline)

---

## 🎬 AD-Focused Enhancements

- [ ] Export summary per scene:
  - [ ] Time estimate
  - [ ] Length label
  - [ ] Complexity warning (long action or beats)
- [ ] Integrate with stripboard-style templates
- [ ] Generate "day-out-of-days" style summary
