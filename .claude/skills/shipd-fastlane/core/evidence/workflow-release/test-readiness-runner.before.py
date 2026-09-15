#!/usr/bin/env python3
"""Bounded harness fixtures; no Cargo compiler, repository tests, or Docker runs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

TEMPLATE = Path(__file__).with_name("runner-template.py")
FAKE_TOOL = r"""#!/usr/bin/env python3
import json, os, pathlib, sys
root = pathlib.Path.cwd()
config = json.loads((root / 'fixture-config.json').read_text())
tool = pathlib.Path(sys.argv[0]).name
with (root / 'calls.jsonl').open('a') as out:
 out.write(json.dumps({'tool':tool, 'args':sys.argv[1:], 'bootstrap':os.environ.get('RUSTC_BOOTSTRAP')})+'\n')
if tool == 'cargo':
 if sys.argv[1] == 'build':
  cli = root / 'target/debug/lis'; cli.parent.mkdir(parents=True,exist_ok=True); cli.write_text('fake CLI\n')
  sys.exit(config.get('cli_code',0))
 if config.get('compile_code'):
  print('simulated compiler error',file=sys.stderr); sys.exit(config['compile_code'])
 targets=[]
 for index,arg in enumerate(sys.argv):
  if arg=='--test': targets.append(sys.argv[index+1])
  if arg=='--lib': targets.append('kite_sql')
 for target in targets:
  if target in config.get('omit_artifact',[]): continue
  print(json.dumps({'reason':'compiler-artifact','profile':{'test':True},'target':{'name':target},'executable':str(root/'bin'/target)}))
 sys.exit(0)
target=config['targets'][tool]
if '--list' in sys.argv:
 for name in target['inventory']: print(name+': test')
 sys.exit(target.get('discovery_code',0))
if 'events' in target:
 events=target['events']
else:
 names=sys.argv[1:sys.argv.index('--exact')]
 events=[]
 for name in names:
  if name in target.get('ignored',[]):
   if target.get('start_ignored'): events.append({'type':'test','event':'started','name':name})
   events.append({'type':'test','event':'ignored','name':name})
  else:
   events.extend([{'type':'test','event':'started','name':name},
                  {'type':'test','event':'failed' if name in target.get('failed',[]) else 'ok','name':name}])
for event in events:
 print(event if isinstance(event,str) else json.dumps(event))
