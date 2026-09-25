class ClosestStrikeSelector:
    def __init__(self, max_distance):
        self.max_distance = max_distance

    def select(self, spot, candidates):
        eligible = [c for c in candidates if abs(spot - c['strike']) < self.max_distance]
        return min(eligible, key=lambda c: abs(spot - c['strike'])) if eligible else None
