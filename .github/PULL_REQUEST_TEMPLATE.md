## What this changes

<!-- One or two lines. If it closes an issue, say "Closes #N". -->

## If you added or changed a detection pattern

Both tests are required. The second one is the one that gets forgotten, and it is
the one that keeps the scanner usable.

- [ ] A test showing the pattern **is** caught
- [ ] A test showing it does **not** fire on human writing
- [ ] Checked the new pattern against `examples/human-baseline.md` and the scores did not move

## Checks

- [ ] `python3 -m unittest discover tests -v` passes
- [ ] Scores are still deterministic (same input, same score, every run)
- [ ] No new dependencies. The scanner is stdlib-only on purpose.

## Notes

<!-- Anything you are unsure about, or a judgment call you want a second opinion on. -->