sys.exit(target.get('runtime_code',101 if target.get('failed') else 0))
"""

class RunnerTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)
  (self.root/'bin').mkdir()
  (self.root/'tests').mkdir()
  for name in ('cargo','field_defaults','expression_index','suite','kite_sql'):
   f=self.root/'bin'/name; f.write_text(FAKE_TOOL); f.chmod(0o755)
  (self.root/'Cargo.toml').write_text('[package]\nname="fixture"\n')
  (self.root/'Cargo.lock').write_text('# fixture\n')
  self.config={'targets':{
   'expression_index':{'inventory':['feature_one','feature_two','adjacent_legacy']},
   'field_defaults':{'inventory':['feature_one','feature_two','existing_zero_spread_and_constructor_behaviors_stay_valid','illegal_positions_recover_the_next_declaration']},
   'kite_sql':{'inventory':['lib_one','lib_two']},
   'suite':{'inventory':['spec::parse::one','ui::two','stdlib::omitted']}}}
 def execute(self,project='kitesql',mode='new',args=None):
  (self.root/'fixture-config.json').write_text(json.dumps(self.config))
  integration='field_defaults' if project=='lisette' else 'expression_index'
  (self.root/'tests'/(integration+'.rs')).write_text('// fixture source\n')
  (self.root/'runner.py').write_text(TEMPLATE.read_text().replace('__PROJECT__',project))
  env=os.environ.copy()
  env.update(PATH=str(self.root/'bin')+os.pathsep+env['PATH'],RUSTC_BOOTSTRAP='inherited-do-not-forward')
  command=[sys.executable,'runner.py',*(args if args is not None else [mode,'--output','result'])]
  process=subprocess.run(command,cwd=self.root,env=env,capture_output=True,text=True,timeout=15)
  report=self.root/'result/junit.xml' if args is None else self.root/'custom.xml'
  evidence=report.parent if args is None else self.root/'custom.xml.evidence'
  self.assertTrue(report.exists(),process.stderr)
  tree=ET.parse(report).getroot()
  receipt=json.loads((evidence/'receipt.json').read_text())
  inventory=json.loads((evidence/'inventory.json').read_text())
  raw=(evidence/'raw-libtest.jsonl').read_text()
  return process,tree,receipt,inventory,raw,evidence
 def assert_harness_error(self,result,executed=None):
  process,tree,receipt,_,_,_=result
  self.assertNotEqual(process.returncode,0)
  self.assertGreater(int(tree.get('errors')),0)
  if executed is not None:self.assertEqual(receipt['executed'],executed)
 def test_kite_features_exclude_compatibility_and_preserve_sources(self):
  result=self.execute()
  process,tree,receipt,inventory,raw,evidence=result
  self.assertEqual(process.returncode,0,process.stderr)
  self.assertEqual(inventory['tests'],['kitesql::feature_one','kitesql::feature_two'])
  self.assertEqual(receipt['executed'],2)
  self.assertEqual(int(tree.get('failures')),0)
  self.assertEqual(len([json.loads(line) for line in raw.splitlines()]),4)
  hashes=json.loads((evidence/'source-hashes.json').read_text())
  self.assertEqual(hashes['tests/expression_index.rs'],hashlib.sha256(b'// fixture source\n').hexdigest())
  self.assertEqual(receipt['binaries']['expression_index']['sha256'],hashlib.sha256((self.root/'bin/expression_index').read_bytes()).hexdigest())
 def test_kite_base_runs_library_and_adjacent(self):
  process,tree,receipt,inventory,_,_=self.execute(mode='base')
  self.assertEqual(process.returncode,0)
  self.assertEqual(set(inventory['tests']),{'kitesql::lib_one','kitesql::lib_two','kitesql::adjacent_legacy'})
  self.assertEqual(receipt['executed'],3)
 def test_lisette_base_preserves_two_adjacent_and_exclusions(self):
  process,tree,receipt,inventory,_,_=self.execute(project='lisette',mode='base')
  self.assertEqual(process.returncode,0,process.stderr)
  self.assertEqual(receipt['executed'],4)
  self.assertIn('lisette::illegal_positions_recover_the_next_declaration',inventory['tests'])
  self.assertIn('lisette::stdlib::omitted',{x['id'] for x in inventory['excluded']})
  self.assertIn('cli_sha256',receipt)
 def test_lisette_new_contains_only_features(self):
  process,_,receipt,inventory,_,_=self.execute(project='lisette')
  self.assertEqual(process.returncode,0)
  self.assertEqual(inventory['tests'],['lisette::feature_one','lisette::feature_two'])
  self.assertEqual(receipt['executed'],2)
 def test_compile_failure_is_error_with_zero_execution(self):
  self.config['compile_code']=101
  result=self.execute()
  self.assert_harness_error(result,0)
  self.assertEqual(result[0].returncode,101)
  self.assertEqual(int(result[1].get('failures')),0)
  self.assertEqual(result[4],'')
  self.assertEqual(result[3]['tests'],[])
 def test_missing_binary_is_harness_error(self):
  self.config['omit_artifact']=['expression_index']
  self.assert_harness_error(self.execute(),0)
 def test_cli_compile_failure_is_not_assertion(self):
  self.config['cli_code']=101
  result=self.execute(project='lisette')
  self.assert_harness_error(result,0)
  self.assertEqual(int(result[1].get('failures')),0)
 def test_duplicate_discovery_fails_before_execution(self):
  self.config['targets']['expression_index']['inventory']=['feature_one','feature_one']
  self.assert_harness_error(self.execute(),0)
 def test_empty_selected_inventory_is_harness_error(self):
  self.config['targets']['expression_index']['inventory']=['adjacent_legacy']
  self.assert_harness_error(self.execute(),0)
 def test_assertion_failure_is_failure_not_error(self):
  self.config['targets']['expression_index']['failed']=['feature_two']
  process,tree,receipt,_,_,_=self.execute()
  self.assertEqual(process.returncode,101)
  self.assertEqual((int(tree.get('errors')),int(tree.get('failures')),receipt['executed']),(0,1,2))
 def test_failure_with_success_exit_is_harness_contradiction(self):
  self.config['targets']['expression_index'].update(failed=['feature_one'],runtime_code=0)
  self.assert_harness_error(self.execute(),2)
 def test_nonzero_exit_without_assertion_is_harness_error(self):
  self.config['targets']['expression_index']['runtime_code']=3
  self.assert_harness_error(self.execute(),2)
 def events(self,events):
  self.config['targets']['expression_index']['events']=events
 def test_zero_exit_without_events_cannot_pass(self):
  self.events([])
  self.assert_harness_error(self.execute(),0)
 def test_missing_terminal_cannot_pass(self):
  self.events([{'type':'test','event':'started','name':'feature_one'}])
  self.assert_harness_error(self.execute(),1)
 def test_extra_start_without_terminal_cannot_pass(self):
  self.events([{'type':'test','event':'started','name':name} for name in ['feature_one','feature_two','extra']]+[{'type':'test','event':'ok','name':name} for name in ['feature_one','feature_two']])
  self.assert_harness_error(self.execute(),3)
 def test_duplicate_start_cannot_pass(self):
  self.events([{'type':'test','event':'started','name':name} for name in ['feature_one','feature_one','feature_two']]+[{'type':'test','event':'ok','name':name} for name in ['feature_one','feature_two']])
  self.assert_harness_error(self.execute(),2)
 def test_duplicate_terminal_cannot_pass(self):
  self.events([{'type':'test','event':'started','name':name} for name in ['feature_one','feature_two']]+[{'type':'test','event':'ok','name':name} for name in ['feature_one','feature_two','feature_two']])
  self.assert_harness_error(self.execute(),2)
 def test_terminal_before_start_cannot_pass(self):
  self.events([{'type':'test','event':'ok','name':'feature_one'},{'type':'test','event':'started','name':'feature_one'},{'type':'test','event':'started','name':'feature_two'},{'type':'test','event':'ok','name':'feature_two'}])
  self.assert_harness_error(self.execute(),2)
 def test_malformed_event_preserves_valid_prior_evidence(self):
  self.events([{'type':'test','event':'started','name':'feature_one'},'not JSON',{'type':'test','event':'ok','name':'feature_one'},{'type':'test','event':'started','name':'feature_two'},{'type':'test','event':'ok','name':'feature_two'}])
  result=self.execute()
  self.assert_harness_error(result,2)
  self.assertIn('not JSON\n',result[4])
  self.assertEqual(len(result[1].findall('./testcase[@name="feature_one"]')),1)
 def test_unknown_test_event_is_harness_error(self):
  self.events([{'type':'test','event':'mysterious','name':'feature_one'}])
  self.assert_harness_error(self.execute(),0)
 def test_ignored_is_skipped_not_executed(self):
  self.config['targets']['expression_index']['ignored']=['feature_two']
  process,tree,receipt,_,_,_=self.execute()
  self.assertEqual(process.returncode,0)
  self.assertEqual((int(tree.get('skipped')),receipt['executed']),(1,1))
 def test_ignored_may_have_native_start_without_claiming_execution(self):
  self.config['targets']['expression_index'].update(ignored=['feature_two'],start_ignored=True)
  process,tree,receipt,_,_,_=self.execute()
  self.assertEqual(process.returncode,0)
  self.assertEqual((int(tree.get('skipped')),receipt['executed']),(1,1))
 def test_output_path_option_before_mode_matches_hosted_cli(self):
  process,_,receipt,_,_,_=self.execute(args=['--output_path','custom.xml','new'])
  self.assertEqual(process.returncode,0)
  self.assertEqual(receipt['partition'],'new')
 def test_output_path_option_after_mode_matches_hosted_cli(self):
  process,_,_,_,_,_=self.execute(args=['new','--output_path','custom.xml'])
  self.assertEqual(process.returncode,0)
 def test_xml_control_characters_are_escaped_without_changing_raw_events(self):
  stdout="ANSI: \\x1b[31m bad \\x00 \\x0b \\ud800 \\ufffe; unicode: é 🧪\\n"
  self.events([{'type':'test','event':'started','name':'feature_one'},
               {'type':'test','event':'failed','name':'feature_one','stdout':stdout},
               {'type':'test','event':'started','name':'feature_two'},
               {'type':'test','event':'ok','name':'feature_two'}])
  self.config['targets']['expression_index']['runtime_code']=101
  process,tree,receipt,_,raw,_=self.execute()
  self.assertEqual(process.returncode,101)
  self.assertEqual(int(tree.get('errors')),0)
  xml_stdout=tree.find('./testcase[@name="feature_one"]/system-out').text
  self.assertIn(r"\\u001b[31m",xml_stdout)
  self.assertIn(r"\\u0000",xml_stdout)
  self.assertIn(r"\\ud800",xml_stdout)
  self.assertIn("é 🧪",xml_stdout)
  self.assertEqual(json.loads(raw.splitlines()[1])['stdout'],stdout)
 def test_partial_execution_reports_started_separately_from_completed(self):
  self.events([{'type':'test','event':'started','name':'feature_one'},
               {'type':'test','event':'ok','name':'feature_one'},
               {'type':'test','event':'started','name':'feature_two'}])
  self.config['targets']['expression_index']['runtime_code']=137
  result=self.execute()
  self.assert_harness_error(result,2)
  self.assertEqual(result[2]['completed'],1)
  self.assertEqual(result[2]['observed_native_starts'],2)
  self.assertEqual(int(result[1].get('completed')),1)
  self.assertEqual(int(result[1].get('failures')),0)
 def test_bootstrap_only_native_execution(self):
  self.execute()
  calls=[json.loads(line) for line in (self.root/'calls.jsonl').read_text().splitlines()]
  for call in calls:
   expected='1' if call['tool']!='cargo' and '--list' not in call['args'] else None
   self.assertEqual(call['bootstrap'],expected,call)
 def test_source_scan_prunes_target_before_following_unreadable_paths(self):
  target=self.root/'target'; target.mkdir()
  (target/'unreadable.rs').symlink_to('/does-not-exist-readiness-fixture')
  process,_,_,_,_,evidence=self.execute()
  self.assertEqual(process.returncode,0)
  hashes=json.loads((evidence/'source-hashes.json').read_text())
  self.assertNotIn('target/unreadable.rs',hashes)

if __name__=='__main__':
 unittest.main()
