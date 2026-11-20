"""Independent check of the converter's unit table (records/units/units.json).

Each factor is derived here from the unit's legal definition, in exact rational arithmetic, without reading the stored
factor; the stored factor must then equal it (exactly where the unit is exact, to 1e-15 relative for pi). Round trips and
fixtures with known answers are checked as well. Run: python3 site/test/units_check.py
"""
import json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAB = json.load(open(os.path.join(ROOT, 'records', 'units', 'units.json'), encoding='utf-8'))

inch = F('0.0254'); ft = 12 * inch; yd = 3 * ft; mi = 1760 * yd
lb = F('0.45359237'); g0 = F('9.80665'); lbf = lb * g0
c = 299792458; julian = F(36525, 100) * 86400; nmi = 1852
galUS = 231 * inch ** 3; galUK = F('4.54609') / 1000; atm = 101325
DERIVED = {
 'm': 1, 'km': 1000, 'cm': F(1, 100), 'mm': F(1, 1000), 'um': F(1, 10**6), 'nm': F(1, 10**9), 'in': inch, 'ft': ft, 'yd': yd, 'mi': mi, 'nmi': nmi,
 'au': 149597870700, 'ly': c * julian,
 'kg': 1, 'g': F(1, 1000), 'mg': F(1, 10**6), 't': 1000, 'lb': lb, 'oz': lb / 16, 'st': 14 * lb,
 's': 1, 'ms': F(1, 1000), 'us': F(1, 10**6), 'min': 60, 'h': 3600, 'd': 86400, 'wk': 7 * 86400, 'a': julian,
 'm2': 1, 'km2': 10**6, 'ha': 10**4, 'ft2': ft ** 2, 'acre': 4840 * yd ** 2, 'mi2': mi ** 2,
 'm3': 1, 'L': F(1, 1000), 'mL': F(1, 10**6), 'in3': inch ** 3, 'ft3': ft ** 3, 'galUS': galUS, 'ptUS': galUS / 8, 'flozUS': galUS / 128,
 'galUK': galUK, 'ptUK': galUK / 8, 'flozUK': galUK / 160,
 'm/s': 1, 'km/h': F(1000, 3600), 'mph': mi / 3600, 'kn': F(nmi, 3600), 'ft/s': ft, 'c': c,
 'N': 1, 'kN': 1000, 'dyn': F(1, 10**5), 'kgf': g0, 'lbf': lbf,
 'J': 1, 'kJ': 1000, 'erg': F(1, 10**7), 'cal': F('4.184'), 'kcal': 4184, 'Wh': 3600, 'kWh': 3600000, 'eV': F('1.602176634e-19'), 'BTU': F('1055.05585262'),
 'W': 1, 'kW': 1000, 'MW': 10**6, 'hp': 550 * ft * lbf, 'PS': 75 * g0,
 'Pa': 1, 'kPa': 1000, 'bar': 10**5, 'atm': atm, 'torr': F(atm, 760), 'mmHg': F('13.5951') * 1000 * g0 / 1000, 'psi': lbf / inch ** 2,
 'Hz': 1, 'kHz': 1000, 'MHz': 10**6, 'GHz': 10**9, 'rpm': F(1, 60),
 'rad': 1, 'deg': math.pi / 180, 'arcmin': math.pi / 10800, 'arcsec': math.pi / 648000, 'turn': 2 * math.pi,
}


def stored(s):
    s = s.replace('pi', repr(math.pi))
    if any(ch in s for ch in '*') or 'e+' in s or repr(math.pi) in s:
        return eval(s, {'__builtins__': {}})
    if '/' in s:
        a, b = s.split('/'); return F(a) / F(b)
    return F(s)


def main():
    bad = 0; n = 0
    for q in TAB['quantities']:
        for u in q['units']:
            sym = u[0]
            if q.get('affine'):
                continue
            want, got = DERIVED[sym], stored(u[2]); n += 1
            if isinstance(want, float) or isinstance(got, float):
                ok = abs(float(got) - float(want)) <= 1e-15 * abs(float(want))
            else:
                ok = F(got) == F(want)
                if not ok and sym in ('hp', 'psi', 'lbf'):   # stored to 17 significant digits; the exact value is longer
                    ok = abs(F(got) - F(want)) <= F(1, 10**14) * F(want)
            if not ok:
                bad += 1; print('MISMATCH', q['q'], sym, u[2], float(want))
    # temperature, by definition
    t = {u[0]: (stored(u[2]), stored(u[3])) for u in next(q for q in TAB['quantities'] if q['q'] == 'Temperature')['units']}
    K = lambda sym, x: (F(x) + t[sym][1]) * t[sym][0]
    fixtures = [(K('degC', 100), F('373.15')), (K('degF', 32), F('273.15')), (K('degF', -40), K('degC', -40)), (K('degR', 0), 0), (K('degF', 212), K('degC', 100))]
    for got, want in fixtures:
        n += 1
        if got != want: bad += 1; print('MISMATCH temperature', got, want)
    # fixtures with known answers
    known = [('mi', 'km', 1, F('1.609344')), ('lb', 'kg', 1, F('0.45359237')), ('kWh', 'J', 1, 3600000), ('atm', 'psi', 1, None), ('galUS', 'L', 1, F('3.785411784'))]
    tables = {u[0]: stored(u[2]) for q in TAB['quantities'] if not q.get('affine') for u in q['units']}
    for a, b, x, want in known:
        n += 1; v = F(x) * F(tables[a]) / F(tables[b])
        if want is not None and v != want: bad += 1; print('MISMATCH fixture', a, b, v)
        if want is None and abs(float(v) - 14.6959487755) > 1e-9: bad += 1; print('MISMATCH fixture', a, b, float(v))
    print('UNITS: %d checks, %d mismatches | %s' % (n, bad, 'PASS' if not bad else 'FAIL'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
