"""Regression checks for late Sprinter suppression and marker cleanup."""
import unittest
from test_beta import BLUEPRINT, BlueprintLoader
import yaml
class GuardTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.doc=yaml.load(BLUEPRINT.read_text(encoding='utf-8'),Loader=BlueprintLoader)
  cls.branches=cls.doc['actions'][0]['choose']
  cls.sprinter=next(x for x in cls.branches if x.get('alias')=='GenAI Sprinter Update')
  cls.final=next(x for x in cls.branches if x.get('alias')=='Final GenAI Review Summary')
  from jinja2.nativetypes import NativeEnvironment
  cls.env=NativeEnvironment()
  cls.env.globals.update(now=lambda:100000,as_timestamp=lambda x:x)
 def test_marker_age_and_empty_payloads(self):
  check=self.sprinter['sequence'][0]['wait_for_trigger'][0]['value_template']
  for payload,expected in [('99990','finalized'),('10000','expired'),('','expired'),('garbage','expired')]:
   self.assertEqual(self.env.from_string(check).render(value=payload),expected)
 def test_same_object_blocked_other_object_allowed(self):
  t=self.sprinter['sequence'][0]['wait_for_trigger'][0]['topic']
  render=lambda obj:self.env.from_string(t).render(genai_guard_root='root/automation.a',camera='driveway_x16',trigger_payload={'id':obj})
  retained={render('primary'):99990,render('secondary'):99990}
  self.assertIn(render('primary'),retained)
  self.assertIn(render('secondary'),retained)
  self.assertNotIn(render('new-object'),retained)
 def test_final_marks_all_ids_after_filters_before_delivery(self):
  choose=next(x['choose'] for x in self.final['sequence'] if 'choose' in x)
  seq=choose[0]['sequence']
  self.assertEqual(seq[0]['alias'],'Commit Final for every object in the review')
  self.assertEqual(seq[0]['repeat']['for_each'],'{{ detections | unique | list }}')
  self.assertTrue(seq[0]['repeat']['sequence'][0]['data']['retain'])
 def test_phone_rechecked_after_service(self):
  seq=self.sprinter['sequence']
  i=next(i for i,x in enumerate(seq) if x.get('if')=='{{ primary_notify_enabled and genai_sprinter }}')
  self.assertIn('wait_for_trigger',seq[i-2])
  self.assertIn('stop',seq[i-1]['then'][0])
 def test_cleanup_scoped_and_bounded(self):
  branch=next(x for x in self.branches if x.get('alias')=='Expire finalized object markers')
  loop=branch['sequence'][0]['repeat']
  self.assertEqual(loop['count'],100)
  self.assertEqual(loop['sequence'][-1]['data']['payload'],'')
  template=loop['sequence'][0]['wait_for_trigger'][0]['value_template']
  self.assertEqual(self.env.from_string(template).render(value='99990'),'keep')
  self.assertEqual(self.env.from_string(template).render(value='10000'),'expired')

if __name__ == "__main__":
 unittest.main()
