# sdlc-sample-python

Sample Python project for live checks of the SDLC framework plugin. It is a copy of the
framework's fixture project (`tests/fixtures/sample-python-project/` in
`luissiviero/sdlc-framework`): one module, one passing test, one test that fails only when
`SAMPLE_FAIL=1` is set, and a `.env` that the framework's `Read(.env*)` deny rule must keep
out of the model's context.

`.claude/settings.json` declares the plugin `sdlc@sdlc-framework`, so a Claude Code session
(local or cloud) installs it at startup. Then run `/sdlc:sdlc-init`.

- Test: `python -m pytest`
- Lint: `python -m ruff check .`
