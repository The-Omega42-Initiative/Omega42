"""Regression tests for the pinned runner; mocked checkout identity, real hash checks."""
import importlib.util, pathlib, tempfile, unittest
from unittest.mock import patch
from types import SimpleNamespace
import contextlib, io, json
spec=importlib.util.spec_from_file_location("runner",pathlib.Path(__file__).with_name("run-certificate-pilot.py"))
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=pathlib.Path(self.tmp.name).resolve()
        for name in ("records/math/results.json","tools/space_prob.py"):
            p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b"fixture")
        for obj,name,value in [(r,"REGISTER",r.blob(b"fixture")),(r,"BLOB",r.blob(b"fixture")),(r.sys,"argv",["runner",str(self.root)])]:
            p=patch.object(obj,name,value); p.start(); self.addCleanup(p.stop)
        p=patch.object(r.subprocess,"check_output",return_value=r.REV+"\n"); self.rev=p.start(); self.addCleanup(p.stop)
        p=patch.object(r.subprocess,"run",return_value=SimpleNamespace(args=["fixture"],returncode=0,stdout="fixture",stderr="")); self.run=p.start(); self.addCleanup(p.stop)
    def test_hash(self):
        self.assertEqual(r.blob(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
    def test_valid(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out): self.assertEqual(r.main(),0)
        self.assertEqual(json.loads(out.getvalue())["sandbox"],"NONE")
        self.run.assert_called_once()
    def test_revision(self):
        self.rev.return_value="wrong"
        with self.assertRaisesRegex(ValueError,"revision mismatch"): r.main()
        self.run.assert_not_called()
    def test_register(self):
        (self.root/"records/math/results.json").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"source mismatch"): r.main()
        self.run.assert_not_called()
    def test_certificate(self):
        (self.root/"tools/space_prob.py").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"source mismatch"): r.main()
        self.run.assert_not_called()
    def test_symlink(self):
        p=self.root/"tools/space_prob.py"; p.unlink(); p.symlink_to(self.root/"records/math/results.json")
        with self.assertRaisesRegex(ValueError,"source mismatch"): r.main()
        self.run.assert_not_called()
if __name__=="__main__": unittest.main()
