"""Behavior checks for maintainer-requested filtering and phone media policy."""
import unittest
import yaml
from jinja2.nativetypes import NativeEnvironment
from test_beta import BLUEPRINT, BlueprintLoader, walk

class MaintainerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=yaml.load(BLUEPRINT.read_text(encoding='utf-8'),Loader=BlueprintLoader)
        cls.branches=cls.doc['actions'][0]['choose']
        cls.sprinter=next(x for x in cls.branches if x.get('alias')=='GenAI Sprinter Update')
        cls.env=NativeEnvironment()
        cls.env.globals.update(now=lambda:100000,as_timestamp=lambda v:v)
    def test_new_automations_default_to_alerts(self):
        self.assertEqual(self.doc['blueprint']['input']['filters']['input']['review_severity']['default'],['alert'])
    def test_review_cache_stores_all_objects_without_master_or_cooldown(self):
        c=next(x for x in self.branches if x.get('alias')=='Cache review filters for Sprinters')
        self.assertEqual(c['sequence'][0]['repeat']['for_each'],'{{ trigger_detections | unique | list }}')
        self.assertTrue(c['sequence'][0]['repeat']['sequence'][0]['data']['retain'])
        gate=self.doc['conditions']['conditions'][0]['value_template']
        self.assertNotIn('master',gate)
        self.assertNotIn('cooldown',gate)
    def test_missing_context_stops_before_sending(self):
        seq=self.sprinter['sequence']
        i=next(i for i,x in enumerate(seq) if x.get('alias')=='Read Sprinter review context')
        self.assertEqual(seq[i+1]['if'],'{{ not wait.completed }}')
        self.assertIn('stop',seq[i+1]['then'][0])
        t=seq[i]['wait_for_trigger'][0]['value_template']
        self.assertEqual(self.env.from_string(t).render(value_json={'cached_at':99999}),'current')
        self.assertEqual(self.env.from_string(t).render(value_json={'cached_at':1}),'expired')
    def test_filtered_sprinter_does_not_consume_timer(self):
        seq=self.sprinter['sequence']
        self.assertLess(next(i for i,x in enumerate(seq) if x.get('alias')=='Apply Sprinter notification filters'),next(i for i,x in enumerate(seq) if x.get('alias')=='Per camera Sprinter cooldown'))
    def test_sprinter_filter_boolean_behavior(self):
        gate=next(x['value_template'] for x in self.sprinter['sequence'] if x.get('alias')=='Apply Sprinter notification filters')
        # Supply now().hour rather than the numeric clock used for marker tests.
        from types import SimpleNamespace
        base=dict(severity_satisfied=True,objects_satisfied=True,zones_satisfied=True,home=False,state_satisfied=True,custom_filter=True,disable_times=[],now=lambda:SimpleNamespace(hour=12))
        self.assertTrue(self.env.from_string(gate).render(**base))
        for key in ['severity_satisfied','objects_satisfied','zones_satisfied','state_satisfied','custom_filter']:
            self.assertFalse(self.env.from_string(gate).render(**dict(base,**{key:False})),key)
        self.assertFalse(self.env.from_string(gate).render(**dict(base,home=True)))
        self.assertFalse(self.env.from_string(gate).render(**dict(base,disable_times=[12])))
    def test_four_phone_policies_keep_empty_conditions_compatible(self):
        policies=[x for x in walk(self.doc['actions']) if isinstance(x,dict) and x.get('alias')=='Choose phone attachment for current connection']
        self.assertEqual(len(policies),4)
        self.assertTrue(all(x['if']=={'input':'phone_rich_media_condition'} for x in policies))
        for policy in policies:
            gate=policy['else'][0]['if']
            for attachment,video,tv,telegram,want in [('x.gif','',False,False,True),('x.jpg','x.mp4',False,False,True),('x.jpg','',False,False,False),('x.gif','',True,False,False),('x.gif','',False,True,False)]:
                self.assertEqual(self.env.from_string(gate).render(attachment=attachment,video=video,tv=tv,telegram=telegram),want)
            fallback=policy['else'][0]['then'][0]['variables']
            self.assertEqual(fallback['phone_video'],'')
    def test_mobile_payloads_use_phone_media(self):
        sends=[x for x in walk(self.doc['actions']) if isinstance(x,dict) and x.get('domain')=='mobile_app' and x.get('data',{}).get('image')]
        self.assertEqual(len(sends),4)
        for send in sends:
            self.assertEqual(send['data']['image'],'{{phone_attachment}}')
            self.assertNotIn('else attachment',send['data']['attachment']['url'])
    def test_matrix_and_telegram_keep_original_media(self):
        downloads=[x for x in walk(self.doc['actions']) if isinstance(x,dict) and x.get('action')=='downloader.download_file']
        self.assertTrue(downloads)
        self.assertTrue(all(x['data']['url']=='{{ attachment }}' for x in downloads))
        for x in walk(self.doc['actions']):
            if isinstance(x,dict) and str(x.get('service','')).startswith('{{ telegram_'):
                self.assertNotIn('phone_attachment',str(x))
    def test_automation_cooldown_ignores_context_last_triggered(self):
        self.assertNotIn('last_triggered',str(self.doc['conditions']))
        gate=next(x for x in walk(self.doc['actions']) if isinstance(x,dict) and x.get('alias')=='Automation initial notification cooldown')
        self.assertIn('regular_cooldown',gate['then'][0]['wait_for_trigger'][0]['topic'])

if __name__=='__main__':
    unittest.main()
