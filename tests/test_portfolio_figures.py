import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts' / 'build_portfolio_figures.py'


class PortfolioFiguresTest(unittest.TestCase):
    def generator(self):
        self.assertTrue(GENERATOR.exists(), 'Reproducible portfolio figure builder is missing')
        spec = importlib.util.spec_from_file_location('figures', GENERATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_checked_aggregate_estimates_are_loaded(self):
        module = self.generator()
        rows = module.load_results(ROOT / 'results' / 'aggregate_stove_associations.csv')
        self.assertEqual(len(rows), 16)
        self.assertEqual({row['n'] for row in rows}, {179})
        example = next(row for row in rows if row['pollutant'] == 'PM2.5' and row['window'] == 'Cooking period' and row['model'] == 'Selected')
        self.assertAlmostEqual(example['ratio'], 0.6463030142352, places=12)
        self.assertAlmostEqual(example['lower'], 0.536519558768166, places=12)
        self.assertAlmostEqual(example['upper'], 0.778550528835426, places=12)
        self.assertEqual({row['pollutant'] for row in rows}, {'PM10', 'PM2.5', 'PM1', 'CO'})

    def test_figures_are_nonblank_and_text_does_not_overlap(self):
        from PIL import Image
        module = self.generator()
        with tempfile.TemporaryDirectory() as directory:
            reports = module.build_figures(ROOT / 'results' / 'aggregate_stove_associations.csv', Path(directory))
            self.assertEqual(set(reports), {'research-overview.png', 'adjusted-associations.png', 'adjustment-sensitivity.png', 'analysis-workflow.png'})
            for filename, report in reports.items():
                image = Image.open(Path(directory) / filename)
                self.assertGreaterEqual(image.width, 2000)
                self.assertGreater(len(image.getcolors(image.width * image.height)), 50)
                boxes = report['text_boxes']
                for index, (label, box) in enumerate(boxes):
                    left, top, right, bottom = box
                    self.assertGreaterEqual(left, 0, label)
                    self.assertGreaterEqual(top, 0, label)
                    self.assertLessEqual(right, report['width'], label)
                    self.assertLessEqual(bottom, report['height'], label)
                    for other_label, other in boxes[index+1:]:
                        overlap_width = min(right, other[2]) - max(left, other[0])
                        overlap_height = min(bottom, other[3]) - max(top, other[1])
                        self.assertFalse(overlap_width > 0 and overlap_height > 0, f'{filename}: {label} overlaps {other_label}')


if __name__ == '__main__':
    unittest.main()
