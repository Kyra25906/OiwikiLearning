"""Compile the course and compare examples against independent small-case oracles.

Python 3.10+, standard library only. Run: python scripts/check.py [--cxx g++]
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / '.build'
SEED = 20261006
TRIALS = 24


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_documents(sources, cases):
    chapters = sorted((ROOT / 'chapters').glob('*.md'))
    require(len(chapters) == len(sources) == 18, 'Expected 18 chapters and 18 programs')
    samples = {c['example']: c for c in cases if c['name'].endswith('-sample')}
    for source in sources:
        chapter = ROOT / 'chapters' / (source.stem + '.md')
        content = chapter.read_text(encoding='utf-8')
        snippets = re.findall(r'```cpp\n(.*?)\n```', content, re.S)
        require(len(snippets) == 1, f'{chapter.name}: expected one full program')
        require(snippets[0].strip() == source.read_text(encoding='utf-8').strip(),
                f'{chapter.name}: embedded code differs from source')
        sample = samples[source.stem]
        for heading, field in [('样例输入', 'input'), ('样例输出', 'expected')]:
            found = re.search(r'### ' + heading + r'\s+```text\n(.*?)\n```', content, re.S)
            require(found is not None and found[1].split() == sample[field].split(),
                    f'{chapter.name}: {heading} differs from test case')
        for heading in ['先修知识', '分层练习', '参考答案与思路', '过关标准', '对照阅读']:
            require(heading in content, f'{chapter.name}: missing {heading}')
    links = 0
    for doc in ROOT.rglob('*.md'):
        if '.build' in doc.parts or '.git' in doc.parts:
            continue
        content = doc.read_text(encoding='utf-8')
        # C++ lambdas such as [](args) are code, not Markdown links.
        content = re.sub(r'```.*?```', '', content, flags=re.S)
        content = re.sub(r'`[^`\n]*`', '', content)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            if re.match(r'[a-zA-Z]+:', target):
                continue
            name, _, fragment = unquote(target).partition('#')
            path = (doc.parent / name).resolve() if name else doc
            require(path.is_relative_to(ROOT.resolve()), f'{doc.name}: link escapes repository')
            require(path.is_file(), f'{doc.name}: missing target {target}')
            if fragment:
                headings = re.findall(r'^#+\s+(.+)$', path.read_text(encoding='utf-8'), re.M)
                anchors = [re.sub(r'[^\w\-\s]', '', h.lower()).replace(' ', '-') for h in headings]
                require(fragment in anchors, f'{doc.name}: missing anchor {target}')
            links += 1
    return links


def line(values):
    return ' '.join(map(str, values)) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'g++'))
    args = parser.parse_args()
    compiler = shutil.which(args.cxx)
    require(compiler is not None, f'C++ compiler not found: {args.cxx}')
    BUILD.mkdir(exist_ok=True)
    sources = sorted((ROOT / 'examples').glob('*.cpp'))
    cases = json.loads((ROOT / 'tests' / 'cases.json').read_text(encoding='utf-8'))
    links = check_documents(sources, cases)
    executables = {}
    for source in sources:
        output = BUILD / (source.stem + ('.exe' if os.name == 'nt' else ''))
        command = [compiler, '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                   str(source), '-o', str(output)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        require(result.returncode == 0, f'Compile failed: {source.name}\n{result.stderr}')
        executables[source.stem] = output
        print(f'Compiled {source.stem}', flush=True)

    counts = dict(fixed=0, randomized=0, scale=0)
    def run(slug, data):
        result = subprocess.run([str(executables[slug])], input=data, text=True,
                                capture_output=True, timeout=10)
        require(result.returncode == 0, f'{slug} exited {result.returncode}: {result.stderr}')
        return result.stdout.split()

    def check(slug, data, expected, category='randomized'):
        actual, wanted = run(slug, data), str(expected).split()
        require(actual == wanted,
                f'{slug} mismatch\nInput:\n{data[:4000]}\nExpected: {wanted[:150]}\nActual: {actual[:150]}')
        counts[category] += 1

    for case in cases:
        check(case['example'], case['input'], case['expected'], 'fixed')
    print(f'Passed {counts["fixed"]} fixed sample/boundary cases', flush=True)

    rng = random.Random(SEED)
    for _trial in range(TRIALS):
        a = [rng.randint(-10**9, 10**9) for _ in range(rng.randint(1, 15))]
        check('01-cpp-toolkit', f'{len(a)}\n'+line(a), f'{sum(a)} {max(a)} {a.count(max(a))}')

        a = [rng.randint(-5, 5) for _ in range(rng.randint(0, 18))]
        target = rng.randint(-8, 8)
        pairs = sum(x+y == target for x,y in itertools.combinations(a, 2))
        data = f'{len(a)} {target}\n'+line(a)
        check('02-enumeration-complexity', data, pairs)
        check('07-two-pointers', data, pairs)

        commands = ''.join(rng.choice('LRF') for _ in range(rng.randint(1, 60)))
        position, direction = 0j, 1j
        for command in commands:
            if command == 'L': direction *= 1j
            elif command == 'R': direction *= -1j
            else: position += direction
        name = {1j:'N', 1+0j:'E', -1j:'S', -1+0j:'W'}[direction]
        check('03-simulation', commands+'\n', f'{int(position.real)} {int(position.imag)} {name}')

        intervals = []
        for _ in range(rng.randint(0, 9)):
            l = rng.randint(-5, 7)
            intervals.append((l, l+rng.randint(1, 5)))
        best = 0
        for mask in range(1 << len(intervals)):
            chosen = sorted(e for i,e in enumerate(intervals) if mask >> i & 1)
            if all(chosen[i-1][1] <= chosen[i][0] for i in range(1, len(chosen))):
                best = max(best, len(chosen))
        check('04-sorting-greedy', f'{len(intervals)}\n'+''.join(f'{l} {r}\n' for l,r in intervals), best)

        n, m, q = rng.randint(1, 15), rng.randint(0, 10), rng.randint(1, 10)
        a = [rng.randint(-20, 20) for _ in range(n)]
        data = f'{n} {m} {q}\n'+line(a)
        for _ in range(m):
            l = rng.randrange(n)
            r, v = rng.randrange(l, n), rng.randint(-20, 20)
            data += f'{l+1} {r+1} {v}\n'
            for i in range(l, r+1): a[i] += v
        answers = []
        for _ in range(q):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            data += f'{l+1} {r+1}\n'
            answers.append(sum(a[l:r+1]))
        check('05-prefix-difference', data, line(answers))

        a = sorted(rng.randint(-8, 8) for _ in range(rng.randint(0, 20)))
        queries = [rng.randint(-12, 12) for _ in range(12)]
        answers = [next((i for i,v in enumerate(a) if v >= x), len(a)) for x in queries]
        check('06-binary-search', f'{len(a)} {len(queries)}\n'+line(a)+line(queries), line(answers))

        a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 10))]
        target = rng.randint(-7, 7)
        answer = sum(sum(part) == target for k in range(len(a)+1) for part in itertools.combinations(a,k))
        check('08-recursion-dfs', f'{len(a)} {target}\n'+line(a), answer)

        h, w = rng.randint(1, 5), rng.randint(1, 5)
        grid = [''.join('#' if rng.random() < .3 else '.' for _ in range(w)) for _ in range(h)]
        # Independent oracle: repeated synchronous edge relaxation, not BFS.
        infinity = h*w+1
        distance = [infinity]*(h*w)
        if grid[0][0] == '.': distance[0] = 0
        edges = []
        for r in range(h):
            for c in range(w):
                if grid[r][c] == '#': continue
                for nr,nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    if 0<=nr<h and 0<=nc<w and grid[nr][nc] == '.':
                        edges.append((r*w+c,nr*w+nc))
        for _ in range(h*w):
            old = distance.copy()
            for u,v in edges: distance[v] = min(distance[v], old[u]+1)
        answer = distance[-1] if distance[-1] < infinity else -1
        check('09-bfs', f'{h} {w}\n'+'\n'.join(grid)+'\n', answer)

        a = [rng.randint(-4, 4) for _ in range(rng.randint(0, 10))]
        answer = max((len(part) for k in range(len(a)+1) for part in itertools.combinations(a,k)
                      if all(part[i-1] < part[i] for i in range(1,len(part)))), default=0)
        check('10-dp-basics', f'{len(a)}\n'+line(a), answer)

        items = [(rng.randint(1, 8),rng.randint(0, 30)) for _ in range(rng.randint(0, 9))]
        capacity, best = rng.randint(0, 18), 0
        for mask in range(1 << len(items)):
            weight = sum(w for i,(w,v) in enumerate(items) if mask >> i & 1)
            value = sum(v for i,(w,v) in enumerate(items) if mask >> i & 1)
            if weight <= capacity: best = max(best, value)
        check('11-knapsack', f'{len(items)} {capacity}\n'+''.join(f'{w} {v}\n' for w,v in items), best)

        n = rng.randint(1, 6)
        edges = [(rng.randrange(1,n+1),rng.randrange(1,n+1)) for _ in range(rng.randint(0,10))]
        # Enumerate orders, then validate the program's output semantically.
        possible = False
        for perm in itertools.permutations(range(1,n+1)):
            positions = {u:i for i,u in enumerate(perm)}
            if all(positions[u] < positions[v] for u,v in edges):
                possible = True
                break
        data = f'{n} {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges)
        out = run('12-graphs-toposort', data)
        if not possible:
            require(out == ['IMPOSSIBLE'], f'Topological cycle not detected: {data}')
        else:
            order = list(map(int,out))
            require(sorted(order) == list(range(1,n+1)), f'Invalid vertex permutation: {data} {out}')
            positions = {u:i for i,u in enumerate(order)}
            require(all(positions[u] < positions[v] for u,v in edges), f'Dependency violated: {data} {out}')
        counts['randomized'] += 1

        n = rng.randint(1,7)
        source = rng.randrange(1,n+1)
        edges = [(rng.randrange(1,n+1),rng.randrange(1,n+1),rng.randint(0,30))
                 for _ in range(rng.randint(0,20))]
        dist = [math.inf]*(n+1)
        dist[source] = 0
        for _ in range(n-1):
            old = dist.copy()
            for u,v,weight in edges: dist[v] = min(dist[v], old[u]+weight)
        answers = [-1 if x == math.inf else int(x) for x in dist[1:]]
        check('13-dijkstra', f'{n} {len(edges)} {source}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges), line(answers))

        n = rng.randint(1,5)
        edges = [(rng.randrange(1,n+1),rng.randrange(1,n+1),rng.randint(-8,15))
                 for _ in range(rng.randint(0,9))]
        best = math.inf
        # Enumerate n-1 edges and test reachability, without using DSU.
        for subset in itertools.combinations(edges,n-1):
            reached = {1}
            for _ in range(n):
                for u,v,_ in subset:
                    if u in reached or v in reached: reached.update((u,v))
            if len(reached) == n: best = min(best,sum(w for _,_,w in subset))
        answer = 'IMPOSSIBLE' if best == math.inf else str(best)
        check('14-dsu-mst', f'{n} {len(edges)}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges), answer)

        n, q = rng.randint(1,15), 25
        a = [rng.randint(-20,20) for _ in range(n)]
        data, answers = f'{n} {q}\n'+line(a), []
        for _ in range(q):
            if rng.random() < .5:
                i, delta = rng.randrange(n), rng.randint(-20,20)
                data += f'1 {i+1} {delta}\n'
                a[i] += delta
            else:
                l = rng.randrange(n)
                r = rng.randrange(l,n)
                data += f'2 {l+1} {r+1}\n'
                answers.append(sum(a[l:r+1]))
        check('15-fenwick', data, line(answers))

        a, b, p = rng.randint(0,10**9), rng.randint(0,10**18), rng.randint(1,10**9)
        check('16-number-theory', f'{a} {b} {p}\n', f'{math.gcd(a,b)}\n{pow(a,b,p)}')

        text = ''.join(rng.choice('abc') for _ in range(rng.randint(1,35)))
        pattern = ''.join(rng.choice('abc') for _ in range(rng.randint(1,10)))
        answers = [i for i in range(len(text)-len(pattern)+1) if text[i:i+len(pattern)] == pattern]
        check('17-kmp', text+'\n'+pattern+'\n', line(answers) if answers else '-1')

        cost = [rng.randint(0,15) for _ in range(rng.randint(0,10))]
        budgets = [rng.randint(0,60) for _ in range(8)]
        subsets = [(sum(part),len(part)) for k in range(len(cost)+1) for part in itertools.combinations(cost,k)]
        answers = [max(count for total,count in subsets if total <= budget) for budget in budgets]
        check('18-integration', f'{len(cost)} {len(budgets)}\n'+line(cost)+line(budgets), line(answers))

    print(f'Passed {counts["randomized"]} randomized oracle cases (seed={SEED})', flush=True)
    check('07-two-pointers', '200000 0\n'+'0 '*200000+'\n', 19999900000, 'scale')
    check('08-recursion-dfs', '20 0\n'+'0 '*20+'\n', 1048576, 'scale')
    check('17-kmp', 'a'*200000+'\n'+'a'*100000+'\n', line(range(100001)), 'scale')
    report = dict(compiler=subprocess.run([compiler,'--version'],capture_output=True,text=True).stdout.splitlines()[0],
                  cpp_standard='C++17', compiled=len(sources), local_links=links,
                  seed=SEED, trials_per_program=TRIALS, **counts)
    (BUILD / 'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    print('All checks passed. Local verification only; not an online-judge submission.')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, subprocess.TimeoutExpired, OSError, ValueError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
