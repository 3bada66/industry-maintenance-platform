# Video Submission Instructions
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)
**Supporting:** Hamdi Alnaqeeb (DevOps/Operations, 2309116178) · Praise-God Tobby (QA/Test Engineer, 2309116418)

---

## 1. What to Submit

The team records a **7-minute video presentation** of the project and submits **only the link**. Do not submit the video file directly — file attachments are large, may be rejected by the submission system, and cannot be easily shared with the instructor after the fact.

| What | Specification |
|------|--------------|
| Duration | 7 minutes ± 30 seconds |
| Content | Follows `docs/presentation-outline.md` exactly — 7 slides, same order |
| Format | Screen recording with voice narration; webcam is optional |
| Language | English throughout |
| Link | YouTube, Google Drive, Vimeo, or OneDrive — see §4 for options |
| Submission | Paste the link into the course submission form or email it to the instructor |

---

## 2. Pre-Recording Checklist

Complete every item before pressing record. A failed environment cannot be fixed mid-recording.

**System setup (Hamdi — DevOps):**
- [ ] Run `make prod` on the recording machine
- [ ] Wait 90 seconds for all containers to initialise
- [ ] Run `make status` — all containers must show `Up (healthy)`
- [ ] Open `https://localhost` in the browser — login page must load
- [ ] Login with `admin@example.com` / `admin123` — main dashboard must load
- [ ] Navigate to `/monitoring` — confirm green "HEALTHY" status banner
- [ ] Navigate to `/management` — confirm KPI tiles load and data appears
- [ ] Navigate to `/risk` — confirm risk KPI tiles load
- [ ] Run `make demo` if the database is empty (loads 8 assets, 3 sites, full network topology)

**Slides (Fares — UX/UI Designer):**
- [ ] All 7 slides reviewed for visual consistency
- [ ] Screenshots from the live dashboards inserted into Slides 3 and 4
- [ ] Architecture diagram on Slide 2 matches `docs/software-design-analysis.md`

**Recording equipment (Hamdi — DevOps):**
- [ ] Screen recording software tested with a short clip
- [ ] Microphone tested — voice is clear; no background noise
- [ ] Browser zoom at 100 % — dashboard text must be readable at 1080p
- [ ] No notifications, pop-ups, or personal content visible on screen

**Speakers (all):**
- [ ] Each speaker has read their script from `docs/presentation-outline.md`
- [ ] Full timed rehearsal completed — total must be ≤ 7:00
- [ ] Each speaker knows their handoff cue to the next speaker

---

## 3. Recording Instructions

### 3.1 Recording Software Options

| Software | Platform | Cost | Notes |
|----------|---------|------|-------|
| **OBS Studio** | Windows / Mac / Linux | Free | Best quality; requires initial setup |
| **Windows Game Bar** | Windows 10/11 | Built-in | `Win + G` → Record |
| **macOS QuickTime** | macOS | Built-in | File → New Screen Recording |
| **Zoom** | Any | Free | Start a solo meeting, share screen, record locally |
| **Google Meet** | Browser | Free | Share screen; record to Google Drive |
| **Loom** | Browser extension | Free (5 min on free tier) | Uploads automatically; easy to share |

### 3.2 Step-by-Step with OBS Studio (Recommended)

1. Download OBS Studio from obsproject.com (free, no account needed)
2. Sources → Add → **Display Capture** (captures your screen)
3. Sources → Add → **Audio Input Capture** (captures your microphone)
4. Settings → Output → set Recording Path to your desktop folder
5. Settings → Video → Base Resolution: 1920×1080 · FPS: 30
6. Click **Start Recording**
7. Switch to slides or the live Industry Maintenance Platform dashboard
8. Speak clearly, following the `presentation-outline.md` script
9. Click **Stop Recording** at 7:00
10. Rename the output file to `industry-maintenance-platform-presentation.mkv` or `.mp4`

### 3.3 Step-by-Step with Zoom

1. Open Zoom → New Meeting (camera optional)
2. Click **Share Screen** → select your desktop or browser window
3. Click **Record → Record on this Computer**
4. Present all 7 slides following `presentation-outline.md`
5. Click **Stop Recording** → End Meeting → Zoom converts the file automatically
6. Locate the `.mp4` in `~/Documents/Zoom/`

### 3.4 Live Dashboard Demo (Slides 3–4)

For Slides 3 and 4, speakers may switch from slides to the live browser:

- **Slide 3 (Management):** open `https://localhost/management` — show KPI tiles, sprint velocity bars, team workload table
- **Slide 4 (Technical):** open `https://localhost/monitoring` — show status banner, system resources, alert thresholds table

Allow 30–60 seconds per live demo and count this in the total rehearsal time. If the live system is unavailable on recording day, use dashboard screenshots instead — the presentation content does not change.

---

## 4. Upload and Sharing Instructions

Upload the recording to one of the following platforms and configure sharing so the instructor can view it without a login or account.

### Option A — YouTube (Recommended)

