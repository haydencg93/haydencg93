# Install Hayden // Arcade Greenhouse

1. Download and unzip the package.
2. In GitHub, open your public profile repository **haydencg93/haydencg93** (the username repository). Create it if necessary.
3. Upload `README.md`, `assets/`, `scripts/`, and `.github/workflows/update-garden.yml` keeping the folder layout. **Commit to your default branch.**
4. Go to repository **Settings → Actions → General → Workflow permissions** and allow **Read and write permissions**, if your repository settings permit it. The workflow also requests `contents: write`.
5. Go to **Actions → Grow the contribution garden → Run workflow**. It fetches the GitHub GraphQL contribution calendar for the repository owner and replaces the DEMO artwork with your real 26-week graph. Then it refreshes daily (UTC).
6. View your GitHub profile and verify the banner, garden and footer are loading.

## Notes
- The README is the real product. This ZIP's large mockup image is **not** a screenshot of your live GitHub and is not embedded.
- Your first bundled garden artwork says `SAMPLE ACTIVITY`; it does not represent your real activity until the workflow completes successfully.
- GitHub does **not** support free-floating widgets over its whole page or README JavaScript. The frog/cloud float *inside SVG banners only*; the native GitHub contributions graph remains unchanged.
- Some GitHub image renderers and reduced-motion settings may display the first frame of an SVG without animation. The art remains visible.
- For a quick local demo run `python scripts/grow_garden.py --demo`. To generate the real garden locally, set `GH_USERNAME=haydencg93` and a token with access to GitHub's contribution calendar as `GH_TOKEN`.
- The included design is deliberately 26 weeks to leave enough room for readable pixel sprouts. Private activity may depend on your profile contribution visibility settings.
- All the generated SVG assets are local to this repository. No third-party stat card server is required.
- The mockup of an entire GitHub site cannot be applied directly: sidebar, navigation, native pinned cards, and native contribution calendar remain under GitHub's control.

## Customize
- Text and project links: edit `README.md`.
- Header and mascot pixels: `scripts/pixel_art.py`, then run `python scripts/pixel_art.py`.
- Contribution grid, tile sprites and palette: `scripts/grow_garden.py`.
- Palette: `#F3F0E7`, `#A7B69C`, `#677D69`, `#34483B`, `#292F2B` plus deep arcade green `#182521`.
