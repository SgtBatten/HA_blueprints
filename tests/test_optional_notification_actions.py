"""Exercise optional actions with real HA validation/rendering and Spook extraction."""

import ast
import asyncio
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.request import urlopen

import pytest
import yaml
from homeassistant import const
from homeassistant.config_entries import ConfigEntries
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ServiceNotFound
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import service, template
from homeassistant.helpers.script import Script

ROOT = Path(__file__).resolve().parents[1]
SPOOK_REF = "4bee6e1561bb957eddee415159a18cc04de2d43c"
SPOOK_URL = (
    f"https://raw.githubusercontent.com/frenck/spook/{SPOOK_REF}/"
    "custom_components/spook/entity_filtering.py"
)
EXPECTED = Counter(
    {
        "telegram_bot.send_photo": 6,
        "telegram_bot.send_video": 2,
        "nfandroidtv.send_message": 3,
    }
)


class BlueprintLoader(yaml.SafeLoader):
    """Keep input references distinct until blueprint substitution."""


class Input(str):
    """A blueprint input reference."""


BlueprintLoader.add_constructor(
    "!input", lambda loader, node: Input(loader.construct_scalar(node))
)


def walk(value):
    """Walk mappings, including every nested notification branch."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def blueprint(name):
    raw = yaml.load(
        (ROOT / "Frigate_Camera_Notifications" / name).read_text(),
        Loader=BlueprintLoader,
    )
    defaults = {}
    for mapping in walk(raw["blueprint"]["input"]):
        defaults.update(
            {
                key: value["default"]
                for key, value in mapping.items()
                if isinstance(value, dict) and "default" in value
            }
        )
    # This test device only needs to satisfy script schema validation; no device runs.
    defaults["notify_device"] = "0123456789abcdef0123456789abcdef"

    def substitute(value):
        if isinstance(value, Input):
            return deepcopy(defaults[value])
        if isinstance(value, dict):
            return {key: substitute(child) for key, child in value.items()}
        if isinstance(value, list):
            return [substitute(child) for child in value]
        return value

    return substitute(raw["actions"])


@pytest.fixture(scope="session")
def spook():
    """Execute pinned upstream functions, not a reimplementation of its walker.

    AST isolation avoids importing Spook's unrelated integrations. The functions
    retain their real HA constants, action classifier and Template objects.
    """
    source = urlopen(SPOOK_URL, timeout=30).read().decode()
    names = {
        "async_find_services_in_sequence",
        "async_filter_known_services",
        "async_get_all_services",
        "async_get_disabled_integrations",
    }
    tree = ast.parse(source)
    tree.body = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in names
    ]
    assert {node.name for node in tree.body} == names
    namespace = {
        key: getattr(const, key) for key in dir(const) if key.startswith("CONF_")
    }
    namespace.update(cv=cv, callback=callback)
    # Explicit future flag keeps upstream type annotations unevaluated.
    import __future__

    exec(  # noqa: S102 - execute only named functions from the pinned upstream source
        compile(tree, SPOOK_URL, "exec", flags=__future__.annotations.compiler_flag),
        namespace,
    )
    return namespace


@pytest.mark.parametrize("name", ["Beta.yaml"])
def test_optional_actions_not_reported_when_integrations_absent(name, spook, tmp_path):
    async def check():
        hass = HomeAssistant(str(tmp_path))
        hass.config_entries = ConfigEntries(hass, {})
        sequence = cv.SCRIPT_SCHEMA(blueprint(name))
        services = spook["async_find_services_in_sequence"](sequence)
        unknown = spook["async_filter_known_services"](
            hass, services=services, known_services=set()
        )
        assert not (set(EXPECTED) & unknown), (
            f"Optional actions reported: {sorted(set(EXPECTED) & unknown)}"
        )
        # Do not hide ordinary static missing services as a side effect.
        assert "automation.turn_off" in unknown

    asyncio.run(check())


@pytest.mark.parametrize("name", ["Beta.yaml"])
def test_enabled_actions_dispatch_original_services_and_payloads(name, tmp_path):
    async def check():
        hass = HomeAssistant(str(tmp_path))
        calls = []

        async def record(call):
            calls.append((call.domain, call.service, dict(call.data)))

        for action in EXPECTED:
            domain, action_name = action.split(".")
            hass.services.async_register(domain, action_name, record)

        variables = {
            "telegram_config_entry": "test_bot",
            "telegram_chat_id": 123,
            "message": "A Person was detected.",
            "title": "Front Door",
            "attachment": "https://example.test/snapshot.jpg",
            "base_url": "https://example.test",
            "telegram_base_url": "http://frigate.test",
            "video": "https://example.test/clip.mp4",
            "id": "test-event",
            "tv_entities": ["notify.test_tv"],
            "tv_image": "media-source://image/image.front_person",
            "tv_size": "medium",
            "tv_position": "top-right",
            "tv_duration": 10,
            "tv_transparency": "50%",
            "tv_interrupt": False,
            "button_1": "View Clip",
            "button_2": "View Snapshot",
            "button_3": "Silence",
            "url_1": "/clip",
            "url_2": "/snapshot",
            "url_3": "silence-test",
            "this": {"entity_id": "automation.test"},
            "camera": "front",
            "client_id": "frigate",
        }
        found = Counter()
        for step in walk(blueprint(name)):
            value = step.get("action")
            if not isinstance(value, str):
                continue
            original = template.Template(value, hass).async_render(variables)
            if original not in EXPECTED:
                continue
            found[original] += 1
            validated = cv.SERVICE_SCHEMA(deepcopy(step))
            params = service.async_prepare_call_from_config(hass, validated, variables)
            literal = deepcopy(step)
            literal["action"] = original
            literal = cv.SERVICE_SCHEMA(literal)
            expected = service.async_prepare_call_from_config(hass, literal, variables)
            assert params == expected
            assert f"{params['domain']}.{params['service']}" == original
            script = Script(
                hass, [validated], "optional action regression", "automation"
            )
            await script.async_run(variables)
            assert calls[-1][:2] == tuple(original.split("."))
            assert calls[-1][2] == {
                **expected["service_data"],
                **expected.get("target", {}),
            }
            # Selecting an absent integration must still fail at runtime,
            # including the TV steps' existing continue_on_error: true.
            hass.services.async_remove(params["domain"], params["service"])
            with pytest.raises(ServiceNotFound):
                await script.async_run(variables)
            hass.services.async_register(params["domain"], params["service"], record)
        assert found == EXPECTED
        assert len(calls) == sum(EXPECTED.values())

        # Run each real initial/GenAI/update router, not a simulated choose.
        routers = [
            step
            for step in walk(blueprint(name))
            if isinstance(step.get("choose"), list)
            and step["choose"][0].get("conditions") == "{{ telegram }}"
        ]
        assert len(routers) == 3
        hass.services.async_register("notify", "test_mobile", record)
        variables.update(
            notify_group_target="test_mobile",
            alert_once=False,
            critical=False,
            sound="default",
            volume=1,
            attachment_type="",
            ios_live_view=False,
            camera_name="front",
            channel="",
            color="red",
            icon="mdi:cctv",
            tag="event",
            group="frigate",
            subtitle="",
            sticky=False,
            ttl=0,
            priority="high",
            timeout=30,
            importance="default",
            tap_action="/clip",
            android_auto=False,
            loitering=False,
        )
        for index, router in enumerate(routers):
            for channel, end, bot in [
                ("telegram", False, ""),
                ("telegram", False, "test_bot"),
                ("telegram", True, ""),
                ("telegram", True, "test_bot"),
                ("tv", False, ""),
                ("mobile", False, ""),
            ]:
                variables.update(
                    telegram=channel == "telegram",
                    tv=channel == "tv",
                    telegram_config_entry=bot,
                    event={"type": "end" if end else "update"},
                )
                # For mobile, neither optional integration is present at all.
                if channel == "mobile":
                    for action in EXPECTED:
                        domain, action_name = action.split(".")
                        hass.services.async_remove(domain, action_name)
                before = len(calls)
                script = Script(
                    hass,
                    cv.SCRIPT_SCHEMA([deepcopy(router)]),
                    "notification router",
                    "automation",
                )
                await script.async_run(variables)
                assert len(calls) == before + 1
                expected_action = (
                    "telegram_bot.send_video"
                    if channel == "telegram" and end and index == 2
                    else "telegram_bot.send_photo"
                    if channel == "telegram"
                    else "nfandroidtv.send_message"
                    if channel == "tv"
                    else "notify.test_mobile"
                )
                assert ".".join(calls[-1][:2]) == expected_action
                if channel == "telegram":
                    assert calls[-1][2].get("config_entry_id", "") == bot
                    assert calls[-1][2]["parse_mode"] == "plain_text"
                if channel == "mobile":
                    for action in EXPECTED:
                        domain, action_name = action.split(".")
                        hass.services.async_register(domain, action_name, record)

    asyncio.run(check())
