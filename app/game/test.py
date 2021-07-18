import random
from itertools import groupby


def _vertical_key_func(coord):
    return coord[1]

def _horizontal_key_func(coord):
    return coord[0]


# def max_horizontal_points(_moves):
#     g_max = 0
#     for _, coords_on_one_horizont in groupby(_moves, key=_vertical_key_func):
#         coords_on_one_horizont = list(coords_on_one_horizont)
#         exp_coord, l_max = None, 0
#         for x in (c[0] for c in sorted(coords_on_one_horizont, key=_horizontal_key_func)):
#             if exp_coord == x:
#                 l_max += 1
#             else:
#                 if l_max > g_max:
#                     g_max = l_max
#                 l_max = 0
#             exp_coord = x + 1  
#     return g_max

# def max_vertical_points(_moves):
#     g_max = 0
#     for _, coords_on_one_horizont in groupby(_moves, key=_horizontal_key_func):
#         coords_on_one_horizont = list(coords_on_one_horizont)
#         exp_coord, l_max = None, 0
#         for x in (c[1] for c in sorted(coords_on_one_horizont, key=_vertical_key_func)):
#             if exp_coord == x:
#                 l_max += 1
#             else:
#                 if l_max > g_max:
#                     g_max = l_max
#                 l_max = 0
#             exp_coord = x + 1  
#     return g_max


def cc(_moves):
    moves_count = len(moves)
    g_max = moves_count if moves_count <= 1 else 0
    if len(_moves) >= 2:
        max_x = max(m[0] for m in _moves)
        min_x = min(m[0] for m in _moves)
        max_y = max(m[1] for m in _moves)
        min_y = min(m[1] for m in _moves)
        for m in _moves:
            hor_points = {(i, m[1]) for i in range(min_x, max_x + 1)}
            vertical_points = {(m[0], i) for i in range(min_y, max_y + 1)}
            diagonal_1_points = {(m[0] + i, m[1] + i) for i, _ in enumerate(range(m[0], max_x + 1))}.union({(m[0] - i, m[1] - i) for i, _ in enumerate(range(min_y, m[1] + 1))})
            diagonal_2_points = {(m[0] - i, m[1] + i) for i, _ in enumerate(range(min_x, m[0] + 1))}.union({(m[0] + i, m[1] - i) for i, _ in enumerate(range(m[0], max_x + 1))})
            print(f"HOR points: {hor_points}")
            print(f"Vertical points: {vertical_points}")
            print(f"D1: {diagonal_1_points}")
            print(f"D2: {diagonal_2_points}")
            iterables = (hor_points, vertical_points, diagonal_1_points, diagonal_2_points)
            for i in iterables:
                l_max = 0
                for point in i:
                    if point in _moves:
                        l_max += 1
                    else:
                        l_max = 0
                    if l_max > g_max:
                        g_max = l_max
    return g_max

if __name__ == "__main__":
    moves = [(0, 0), (0, 1), (0, 2), (1,6), (2,5), (3,4), (4,3), (6,1)]
    print(cc(moves))
