# MigaBuilder videos

Narrated explanation videos (`<tool>.mp4`) and poster images (`<tool>.jpg`) for
every tool on [migabuilder.com](https://migabuilder.com/), served from
`https://videos.migabuilder.com/` by the `migabuilder-videos` Cloudflare Worker
(`wrangler.jsonc`, `worker.js`), which deploys automatically on every push to
`main`. `worker.js` only adds Range support so videos can be skipped through
and play in Safari; everything else is served as plain static files.

The site itself, the recording script and `videos/manifest.json` (titles,
transcripts and links to these files) live in
[makmurphy69-cpu/migabuilder](https://github.com/makmurphy69-cpu/migabuilder).
Videos are recorded there with `node scripts/tutorial-videos/record.mjs <tool>`,
which writes them into a clone of this repository next to it.
