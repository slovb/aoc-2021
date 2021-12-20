from __future__ import annotations
from itertools import combinations, permutations, product
from typing import Callable


flatten = lambda d: sum([abs(v) for v in d])

def difference(a, b):
    return tuple([b[i] - a[i] for i in range(3)])


def generate_rotators():
    for a,b,c in product([-1, 1], repeat=3):
        for i,j,k in permutations([0, 1, 2]):
            yield lambda d: tuple([a*d[i], b*d[j], c*d[k]])


class Scanner:
    def __init__(self, id, beacons) -> None:
        self.id = id
        self.beacons = []
        self.vectors = []
        self.distances = []
        for b in beacons:
            self.add(b)

    def add(self, beacon):
        if beacon in self.beacons:
            return
        for b in self.beacons:
            d = difference(b, beacon)
            self.vectors.append(d)
            self.distances.append(flatten(d))
        self.beacons.append(beacon)
        self.vectors = sorted(self.vectors, key=flatten)
        self.distances = sorted(self.distances)

    def distance_score(self, scanner: Scanner) -> int:
        total = 0
        i, j = 0, 0
        while i < len(self.distances) and j < len(scanner.distances):
            a, b = self.distances[i], scanner.distances[j]
            if a == b:
                i += 1
                j += 1
                total += 1
            elif a < b:
                i += 1
            else:
                j += 1
        return total

    def rot_score(self, scanner: Scanner, rotator: Callable) -> int:
        # This is not the way to score this, TODO FIX
        rotated = [rotator(d) for d in scanner.vectors]
        return len([d for d in rotated if d in self.vectors])
    
    def find_rotator(self, scanner: Scanner) -> callable:
        best_score = -1
        best_rotator = None
        for r in generate_rotators():
            score = self.rot_score(scanner, r)
            if score > best_score:
                best_score = score
                best_rotator = r
        print('{} best rotation: {}'.format(scanner.id, best_score))
        return best_rotator
    
    def align_beacons(self, beacons) -> list:
        # TODO after rotations are fixed
        return beacons
    
    def __str__(self) -> str:
        output = ['---  scanner {}  ---'.format(self.id)]
        for b in self.beacons:
            output.append(' ' + ''.join([str(v).rjust(5) for v in b]))
        return '\n'.join(output)


def solve(scanners: list[Scanner]):
    constellation = scanners.pop(0)
    print(constellation)
    print('')
    
    while len(scanners) > 0:
        best_score = 0
        best_scanner = None
        for scanner in scanners:
            score = constellation.distance_score(scanner)
            if score > best_score:
                best_score = score
                best_scanner = scanner
        scanners.remove(best_scanner)
        rotator = constellation.find_rotator(best_scanner)
        aligned_beacons = constellation.align_beacons([rotator(b) for b in best_scanner.beacons])     
        for b in aligned_beacons:
            constellation.add(b)
        print(constellation)
        print('')
        
    return len(constellation.beacons)


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        scanners = []
        beacons = []
        id = 0
        for row in rows:
            if '---' in row:
                continue
            if row == '':
                scanners.append(Scanner(id, beacons))
                id += 1
                beacons = []
            else:
                beacons.append(tuple([int(v) for v in row.split(',')]))
            
        return scanners


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import time
    start_time = time.time()
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
    print('--- %s seconds ---' % (time.time() - start_time))