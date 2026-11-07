# Optional notification action regression

Run with Python 3.14 and Home Assistant 2026.11.0:

```sh
uv venv .venv
uv pip install --python .venv/bin/python homeassistant==2026.11.0 PyYAML pytest
.venv/bin/python -m pytest -q tests/test_optional_notification_actions.py
```

The test downloads `entity_filtering.py` from Spook commit
`4bee6e1561bb957eddee415159a18cc04de2d43c` (network access required).
It executes only the four named upstream extraction/filter functions, with
real Home Assistant script validation, constants and template objects. It does
not substitute a hand-written scanner or scan raw YAML strings.

Both active blueprints are checked for:

- No missing optional Telegram/Android TV actions after HA script validation,
  while an ordinary missing static action remains detectable.
- All six photo, two video and three TV action sites render and dispatch the
  same action names and payloads as their literal-action equivalents.
- Real HA script execution still raises `ServiceNotFound` if a selected action
  is missing (including TV's existing `continue_on_error: true`).
- Initial, GenAI and update routing with Telegram enabled (with/without a bot
  entry, photo/video), TV enabled, and mobile notify-group fallback with both
  optional integrations absent.

Dispatch is to in-memory test services, not Telegram, TVs or a live HA server.
This does not test delivery over those integrations' networks.

## Why template constant action names?

[Spook's automation repair](https://github.com/frenck/spook/blob/4bee6e1561bb957eddee415159a18cc04de2d43c/custom_components/spook/ectoplasms/automation/repairs/unknown_service_references.py#L50-L56)
scans the validated `action_script.sequence`.
[Its walker](https://github.com/frenck/spook/blob/4bee6e1561bb957eddee415159a18cc04de2d43c/custom_components/spook/entity_filtering.py#L860-L920)
visits all choose branches, without evaluating their conditions;
[the filter](https://github.com/frenck/spook/blob/4bee6e1561bb957eddee415159a18cc04de2d43c/custom_components/spook/entity_filtering.py#L782-L804)
only reports string action names. HA validation turns templated action names
into `Template` objects; HA resolves them when the selected branch runs.

This deliberately gives up static missing-action detection at these optional
call sites even when that channel is selected. It does not silently skip
missing integrations, add `has_service` guards, or change runtime error handling.
Telegram/TV selection, payloads and mobile fallback remain unchanged.
