# btc-cent-forecast-01 entry: persistence, leaned on only when the case's own
# history agrees with itself. The guess is the checkpoint close plus the median
# 240-minute change over the 72 hours given, scaled by how consistently those
# changes share the median's sign (2*same-1, clamped to [0,1]): in a one-sided
# tape the lean is full, in a two-sided tape it vanishes and the guess is the
# close itself. Deterministic; standard library only.
import json
import os
import statistics

INPUT_DIR = os.environ.get('MAKEFUN_INPUT_DIR', '/input')
OUTPUT_DIR = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
MIN_PRICE = 0.00001
MAX_PRICE = 9999999.99999
H = 240


def price5(x):
    return round(min(MAX_PRICE, max(MIN_PRICE, x)) * 1e5) / 1e5 + 0.0


def guess(prices):
    x = prices[-1]
    if len(prices) <= H:
        return price5(x)
    ch = [prices[i + H] - prices[i] for i in range(len(prices) - H)]
    med = statistics.median(ch)
    if med == 0:
        return price5(x)
    same = sum(1 for c in ch if (c > 0) == (med > 0)) / len(ch)
    k = max(0.0, min(1.0, 2 * same - 1))
    return price5(x + k * med)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in sorted(os.listdir(INPUT_DIR)):
        if not name.endswith('.in'):
            continue
        cid = name[:-3]
        try:
            with open(os.path.join(INPUT_DIR, name)) as f:
                case = json.load(f)
            price = guess(case['markets'][0]['prices'])
        except Exception:
            price = 1.0  # never leave a case invalid over a parse surprise
        with open(os.path.join(OUTPUT_DIR, cid + '.out'), 'w') as f:
            f.write(json.dumps({'forecasts': [{'case': cid, 'price': price}]}) + '\n')


if __name__ == '__main__':
    main()
