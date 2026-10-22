# Install Miso’s Garden Graph — Arcade Greenhouse

This **uses the real Shagshag/garden-graph engine**. The Action checks it out from GitHub and patches the `gardener()` function, retaining the existing isometric five-year landscape and its animations. It **does not use** the previous custom `scripts/grow_garden.py` flat renderer.

## One-time installation

1. Extract the ZIP. Upload **the contents of `miso-garden-graph/`** (not the parent folder) to the root of your public profile repo `haydencg93/haydencg93`.
2. Keep `.github/workflows/miso-garden.yml` and `scripts/` in place. Hidden `.github` folder must be uploaded as well.
3. **Remove or disable** the old `.github/workflows/update-garden.yml` / “Grow the contribution garden” workflow if it is still installed. It generates the old flat SVG, which this README no longer uses.
4. Under **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** (when offered). The new workflow also declares `contents: write`.
5. In **Actions**, select **Grow Miso's Garden Graph** and choose **Run workflow**. This downloads upstream Garden Graph, replaces its tiny farmer with a pixel frog, reads your contribution history and writes six SVG images into `assets/`.
6. Open your GitHub profile to view the updated garden. The README supports dark, light, and mobile views. All references get an updated content hash automatically each run.

## What updates

- GitHub Actions attempts two daily scheduled runs (GitHub schedules can be delayed or skipped).
- The original Garden Graph fetcher gathers GitHub contribution data, and the original renderer produces the full isometric multi-year garden, plus one-year and mobile views.
- The README embeds the **five-year isometric garden** on desktop, exactly matching the multi-year reference, and the readable one-year compact layout on mobile. The original renderer also produces single-year desktop views.
- Your regular GitHub contribution graph under the README remains unchanged.

## Optional private contributions

The upstream README explains that private contribution totals may require enabling “Private contributions” in GitHub profile settings and using a `GH_STATS_TOKEN` repository secret with `read:user`. The workflow uses `GH_STATS_TOKEN` if present, otherwise `GITHUB_TOKEN`.

## Customize

- **Miso artwork**: `scripts/patch_garden.py`, inside `gardener()`. Each character in the sprite grid is a drawn block.
- **Colors**: four seasonal palette replacements in `scripts/patch_garden.py`.
- **General profile content**: `README.md`.
- **Header and footer**: `assets/arcade-header.svg` and `assets/arcade-footer.svg` retained from the earlier Arcade Greenhouse artwork.

## Maintenance / transparency

The Action fetches the upstream repository at runtime. If a future upstream change renames or significantly alters the gardener function or seasonal palette, the patch intentionally fails instead of silently producing the wrong result. The original source is not bundled in this ZIP because this environment could not download GitHub source into the archive. The patch has been syntax-checked and run against a test fixture matching the published function signature and palette layout, but a complete production Actions run has **not** been verified here. Original project: https://github.com/Shagshag/garden-graph (MIT License).
