import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('result_gate', Path(__file__).parents[1] / 'scripts/test_result_gate.py')
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)

class ResultGateTest(unittest.TestCase):
    def run_gate(self, xml, ids=('m::one',), code=0, expected='pass', excluded=None):
        with tempfile.TemporaryDirectory() as d:
            xml_path, inventory = Path(d)/'results.xml', Path(d)/'inventory.json'
            xml_path.write_text(xml); inventory.write_text(json.dumps({'tests': list(ids), 'excluded': excluded or []}))
            return gate.check(xml_path, inventory, code, expected)

    def test_nested_suites_and_pass(self):
        r = self.run_gate('<testsuites tests="1"><testsuite tests="1" failures="0"><testcase classname="m" name="one"/></testsuite></testsuites>')
        self.assertEqual(r['status'], 'EXECUTION_RECONCILED')

    def test_missing_discovered_test_blocks(self):
        r = self.run_gate('<testsuite tests="1"><testcase classname="m" name="one"/></testsuite>', ids=['m::one','m::two'])
        self.assertEqual(r['missing'], ['m::two']); self.assertEqual(r['status'], 'FAIL')

    def test_duplicate_case_cannot_inflate_coverage(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"/><testcase classname="m" name="one"/></testsuite>')
        self.assertEqual(r['status'], 'FAIL')

    def test_silent_wrong_filter_blocks(self):
        r = self.run_gate('<testsuite tests="0"/>')
        self.assertEqual(r['status'], 'FAIL')

    def test_broken_counter_blocks(self):
        r = self.run_gate('<testsuite tests="99"><testcase classname="m" name="one"/></testsuite>')
        self.assertEqual(r['status'], 'FAIL')

    def test_failure_and_nonzero_discriminate(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"><failure>assertion</failure></testcase></testsuite>', code=101, expected='fail')
        self.assertEqual(r['status'], 'EXECUTION_RECONCILED')

    def test_compile_error_is_not_behavioral_failure(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"><error>compile failed</error></testcase></testsuite>', code=101, expected='fail')
        self.assertEqual(r['status'], 'FAIL')

    def test_hidden_exit_failure_blocks(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"/></testsuite>', code=101)
        self.assertEqual(r['status'], 'FAIL')

    def test_skipped_requirement_blocks(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"><skipped/></testcase></testsuite>')
        self.assertEqual(r['status'], 'FAIL')

    def test_invalid_xml_control_byte_rejected(self):
        with self.assertRaises(gate.ET.ParseError):
            self.run_gate('<testsuite><testcase classname="m" name="one"><system-out>\x01</system-out></testcase></testsuite>')

    def test_explicit_exclusions_remain_unverified(self):
        exclusion = {'id':'m::live_db','reason':'requires external database','grounding':'pinned test opens SCYLLA_URI'}
        r = self.run_gate('<testsuite><testcase classname="m" name="one"/></testsuite>', excluded=[exclusion])
        self.assertEqual(r['status'], 'EXECUTION_RECONCILED'); self.assertEqual(r['unverified_exclusions'], [exclusion])

    def test_required_test_cannot_be_excluded(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"/></testsuite>', excluded=[{'id':'m::one','reason':'slow','grounding':'test'}])
        self.assertEqual(r['status'], 'FAIL')

    def test_process_failure_with_no_assertion_is_not_discrimination(self):
        r = self.run_gate('<testsuite><testcase classname="m" name="one"/></testsuite>', code=1, expected='fail')
        self.assertEqual(r['status'], 'FAIL')

class RawEventsTest(unittest.TestCase):
    def run_events(self, xml, events, code=0, expected='pass'):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            (d/'x.xml').write_text(xml)
            (d/'i.json').write_text(json.dumps({'tests':['m::one']}))
            (d/'events').write_text(events)
            return gate.check(d/'x.xml', d/'i.json', code, expected, d/'events', 'm')

    def events(self, outcome):
        return '\n'.join(json.dumps(e) for e in [
            {'type':'test','event':'started','name':'one'},
            {'type':'test','event':outcome,'name':'one'}])

    def test_direct_pass_events_reconcile(self):
        r=self.run_events('<testsuite><testcase classname="m" name="one"/></testsuite>',self.events('ok'))
        self.assertEqual(r['status'],'EXECUTION_RECONCILED')
        self.assertEqual(r['raw_event_evidence']['terminal_count'],1)

    def test_fabricated_compile_failure_has_no_terminal_execution(self):
        r=self.run_events('<testsuite><testcase classname="m" name="one"><failure>compiler error</failure></testcase></testsuite>','error: build failed',101,'fail')
        self.assertEqual(r['status'],'FAIL')
        self.assertIn('No raw terminal events.',r['issues'])

    def test_pass_in_xml_but_failed_event_rejected(self):
        r=self.run_events('<testsuite><testcase classname="m" name="one"/></testsuite>',self.events('failed'))
        self.assertEqual(r['status'],'FAIL')

    def test_duplicate_terminal_event_rejected(self):
        stream=self.events('ok')+'\n'+json.dumps({'type':'test','event':'ok','name':'one'})
        self.assertEqual(self.run_events('<testsuite><testcase classname="m" name="one"/></testsuite>',stream)['status'],'FAIL')

    def test_terminal_without_start_rejected(self):
        stream=json.dumps({'type':'test','event':'ok','name':'one'})
        self.assertEqual(self.run_events('<testsuite><testcase classname="m" name="one"/></testsuite>',stream)['status'],'FAIL')

    def test_extra_started_test_cannot_hide_behind_passing_report(self):
        stream = self.events('ok') + '\n' + json.dumps({'type':'test','event':'started','name':'interrupted'})
        r = self.run_events('<testsuite><testcase classname="m" name="one"/></testsuite>', stream)
        self.assertEqual(r['status'], 'FAIL')
        self.assertIn('Raw start event has no terminal outcome: m::interrupted', r['issues'])

    def test_extra_started_test_invalidates_expected_behavioral_failure(self):
        stream = self.events('failed') + '\n' + json.dumps({'type':'test','event':'started','name':'interrupted'})
        r = self.run_events('<testsuite><testcase classname="m" name="one"><failure>assertion</failure></testcase></testsuite>',
                            stream, 101, 'fail')
        self.assertEqual(r['status'], 'FAIL')
        self.assertIn('Raw start event has no terminal outcome: m::interrupted', r['issues'])

    def test_ignored_event_without_start_still_reports_selected_skip(self):
        stream = json.dumps({'type':'test','event':'ignored','name':'one'})
        r = self.run_events('<testsuite><testcase classname="m" name="one"><skipped/></testcase></testsuite>', stream)
        self.assertEqual(r['status'], 'FAIL')
        self.assertEqual(r['issues'], ['Selected tests were skipped.'])

    def test_ignored_event_with_start_does_not_leave_pending_start(self):
        r = self.run_events('<testsuite><testcase classname="m" name="one"><skipped/></testcase></testsuite>', self.events('ignored'))
        self.assertEqual(r['status'], 'FAIL')
        self.assertEqual(r['issues'], ['Selected tests were skipped.'])
