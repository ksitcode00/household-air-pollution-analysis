"""Render portfolio figures from published aggregate estimates, never raw records."""

import argparse
import csv
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

INK = '#17272C'
TEAL = '#087F83'
CORAL = '#C45B4D'
MUTED = '#596970'
RULE = '#DAE3E5'
POLLUTANTS = ['PM10', 'PM2.5', 'PM1', 'CO']
SCALE = 2
FONT_DIR = Path('/System/Library/Fonts/Supplemental')


def font(size, bold=False, display=False):
    names = ['Georgia.ttf'] if display else ['Arial Bold.ttf' if bold else 'Arial.ttf']
    paths = [FONT_DIR / names[0], Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSerif.ttf' if display else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size * SCALE)
    return ImageFont.truetype('DejaVuSans.ttf', size * SCALE)


def load_results(path):
    rows = []
    with Path(path).open() as stream:
        records = list(csv.DictReader(stream))
    for row in records:
        row['n'] = int(row['n'])
        for key in ['ratio', 'lower', 'upper', 'p']:
            row[key] = float(row[key])
        assert row['pollutant'] in POLLUTANTS
        assert row['window'] in ['24-hour', 'Cooking period']
        assert row['model'] in ['Selected', 'Full background']
        assert row['n'] == 179
        assert all(math.isfinite(row[key]) for key in ['ratio', 'lower', 'upper', 'p'])
        assert 0 < row['lower'] < row['ratio'] < row['upper']
        assert 0 <= row['p'] <= 1
        rows.append(row)
    expected = {(p, w, m) for p in POLLUTANTS for w in ['24-hour', 'Cooking period'] for m in ['Selected', 'Full background']}
    assert len(rows) == 16 and {(r['pollutant'], r['window'], r['model']) for r in rows} == expected
    return rows


class Canvas:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.image = Image.new('RGB', (width * SCALE, height * SCALE), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.boxes = []

    def text(self, x, y, value, size=26, color=INK, bold=False, display=False, anchor='lt', max_width=None):
        face = font(size, bold, display)
        if max_width:
            while self.draw.textlength(value, font=face) > max_width * SCALE:
                size -= 1
                assert size >= 20, value
                face = font(size, bold, display)
        point = (x * SCALE, y * SCALE)
        box = self.draw.textbbox(point, value, font=face, anchor=anchor)
        self.boxes.append((value, tuple(v / SCALE for v in box)))
        self.draw.text(point, value, fill=color, font=face, anchor=anchor)

    def line(self, x1, y1, x2, y2, color=RULE, width=1):
        self.draw.line((x1*SCALE, y1*SCALE, x2*SCALE, y2*SCALE), fill=color, width=max(1, int(width*SCALE)))

    def rectangle(self, box, fill):
        self.draw.rectangle(tuple(v*SCALE for v in box), fill=fill)

    def interval(self, record, x1, x2, y, color, square=False):
        def project(value):
            assert .45 <= value <= 1.08
            return x1 + (value - .45) / .63 * (x2 - x1)
        lo, hi, center = [project(record[key]) for key in ['lower', 'upper', 'ratio']]
        self.line(lo, y, hi, y, color, 3)
        self.line(lo, y-6, lo, y+6, color, 2)
        self.line(hi, y-6, hi, y+6, color, 2)
        box = ((center-6)*SCALE, (y-6)*SCALE, (center+6)*SCALE, (y+6)*SCALE)
        if square:
            self.draw.rectangle(box, fill=color)
        else:
            self.draw.ellipse(box, fill=color)

    def axis(self, x1, x2, top, bottom, ticks=True):
        for value in [.5, .75, 1.0]:
            x = x1 + (value-.45)/.63 * (x2-x1)
            if value == 1:
                for y in range(int(top), int(bottom), 12):
                    self.line(x, y, x, min(y+6, bottom), MUTED, 1)
            else:
                self.line(x, top, x, bottom, RULE, 1)
            if ticks:
                self.text(x, bottom+18, f'{value:.2f}', 24, MUTED, anchor='mt')
        self.line(x1, bottom, x2, bottom, RULE, 1)

    def save(self, path):
        self.image.save(path, optimize=True)
        return {'width': self.width, 'height': self.height, 'text_boxes': self.boxes}


def overview(data):
    c = Canvas(1200, 980)
    c.text(64, 50, 'Environmental health research in rural Odisha', 25, TEAL)
    c.text(64, 102, 'Air Pollution Research Project', 60, display=True, max_width=1072)
    c.text(64, 204, 'Lower particle ratios during active cooking.', 38, bold=True, max_width=1072)
    c.text(64, 266, '180 households enrolled. 179 in the adjusted models.', 28, MUTED)
    c.line(64, 326, 1136, 326)
    c.line(275, 367, 302, 367, TEAL, 4)
    c.text(314, 351, 'Cooking period', 26, TEAL)
    c.line(541, 367, 568, 367, CORAL, 4)
    c.text(580, 351, '24-hour', 26, CORAL)
    c.text(952, 354, 'Cooking', 25, MUTED, anchor='mt')
    c.text(1080, 354, '24-hour', 25, MUTED, anchor='mt')
    c.axis(275, 805, 421, 780)
    for i, pollutant in enumerate(POLLUTANTS):
        y = 448 + i*88
        c.text(64, y-8, pollutant, 36, bold=True)
        for window, shift, color, x in [('Cooking period', 20, TEAL, 952), ('24-hour', -7, CORAL, 1080)]:
            row = data[pollutant, window, 'Selected']
            c.interval(row, 275, 805, y+shift, color)
            c.text(x, y-2, f"{row['ratio']:.3f}", 35, color, bold=True, anchor='mt')
    c.text(540, 829, 'Adjusted ratio of C+1; reference = traditional stove', 23, MUTED, anchor='mt')
    c.line(64, 875, 1136, 875)
    c.text(64, 901, 'Points and lines: estimates and HC3 95% confidence intervals.', 24, MUTED)
    c.text(64, 940, 'Observational associations, not causal effects or exact reductions in C.', 23, MUTED)
    return c


def associations(data):
    c = Canvas(1400, 1150)
    c.text(64, 50, 'Adjusted cookstove associations', 58, display=True, max_width=1272)
    c.text(64, 143, 'Four pollutants. Two exposure windows. Uncertainty shown for every estimate.', 28, MUTED, max_width=1272)
    c.line(64, 210, 1336, 210)
    for window, label, offset, color in [('24-hour', '24-hour averages', 0, CORAL), ('Cooking period', 'Cooking periods', 700, TEAL)]:
        c.text(64+offset, 247, label, 35, color, bold=True)
        c.axis(220+offset, 616+offset, 336, 892)
        for i, pollutant in enumerate(POLLUTANTS):
            y = 378 + i*132
            row = data[pollutant, window, 'Selected']
            c.text(64+offset, y-16, pollutant, 34, bold=True)
            c.interval(row, 220+offset, 616+offset, y, color)
            c.text(220+offset, y+34, f"{row['ratio']:.3f} ({row['lower']:.3f} to {row['upper']:.3f})", 26, color, max_width=416)
        c.text(418+offset, 947, 'Adjusted ratio of C+1', 25, MUTED, anchor='mt')
    c.line(64, 1001, 1336, 1001)
    c.text(64, 1028, 'IDES versus traditional. Selected log(C+1) models; n=179; HC3 95% CIs.', 26, MUTED, max_width=1272)
    c.text(64, 1072, 'The dashed line at 1 is the null. Ratios are not exact percentage reductions in C.', 25, MUTED, max_width=1272)
    c.text(64, 1110, 'Separate window estimates are not a formal test of a difference between windows.', 24, MUTED, max_width=1272)
    return c


def sensitivity(data):
    c = Canvas(1400, 1520)
    c.text(64, 50, 'Does full adjustment change the story?', 56, display=True, max_width=1272)
    c.text(64, 145, 'Compare selected models with every background term retained.', 30, MUTED, max_width=1272)
    c.line(64, 213, 1336, 213)
    c.line(64, 270, 93, 270, TEAL, 4)
    c.text(109, 254, 'Selected model', 27, TEAL)
    c.line(438, 270, 467, 270, CORAL, 4)
    c.text(483, 254, 'Full background', 27, CORAL)
    c.text(1120, 320, 'Selected', 24, MUTED, anchor='mt')
    c.text(1280, 320, 'Full', 24, MUTED, anchor='mt')
    c.axis(405, 982, 366, 1302)
    for i, (window, pollutant) in enumerate((w,p) for w in ['24-hour', 'Cooking period'] for p in POLLUTANTS):
        y = 400 + i*112
        c.text(64, y-1, pollutant, 33, bold=True)
        c.text(64, y+39, window, 25, MUTED)
        for model, shift, color, x in [('Selected', 7, TEAL, 1120), ('Full background', 40, CORAL, 1280)]:
            row = data[pollutant, window, model]
            c.interval(row, 405, 982, y+shift, color, square=model=='Full background')
            c.text(x, y+9, f"{row['ratio']:.3f}", 31, color, bold=True, anchor='mt')
        if i == 3:
            c.line(64, y+93, 335, y+93)
    c.text(694, 1355, 'Adjusted ratio of C+1 with HC3 95% confidence intervals', 25, MUTED, anchor='mt')
    c.line(64, 1406, 1336, 1406)
    c.text(64, 1430, 'Same 179 households. All nine terms retained in the full-background models.', 25, MUTED, max_width=1272)
    c.text(64, 1474, 'Nominal inference; CO evidence is close to 0.05. Neither model establishes causality.', 24, MUTED, max_width=1272)
    return c


def workflow():
    c = Canvas(1400, 1190)
    c.text(64, 50, 'From household data to evidence', 58, display=True, max_width=1272)
    c.text(64, 148, 'An end-to-end R workflow with a clear interpretation boundary.', 30, MUTED)
    c.line(64, 214, 1336, 214)
    c.text(64, 248, 'Study cohort', 28, bold=True)
    c.rectangle((64, 307, 823, 343), TEAL)
    split = 64 + 759*105/180
    c.rectangle((split, 307, 823, 343), CORAL)
    c.text(64, 370, '105 IDES households', 26, TEAL)
    c.text(505, 370, '75 traditional-stove households', 24, CORAL, max_width=340)
    c.line(928, 247, 928, 411)
    c.text(1000, 246, '179', 80, display=True)
    c.text(1000, 359, 'Complete-case models', 26, MUTED, max_width=336)
    stages = [
        ('Clean and encode', ['Survey categories', 'Explicit reference groups', 'Fixed complete-case sample']),
        ('Explore', ['Tables and subgroup views', 'Distributions and Q-Q plots', 'Separate exposure windows']),
        ('Model', ['Eight log(C+1) regressions', 'Forced + backward selection', 'Full-background sensitivity']),
        ('Check and interpret', ['Residuals and influence', 'GVIF and HC3 uncertainty', 'Association, not causation']),
    ]
    for i, (title, lines) in enumerate(stages):
        x = 64 + i*328
        c.line(x, 484, x+252, 484, TEAL if i%2==0 else CORAL, 3)
        c.text(x, 523, title, 28, bold=True, max_width=288)
        for j, value in enumerate(lines):
            c.text(x, 582+j*46, value, 24, MUTED, max_width=288)
        if i < 3:
            c.line(x+270, 484, x+302, 484, MUTED, 2)
            c.line(x+295, 479, x+302, 484, MUTED, 2)
            c.line(x+295, 489, x+302, 484, MUTED, 2)
    c.line(64, 768, 1336, 768)
    c.text(64, 808, 'Exploratory extensions', 34, display=True)
    for x, title, detail in [(64, 'Logistic regression', 'Respiratory and lung-function outcomes'), (510, 'Mediation', 'Bootstrap pathway estimates'), (950, 'IPW sensitivity', 'Balance, weighting and E-values')]:
        c.text(x, 884, title, 29, bold=True)
        c.text(x, 934, detail, 24, MUTED, max_width=386)
    c.text(64, 1031, 'The extensions above are separate from the eight revised pollutant estimates.', 26, MUTED, max_width=1272)
    c.text(64, 1080, 'Restricted household data stay private. Public figures use aggregate estimates only.', 25, MUTED, max_width=1272)
    c.text(64, 1128, 'Cross-sectional observational research; not a randomized intervention.', 25, MUTED)
    return c


def build_figures(source, destination):
    rows = load_results(source)
    data = {(r['pollutant'], r['window'], r['model']): r for r in rows}
    destination.mkdir(parents=True, exist_ok=True)
    drawings = {'research-overview.png': overview(data), 'adjusted-associations.png': associations(data), 'adjustment-sensitivity.png': sensitivity(data), 'analysis-workflow.png': workflow()}
    return {name: canvas.save(destination / name) for name, canvas in drawings.items()}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=root / 'results' / 'aggregate_stove_associations.csv')
    parser.add_argument('--output', type=Path, default=root / 'figures')
    args = parser.parse_args()
    reports = build_figures(args.source, args.output)
    print('Rendered ' + ', '.join(reports))
