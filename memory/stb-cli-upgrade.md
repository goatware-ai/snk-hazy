---
name: stb-cli-upgrade
description: stb version-gates itself; when a command errors as outdated, upgrade with uv tool upgrade snorkelai-stb from the Snorkel wheel index
metadata:
  type: reference
---

The `stb` CLI refuses to run once a newer release ships. Every command, not just the one being run, fails with:

```
Error: Version 2.4.8 is outdated (latest: 2.4.9).
Please upgrade before continuing:
```

Fix:

```bash
uv tool upgrade snorkelai-stb \
  --find-links https://snorkel-python-wheels.s3.us-west-2.amazonaws.com/stb/index.html \
  --python ">=3.12"
```

**Why:** the error looks like a data or auth problem but is neither, and the upgrade needs the Snorkel S3 wheel index plus the `>=3.12` pin, so a plain `uv tool upgrade snorkelai-stb` is not enough.

**How to apply:** treat an outdated-version error as a prerequisite, not a failure. Upgrade, then re-run the original command. `.claude/skills/fetch-status/fetch_status.py` detects this text and prints the upgrade command instead of leaving a bare CLI error. `stb` lives at `~/.local/bin/stb`; it was at 2.4.9 on 2026-08-20. See [[submission-tracking]].
