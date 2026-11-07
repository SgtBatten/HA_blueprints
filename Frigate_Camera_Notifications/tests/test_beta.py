"""Static and rendering checks; run with Python, PyYAML and Jinja2 installed."""
from pathlib import Path
import json
import unittest

import yaml
from jinja2 import Environment, nodes
from jinja2.nativetypes import NativeEnvironment

BLUEPRINT = Path(__file__).resolve().parents[1] / 'Beta.yaml'


class BlueprintLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key {key!r} at {key_node.start_mark}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


BlueprintLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
BlueprintLoader.add_constructor('!input', lambda loader, node: {'input': loader.construct_scalar(node)})


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


class BetaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = BLUEPRINT.read_text(encoding='utf-8')
        cls.blueprint = yaml.load(cls.source, Loader=BlueprintLoader)
        cls.environment = NativeEnvironment()
        cls.inputs = {}
        for name, field in cls.blueprint['blueprint']['input'].items():
            cls.inputs.update(field['input'] if 'input' in field else {name: field})

    def test_input_references(self):
        for value in walk(self.blueprint):
            if isinstance(value, dict) and list(value) == ['input']:
                self.assertIn(value['input'], self.inputs)

    def test_templates_and_supported_global_calls(self):
        environment = Environment()
        allowed = {'as_datetime', 'as_timestamp', 'device_attr', 'dict', 'iif',
                   'is_state', 'namespace', 'now', 'state_attr', 'states'}
        for value in walk(self.blueprint):
            if isinstance(value, str) and ('{{' in value or '{%' in value):
                syntax = environment.parse(value)
                for call in syntax.find_all(nodes.Call):
                    if isinstance(call.node, nodes.Name):
                        self.assertIn(call.node.name, allowed)

    def test_upstream_telegram_compatibility(self):
        self.assertIn('notify_telegram_config_entry', self.inputs)
        sends = [value for value in walk(self.blueprint['actions'])
                 if isinstance(value, dict) and str(value.get('service', '')).startswith('{{ telegram_')]
        self.assertEqual(len(sends), 14)
        self.assertTrue(all(value['data']['parse_mode'] == 'plain_text' for value in sends))
        self.assertEqual(sum('config_entry_id' in value['data'] for value in sends), 7)

    def test_upstream_tv_compatibility(self):
        self.assertIn('tv_entities', self.inputs)
        sends = [value for value in walk(self.blueprint['actions'])
                 if isinstance(value, dict) and value.get('action') == 'nfandroidtv.send_message']
        self.assertEqual(len(sends), 4)
        self.assertTrue(all(value['data']['image']['media_content_id'] == '{{ tv_media_source }}' for value in sends))

    def test_final_summary_guard_is_boolean(self):
        branch = self.blueprint['actions'][0]['choose'][3]
        guard = branch['sequence'][1]['choose'][0]['conditions'][1]
        for metadata, expected in [({}, False), ({'shortSummary': '  '}, False),
                                   ({'shortSummary': 'Person walking a dog'}, True),
                                   ({'scene': 'Detailed scene'}, True)]:
            self.assertIs(self.environment.from_string(guard).render(metadata=metadata), expected)

    def test_final_summary_fallback(self):
        variables = self.blueprint['actions'][0]['choose'][3]['sequence'][0]['variables']
        expression = self.environment.from_string(variables['message'])
        self.assertEqual(expression.render(metadata={'scene': 'Scene'}, genai_final_description=True), 'Scene')
        self.assertEqual(expression.render(metadata={'shortSummary': 'Short', 'scene': 'Scene'}, genai_final_description=True), 'Short')
        self.assertEqual(expression.render(metadata={'scene': 'Scene'}, genai_final_description=False), '')

    def test_matrix_titles_and_uploads(self):
        titles = [value['matrix_title_html'] for value in walk(self.blueprint)
                  if isinstance(value, dict) and 'matrix_title_html' in value]
        self.assertEqual(len(titles), 4)
        for expression in titles:
            for title in ['', None, ' ', '<strong></strong>']:
                self.assertEqual(self.environment.from_string(expression).render(title=title, camera_name='Front Door'),
                                 '<strong>Detection at Front Door</strong>')
        uploads = [value for value in walk(self.blueprint['actions'])
                   if isinstance(value, dict) and value.get('action') == 'matrix.send_message'
                   and 'images' in value.get('data', {}).get('data', {})]
        self.assertEqual(len(uploads), 4)
        self.assertTrue(all(value['data']['message'] == '' for value in uploads))
        downloads = [value for value in walk(self.blueprint['actions'])
                     if isinstance(value, dict) and value.get('action') == 'downloader.download_file']
        self.assertEqual(len(downloads), 4)
        self.assertTrue(all(value['data']['subdir'] == '{{ matrix_download_subdir }}' for value in downloads))

    def test_independent_service_and_phone_controls(self):
        variables = self.blueprint['variables']
        for stage in ['sprinter', 'final']:
            expression = variables[f'genai_{stage}_active']
            self.assertIs(self.environment.from_string(expression).render(
                **{f'genai_{stage}': False}, notification_service='notify.example',
                notification_service_stages=[f'genai_{stage}']), True)
        self.assertTrue(self.inputs['genai_final']['default'])
        self.assertFalse(self.inputs['genai_sprinter']['default'])
        self.assertEqual(set(self.inputs['notification_service_stages']['default']),
                         {'frigate_initial', 'frigate_final', 'genai_sprinter', 'genai_final'})

    def test_separate_timers_and_final_exemption(self):
        self.assertNotEqual(self.inputs['regular_cooldown_timer_prefix']['default'],
                            self.inputs['genai_sprinter_timer_prefix']['default'])
        final = json.dumps(self.blueprint['actions'][0]['choose'][3])
        self.assertNotIn('regular_timer_entity', final)
        self.assertNotIn('sprinter_timer_entity', final)
        self.assertEqual(self.inputs['genai_sprinter_interval']['default'], 0)
        self.assertEqual(self.inputs['regular_cooldown_scope']['default'], 'automation')

    def test_source_and_no_local_credentials(self):
        self.assertEqual(self.blueprint['blueprint']['source_url'],
                         'https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Beta.yaml')
        self.assertNotIn('has_service(', self.source)
        self.assertEqual(self.inputs['matrix_room']['default'], '')
        self.assertEqual(self.inputs['base_url']['default'], '')


if __name__ == '__main__':
    unittest.main()
