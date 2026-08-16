# Before you publish — what still needs real content

The generator (`build.py`) refused to invent any of these, on purpose — a
portfolio with even one fabricated detail is a liability the moment someone
asks about it in an interview. Everything below is marked `[FILL]` directly
in the generated HTML too, so you'll see it in the browser if you skip this.

## 1. GitHub repo links (5 places)
Each project page (`projects/*.html`) has a "View on GitHub" button pointing
at a placeholder URL. Open `build.py`, find the `PROJECTS` list near the top,
and replace each `github` field with the real repo URL. Re-run
`python3 build.py` after editing — it regenerates every page from this one
list, so you only edit the data once.

## 2. Resume PDF
Drop your current resume as `assets/resume.pdf`. The embed and download
button on `resume.html` already point there — nothing else to wire up.

## 3. Photo
`about.html` has a dashed placeholder box where a real photo should go.
Add an image to `assets/` and swap the placeholder `<div class="avatar-box">`
for an `<img>` tag pointing at it (in `build_about()` inside `build.py`, then
re-run the generator).

## 4. Writing page
Both entries on `writing.html` are placeholders for the RAG project writeup
and the "why I evaluate before I model" piece discussed earlier. Publish the
posts wherever you're writing them (Medium, a static blog, this same site),
then update the `build_writing()` function in `build.py` with real dates,
summaries, and links.

## 5. Contact — optional scheduling link
If you're actively interviewing, consider adding a Calendly (or similar)
link on `contact.html` — it saves a recruiter an email round-trip. Purely
optional; the page works fine without it.

---

## Deploying

No build step required after `python3 build.py` has run once — the output
is plain static HTML/CSS/JS. Fastest paths:

**Netlify / Vercel (drag-and-drop):** drag this whole folder onto
netlify.com/drop, or run `vercel` from inside this folder if you have the
Vercel CLI installed. Either gives you a live URL in under a minute.

**GitHub Pages:** push this folder to a repo, enable Pages in repo settings,
point it at the root of the `main` branch (or a `docs/` folder if you prefer
to nest it inside an existing repo).

Either way — re-run `python3 build.py` locally after any content edit, then
redeploy the regenerated files. The Python script is a convenience for
editing consistently across all 11 pages; it is not a runtime dependency of
the deployed site.
