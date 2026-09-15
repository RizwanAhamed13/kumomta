#!/usr/bin/env python3
import hashlib,json,os,pathlib,re,shutil,subprocess,time
root=pathlib.Path('/home/admin/olympus-work/fastlane-routing-20260912/shipd-fastlane')
e=root/'evidence/thermal-guard-v2';e.mkdir(exist_ok=True)
guard=root/'scripts/thermal_guard.py'
start=time.monotonic()
def run(*args,**kwargs):return subprocess.run(args,check=True,capture_output=True,text=True,**kwargs)
temp=float(re.search(r'Package id 0:\s*\+([\d.]+)',run('sensors').stdout).group(1))
assert temp<75,temp
owned=run('docker','run','-d','--cpus','.1','--name','fastlane-guard-v2-tiny-20260913','public.ecr.aws/d3j8x8q7/olympus-base-rust:latest','sleep','300').stdout.strip()
assert re.fullmatch('[0-9a-f]{64}',owned)
def state():return json.loads(run('docker','inspect',owned).stdout)[0]
def unpause():
 if state()['State']['Paused']:run('docker','unpause',owned)
tools=e/'tools';tools.mkdir(exist_ok=True)
real_docker=shutil.which('docker')
(tools/'docker').write_text("""#!/usr/bin/env python3
import json,os,pathlib,subprocess,sys
a=sys.argv[1:];mode=os.environ['GUARD_FAULT_MODE'];counter=pathlib.Path(os.environ['GUARD_FAULT_COUNTER'])
assert os.environ['OWNED_GUARD_ID'] in a
if a[0]=='inspect':
 n=int(counter.read_text())+1 if counter.exists() else 1;counter.write_text(str(n))
 if n>=2 and mode=='inspect_error':print('injected inspect unavailable',file=sys.stderr);sys.exit(11)
 if n>=2 and mode=='malformed_json':print('{malformed');sys.exit(0)
if a[0]=='update' and mode=='quota_error':print('injected quota rejection',file=sys.stderr);sys.exit(12)
sys.exit(subprocess.run([os.environ['REAL_GUARD_DOCKER'],*a]).returncode)
""")
(tools/'docker').chmod(0o755)
receipts=[]
def events(path):return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []
def wait_for(proc,path,predicate):
 limit=time.monotonic()+12
 while time.monotonic()<limit:
  ev=events(path)
  if predicate(ev):return ev
  if proc.poll() is not None:raise AssertionError((proc.returncode,ev))
  time.sleep(.05)
 raise AssertionError('timeout waiting for event')
try:
 for mode in ['cycle','preexisting','inspect_error','malformed_json','quota_error']:
  unpause()
  if mode=='preexisting':run('docker','pause',owned)
  path=e/(mode+'.jsonl');assert not path.exists()
  env=os.environ.copy()
  if mode in ['inspect_error','malformed_json','quota_error']:
   env.update(PATH=str(tools)+':'+env['PATH'],GUARD_FAULT_MODE=mode,GUARD_FAULT_COUNTER=str(e/(mode+'.count')),OWNED_GUARD_ID=owned,REAL_GUARD_DOCKER=real_docker)
  cmd=['python3',str(guard),'--container',owned,'--log',str(path),'--cpus','.5','--interval','.15']
  if mode=='cycle':cmd+=['--pause-at',str(temp-10),'--resume-below',str(temp+10)]
  # Forced overlapping thresholds intentionally use a test-specific imported
  # Guard configuration; CLI correctly rejects them. Use alternating sensor
  # readings below with valid hysteresis instead.
  if mode=='cycle':
   cmd=cmd[:cmd.index('--pause-at')]
   sensor=tools/'sensors'
   sensor.write_text('#!/bin/sh\nprintf "Package id 0: +'+str(temp)+'°C\\n"\n')
   sensor.chmod(0o755)
   cmd+=['--pause-at',str(temp-5),'--resume-below',str(temp-10)]
   env.update(PATH=str(tools)+':'+env['PATH'],GUARD_FAULT_MODE=mode,GUARD_FAULT_COUNTER=str(e/(mode+'.count')),OWNED_GUARD_ID=owned,REAL_GUARD_DOCKER=real_docker)
  with (e/(mode+'.stderr')).open('w') as err:
   proc=subprocess.Popen(cmd,env=env,stdout=err,stderr=err)
   if mode=='cycle':
    wait_for(proc,path,lambda ev:any(x['action']=='pause' and x['returncode']==0 for x in ev))
    assert state()['State']['Paused']
    assert state()['HostConfig']['NanoCpus']==500000000
    sensor.write_text('#!/bin/sh\nprintf "Package id 0: +'+str(temp-15)+'°C\\n"\n')
    wait_for(proc,path,lambda ev:any(x['action']=='unpause' and x['returncode']==0 for x in ev))
    proc.terminate();rc=proc.wait(timeout=15);assert rc==143
    sensor.unlink()
   elif mode=='preexisting':
    wait_for(proc,path,lambda ev:any(x['action']=='sample' for x in ev))
    proc.terminate();rc=proc.wait(timeout=15);assert rc==143
   else:
    rc=proc.wait(timeout=15);assert rc==(4 if mode=='quota_error' else 7),(mode,rc)
  ev=events(path)
  assert state()['State']['Paused'],mode
  if mode=='preexisting':
   assert ev[0]['pre_existing_paused'] and not any(x['action']=='unpause' for x in ev)
  if mode in ['inspect_error','malformed_json']:
   assert any(x['action']=='fail_closed_inspect_failed' for x in ev)
   assert any(x['action']=='fail_closed_pause' and x['returncode']==0 for x in ev)
  receipts.append({'case':mode,'exit_code':rc,'status':'PASS','log':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
finally:
 unpause();run('docker','stop','-t','1',owned)
receipt={'status':'PASS','temperature':temp,'owned_container':owned,'stopped':not state()['State']['Running'],'wall_seconds':round(time.monotonic()-start,3),'guard_sha256':hashlib.sha256(guard.read_bytes()).hexdigest(),'cases':receipts}
(e/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
