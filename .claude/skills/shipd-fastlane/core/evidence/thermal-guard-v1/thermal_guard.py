#!/usr/bin/env python3
"""Watch one explicitly owned Docker container; never discovers unrelated containers."""
import argparse,datetime,json,pathlib,re,signal,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--container',required=True);p.add_argument('--log',required=True);p.add_argument('--cpus',type=float,default=.5);p.add_argument('--pause-at',type=float,default=75);p.add_argument('--resume-below',type=float,default=65);p.add_argument('--interval',type=float,default=3);p.add_argument('--wait-start',type=float,default=300)
a=p.parse_args();log=pathlib.Path(a.log);log.parent.mkdir(parents=True,exist_ok=True)
started=time.monotonic();identity=None;paused_at=None;paused_seconds=0;configured=False
def emit(action,**extra):
 with log.open('a') as f:f.write(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),container=identity or a.container,action=action,**extra))+'\n')
def inspect():
 r=subprocess.run(['docker','inspect',a.container],capture_output=True,text=True)
 return json.loads(r.stdout)[0] if r.returncode==0 else None
def fail_closed(reason,code):
 # Never resume a pre-existing pause or operate on a replacement container.
 latest=inspect()
 if latest and latest['Id']==identity and latest['State']['Running']:
  if latest['State']['Paused']:emit('fail_closed_already_paused',reason=reason)
  else:
   r=subprocess.run(['docker','pause',identity],capture_output=True,text=True)
   emit('fail_closed_pause',reason=reason,returncode=r.returncode,diagnostic=r.stderr.strip())
 done(reason)
 raise SystemExit(code)
def done(reason):
 global paused_seconds
 if paused_at is not None:paused_seconds+=time.monotonic()-paused_at
 emit('finished',reason=reason,wall_seconds=round(time.monotonic()-started,3),thermal_pause_seconds=round(paused_seconds,3))
def interrupted(signum, frame):
 emit('interrupted',signal=signum)
 fail_closed('guard_interrupted',128+signum)
signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGINT, interrupted)
while True:
 info=inspect()
 if info is None:
  if identity is not None:done('container_removed');break
  if time.monotonic()-started>a.wait_start:done('start_timeout');raise SystemExit(2)
  time.sleep(a.interval);continue
 if identity is None:identity=info['Id'];emit('attached',pre_existing_paused=info['State']['Paused'])
 elif identity!=info['Id']:done('container_identity_changed');raise SystemExit(3)
 state=info['State']
 if state['Status'] in ['exited','dead','removing']:done('container_completed');break
 if not state['Running']:time.sleep(a.interval);continue
 if not configured:
  flags=['--cpus',str(a.cpus)] if info['HostConfig'].get('NanoCpus',0) else ['--cpu-period','100000','--cpu-quota',str(round(a.cpus*100000))]
  result=subprocess.run(['docker','update',*flags,identity],capture_output=True,text=True)
  emit('quota_update',returncode=result.returncode,cpus=a.cpus,diagnostic=result.stderr.strip())
  if result.returncode:
   if inspect() is None:done('completed_during_update');break
   fail_closed('quota_update_failed',4)
  configured=True
 try: sensor=subprocess.check_output(['sensors'],text=True,stderr=subprocess.STDOUT)
 except (OSError,subprocess.CalledProcessError) as error:
  emit('sensor_read_failed',diagnostic=str(error));fail_closed('sensor_read_failed',5)
 match=re.search(r'Package id 0:\s*\+([\d.]+)',sensor)
 if not match:emit('sensor_unavailable');fail_closed('sensor_unavailable',5)
 temp=float(match.group(1));action=None
 if temp>=a.pause_at and not state['Paused']:action='pause'
 elif temp<a.resume_below and paused_at is not None:action='unpause'
 if action:
  result=subprocess.run(['docker',action,identity],capture_output=True,text=True)
  emit(action,celsius=temp,returncode=result.returncode,diagnostic=result.stderr.strip())
  if result.returncode:
   latest=inspect()
   if latest is None or not latest['State']['Running']:done('completed_during_'+action);break
   fail_closed(action+'_failed',6)
  if action=='pause':paused_at=time.monotonic()
  else:
   waited=time.monotonic()-paused_at;paused_seconds+=waited;paused_at=None
   emit('thermal_wait',seconds=round(waited,3))
 else:emit('sample',celsius=temp,paused=state['Paused'])
 time.sleep(a.interval)
