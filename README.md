# ericreier.com

The source for ericreier.com. Change a file here and the site republishes itself in about a minute.

## What's where

| File | What it controls |
| --- | --- |
| `content.toml` | All the words: reel blurb, projects, About, resume, email, LinkedIn |
| `img/` | Thumbnails. Each project's picture is `img/<key>.jpg`. Reel still is `img/reel.jpg`, About photo is `img/headshot.jpg` |
| `template.html` | The design, plus the big headlines on each page |
| `build.py` | Turns the two files above into the site. You shouldn't need to touch it |

## Edit with the form editor (easiest)

1. Go to [app.pagescms.org](https://app.pagescms.org) and sign in with GitHub (first time only: allow it access to the `mancashew.github.io` repo).
2. Open **mancashew.github.io > Website**. Every piece of text, link and picture is a form field. Drag projects to reorder them, use **Add** for a new one, and click a picture to upload a new one.
3. Click **Save**. The site is live about a minute later.

Pages CMS rewrites `content.toml` when it saves, so the comments in that file disappear. That's fine.

## Edit the file on GitHub

1. Open [content.toml on GitHub](https://github.com/ManCashew/mancashew.github.io/blob/main/content.toml) and click the pencil.
2. Change the text between the quotes.
3. Click **Commit changes**.
4. Wait about a minute. Progress shows on the [Actions tab](https://github.com/ManCashew/mancashew.github.io/actions). Green check means it's live. A red X means there's a typo; click it to see which line, and the old site stays up until it's fixed.

To swap a thumbnail, open the `img` folder on GitHub, **Add file > Upload files**, and upload a JPG with the same name.

## Edit on your Mac

The folder is `~/website/ericreier.com`.

1. Edit `content.toml` in any text editor (TextEdit works, set it to plain text).
2. Double-click `preview.command` to see it at http://localhost:8000.
3. Double-click `publish.command` to put it live.

If you edited on GitHub too, `publish.command` pulls those changes first.

## Common jobs

- **Reorder projects**: move the whole `[[projects]]` block up or down. The first six also show on the Reel page.
- **Add a project**: copy a `[[projects]]` block, give it a new `key` and `slug`, and add `img/<key>.jpg`. The Vimeo `player_url` is the link from Vimeo's Share > Embed, the `https://player.vimeo.com/video/...` part.
- **Remove a project**: delete its block. Its old link then shows the "page not found" page, so think twice if you've sent that link to anyone.
- **Never change an existing `slug`.** Old links in applications point at them.

## Text rules

- Long text sits between `"""` triple quotes and can run over several lines.
- Short text uses `"` quotes. To put a quote mark inside, use `\"` or switch to triple quotes.
