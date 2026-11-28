#!/usr/bin/env python3
"""Local pilot only. Not a security sandbox. Run in an isolated trusted checkout."""
import hashlib, json, pathlib, subprocess, sys, os
REV="bf72fe90290481fbdd0194a3b57cf060105f9540"
BLOB="2d413c848cb7f41362bcf057a9af8da70a2be1f2"
REGISTER="5db44e140940ffb935a1ded423c9c4f7f69a528f"
def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def main():
    if len(sys.argv)!=2: raise ValueError("provide trusted checkout directory")
    root=pathlib.Path(sys.argv[1]).resolve(strict=True)
    rev=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True,timeout=5).strip()
    if rev!=REV: raise ValueError("revision mismatch")
    for name,expected in [("records/math/results.json",REGISTER),("tools/space_prob.py",BLOB)]:
        p=root/name
        if p.resolve()!=p or blob(p.read_bytes())!=expected: raise ValueError("source mismatch: "+name)
    result=subprocess.run([sys.executable,"-I","tools/space_prob.py","--selftest"],cwd=root,capture_output=True,text=True,timeout=15,env={"PATH":os.defpath})
    print(json.dumps({"revision":rev,"blob":BLOB,"argv":["python3","tools/space_prob.py","--selftest"],"actual_argv":result.args,"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr,"python":sys.version,"execution":"LOCAL_RUNNER_REPORTED","sandbox":"NONE"},indent=2))
    return result.returncode
if __name__=="__main__":
    try: sys.exit(main())
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)})); sys.exit(2)
