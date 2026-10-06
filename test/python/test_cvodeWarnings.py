"""Regression test for #1316: CVODE "t + h = t" warnings bypassed the RoadRunner Logger
(and were printed to stdout) after the move to SUNDIALS 7.

The warning is written by SUNDIALS at the OS level, so the simulation is run in a
subprocess and its stdout/stderr are inspected. The number of warnings that an
unfixed build prints varies from run to run, so only "zero" is ever asserted.
"""
import os
import subprocess
import sys
import unittest

thisDir = os.path.dirname(os.path.realpath(__file__))
rr_site_packages = os.path.dirname(os.path.dirname(thisDir))

sys.path += [
    rr_site_packages,
]

MODEL = os.path.join(thisDir, "cvode_hnil_warnings.xml")

CHILD = r"""
import sys
sys.path += [sys.argv[3]]
import roadrunner
level = sys.argv[2]
if level != "default":
    roadrunner.Logger.setLevel(getattr(roadrunner.Logger, level))
r = roadrunner.RoadRunner(open(sys.argv[1]).read())
r.integrator = "cvode"
r.integrator.variable_step_size = True
r.integrator.absolute_tolerance = 1e-12
r.integrator.relative_tolerance = 1e-10
res = r.simulate(613190, 613210, 5)
print("RESULT", " ".join(repr(float(x)) for x in res[-1]))
"""


class CVODEWarningTests(unittest.TestCase):

    def run_model(self, level: str):
        p = subprocess.run([sys.executable, "-c", CHILD, MODEL, level, rr_site_packages],
                           capture_output=True, text=True)
        self.assertEqual(0, p.returncode, p.stderr)
        lines = (p.stdout + p.stderr).splitlines()
        warnings = [l for l in lines if "[WARNING]" in l]
        result = [l for l in lines if l.startswith("RESULT")]
        self.assertEqual(1, len(result), p.stdout + p.stderr)
        return warnings, [float(v) for v in result[0].split()[1:]]

    def test_no_cvode_warnings_at_any_level(self):
        for level in ("default", "LOG_ERROR", "LOG_FATAL", "LOG_WARNING"):
            for _ in range(3):  # the unfixed build is not deterministic in how many lines it prints
                with self.subTest(level=level):
                    warnings, _ = self.run_model(level)
                    self.assertEqual([], warnings)

    def test_results_unchanged(self):
        # This model is numerically pathological (CVODE steps of ~1e-45 around three events
        # at t ~ 6e5), and even before the warnings were disabled a given build gave one of
        # two final rows, apparently at random from run to run (measured with libroadrunner
        # 2.9.0 and 2.10.0; 2.8.0 and 2.10.0 are reported to give the first). Disabling the
        # warnings must not produce a third result.
        known = [[613210.0, 0.005, 10.000045424505819],
                 [613210.0, 1.9705791265204408e-76, 0.04093358273117023]]
        for _ in range(3):
            _, row = self.run_model("default")
            self.assertTrue(any(all(abs(e - a) <= 1e-8 * max(1.0, abs(e)) for e, a in zip(k, row))
                                for k in known), row)


if __name__ == '__main__':
    unittest.main()
