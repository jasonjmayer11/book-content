# book-content
Short-form video pipeline for Jason Mayer's books. Reuses the dealcaddie-content engine.

- `books/*.json` one profile per book · `stories/*.json` one storyboard per video · `pages/<book>/` approved page images
- `python3 scripts/bookkit.py dist stories/*.json` builds mp4 + cover + caption + QA contact sheet
- Actions → **Build book reels** publishes each video as a prerelease. Builds never post.
- Actions → **Publish approved reel** (tag, schedule_at) posts via Upload-Post, only after approval.
- Secrets: `UPLOAD_POST_API_KEY` · Vars: `UPLOAD_POST_USER`, `POST_PLATFORMS`
