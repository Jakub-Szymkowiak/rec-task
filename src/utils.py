import numpy as np

def get_random_subsets(data_size: int, subset_size: int=2):
    remainder = data_size % subset_size
    remaining_indeces = list(range(data_size))

    # drop redundant indeces
    if remainder != 0:
        for _ in range(remainder):
            to_drop = np.random.randint(0, len(remaining_indeces))
            remaining_indeces.pop(to_drop)
        
    subsets = [] 
    while len(remaining_indeces) > 0:
        subset = []
        for _ in range(subset_size):
            selection_idx = np.random.randint(0, len(remaining_indeces))
            subset.append(remaining_indeces[selection_idx])
            remaining_indeces.pop(selection_idx)
        
        subsets.append(subset)

    return subsets

class Color():
    def __init__(self, r: int, g: int, b: int):
        for c in [r,g,b]:
            assert(0 <= c <= 255)
        
        self.r = r
        self.g = g
        self.b = b

    def to_str(self):
        return f"rgb({self.r}, {self.g}, {self.b})"

class ColorUtils:
    RED  = Color(255, 0, 0  )
    BLUE = Color(0,   0, 255)

    color_normalization_const = np.sqrt(255**2 * 3)

    def __avg(x, y):
        return (x + y) / 2

    def get_random_color():
        rc = lambda: np.random.randint(0, 255+1)
        return Color(rc(), rc(), rc())

    def get_color_avg(c1: Color, c2: Color):
        r = ColorUtils.__avg(c1.r, c2.r)
        g = ColorUtils.__avg(c1.g, c2.g)
        b = ColorUtils.__avg(c1.b, c2.b)
        return Color(int(r), int(g), int(b))

    def compare_colors(c1: Color, c2: Color):
        r_cond = c1.r == c2.r
        g_cond = c1.g == c2.g
        b_cond = c1.b == c2.b
        return r_cond and g_cond and b_cond

    def normalized_sRGB(c1: Color, c2: Color):
        delta_r = c1.r - c2.r
        delta_g = c1.g - c2.g
        delta_b = c1.b - c2.b

        delta_sq = [delta_r**2, delta_g**2, delta_b**2]
        delta_sq_sum = sum(delta_sq)

        return np.sqrt(delta_sq_sum) / ColorUtils.color_normalization_const

    def single_color_comp(c1: Color, c2: Color):
        cl1 = [c1.r, c1.g, c1.b]
        cl2 = [c2.r, c2.g, c2.b]
        if cl1 > cl2:
            return 1
        elif cl1 < cl2:
            return -1
        else:
            return 0
        