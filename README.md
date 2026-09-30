# sdlc-sample-python

Sample Python project for live checks of the SDLC framework plugin. It is a copy of the
framework's fixture project (`tests/fixtures/sample-python-project/` in
`luissiviero/sdlc-framework`), grown by the changes under `changes/`: one module
(`sample_pkg/calc.py`: `add`, `divide`, `percent`, `mean`), its behaviour tests, one test that
fails only when `SAMPLE_FAIL=1` is set, and a `.env` that the framework's `Read(.env*)` deny
rule must keep out of the model's context.

`.claude/settings.json` declares the plugin `sdlc@sdlc-framework`, so a Claude Code session
(local or cloud) installs it at startup. Then run `/sdlc:sdlc-init`.

- Build: `python -m compileall -q .`
- Test: `python -m pytest`
- Lint: `python -m ruff check .`

`main` is protected: every change, the owner's own guardrail edits (`CLAUDE.md`, `REVIEW.md`,
`sdlc.yaml`, `.claude/**`) included, reaches it through a pull request.
