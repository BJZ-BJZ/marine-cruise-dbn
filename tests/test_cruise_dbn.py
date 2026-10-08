"""Cruise DBN: verification entry points must refuse to run with assertions disabled."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = ['src/verify.py']

class VerificationGuards(unittest.TestCase):
    def test_optimized_entry_points_refuse_to_report_success(self):
        for rel in SCRIPTS:
            path = ROOT / rel
            with self.subTest(path=rel):
                result = subprocess.run([sys.executable, '-O', str(path)],
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Verification requires assertions', result.stderr)


class Contracts(unittest.TestCase):
    def setUp(self):
        import importlib.util
        import numpy as np
        self.np = np
        spec = importlib.util.spec_from_file_location('dbn', ROOT / 'src/dbn.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.m = module

    def test_dbn_unknown_speed_rejected(self):
        with self.assertRaises(ValueError):
            self.m.ConditionalDBN().fit([(0, 0, 0, 1)]).predict(2, 0, 0)

    def test_brier_extremes(self):
        self.assertEqual(self.m.brier([1, 0, 0], 0), 0)
        self.assertEqual(self.m.brier([0, 1, 0], 2), 2)

    def test_dbn_rejects_invalid_prediction_states(self):
        model = self.m.ConditionalDBN().fit([(0, 0, 0, 1)])
        for values in [(0, 2, 0), (0, 0, -1), (3, 0, 0), (0, float('nan'), 0)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                model.predict(*values)
        with self.assertRaises(ValueError):
            self.m.ConditionalDBN().predict(0, 0, 0)
        self.assertEqual(model.predict(0, 1, 1), ([0., 1., 0.], True))

if __name__ == '__main__':
    unittest.main()