1. Sign in to [youtube.com](https://youtube.com) with a Google account
2. Click the camera + icon → **Upload Video** → select the recorded file
3. Title: `Industry Maintenance Platform — Industrial Monitoring Platform — SPM Course Presentation`
4. Visibility: **Unlisted** — anyone with the link can view; does not appear in YouTube search
5. Click **Publish**
6. Copy the link from the address bar: `https://youtu.be/XXXXXXXXXX`
7. Verify: open the link in a private/incognito window — video must play without login

**Why YouTube:** no account required to view an unlisted video; link works on any device; the instructor can watch at any time without an account.

### Option B — Google Drive

1. Sign in to [drive.google.com](https://drive.google.com)
2. Click **New → File upload** → select the video file → wait for upload
3. Right-click the file → **Share**
4. Under "General access" → **Anyone with the link** → role: **Viewer**
5. Click **Copy link**
6. Verify: open the link in a private window — video must play without login

### Option C — Vimeo

1. Create a free account at [vimeo.com](https://vimeo.com)
2. Click **New video → Upload** → select the file
3. Privacy setting: **Anyone with a link**
4. Copy the video URL
5. Verify in a private window before submitting

### Option D — OneDrive

1. Open your university OneDrive or [onedrive.live.com](https://onedrive.live.com)
2. Upload the video file
3. Right-click → **Share → Anyone with the link can view**
4. Copy and submit the link
5. Verify in a private window before submitting

---

## 5. Submission

### 5.1 Submit Only the Link

Submit exactly **one link**. Nothing else.

```
Example: https://youtu.be/XXXXXXXXXX
```

Do not submit:
- The video file (too large; may be rejected by the course system)
- A zip or compressed archive
- The slide deck alone (without the video)
- Multiple links from different platforms

### 5.2 Where to Submit

Use the method the course specifies:

- **Course portal:** paste the link into the video submission text field
- **Email:** send to the instructor with subject line: `[SPM Course] Industry Maintenance Platform Video Presentation — Team Obada`
- **Repository:** create `SUBMISSION.md` at the repo root with the link and submission date

### 5.3 Deadline

Submit the link **before the course deadline**. The video must be accessible at the time of submission. Do not delete the video or change the sharing settings after submitting — the instructor may return to review it at any point.

---

## 6. Verification Before Submitting

Run through this final check before submitting the link:

- [ ] Open the link in a **private/incognito browser window** — confirms it works without login
- [ ] Video plays from the beginning without error or buffering
- [ ] All 7 speakers are clearly audible
- [ ] Slides and/or live dashboard are visible on screen throughout
- [ ] Total duration is between 6:30 and 7:30
- [ ] The 7-slide structure from `docs/presentation-outline.md` is followed in order
- [ ] No sensitive personal information is visible (passwords, private files, personal URLs)

If any check fails, fix the issue and re-verify before submitting.

---

## 7. Presentation and Video Alignment

The video must follow the exact structure of `docs/presentation-outline.md`. The instructor evaluates the video against the same criteria as a live presentation.

| Slide | Topic | Speaker | Duration |
|-------|-------|---------|---------|
| 1 | Problem and Project Idea | Obada | 1:00 |
| 2 | System Overview and Architecture | Mohanad | 1:00 |
| 3 | Management Monitoring | Obada | 1:00 |
| 4 | Technical Monitoring | Mohanad + Hamdi | 1:30 |
| 5 | Risk, Stakeholders, and Value | Abdulaziz | 1:00 |
| 6 | CI/CD, Testing, and Course Concepts | Hamdi + Praise-God | 0:30 |
| 7 | Conclusion | Obada | 1:00 |
| **Total** | | | **7:00** |

The key points and speaker notes for each slide are in `docs/presentation-outline.md`. Speakers should follow their written notes — not improvise — to stay within the time budget.

---

## 8. Troubleshooting

| Problem | Solution |
|---------|---------|
| Live dashboard not loading | Run `make status`; if containers are not healthy, run `make stop && make prod` and wait 90 seconds |
| `make prod` fails | Check Docker is running; check port 443 is free; see `docs/ci-cd-testing.md §3.3` for rollback procedure |
| Recording has no audio | Check microphone permissions in OS settings; test with a 10-second clip before the full recording |
| Video file too large to upload | Compress with HandBrake (free, handbrake.fr): `H.264, RF 23, 1080p` reduces most files under 500 MB |
| YouTube "still processing" | Wait 15–30 minutes after upload; do not submit the link until processing shows "Done" |
| Google Drive link requires login | Re-open Sharing settings; confirm "Anyone with the link" is selected, not "Restricted" |
| Total recording is over 7:30 | Tighten Slides 5 or 6 — they have the most compression room; do not cut Slide 1 or 7 |
| Speaker not clearly audible | Re-record in a quieter room; use a headset microphone rather than a laptop built-in mic |
| Slide not visible on recording | Confirm the recording software is capturing the correct screen/window before recording begins |
