import random

def spin_slot_machine_logic(initial_money, stavka):
    symbols = [1, 2, 3, 4, 5, 6, 7, 'w', 'b']
    weights = [100, 100, 100, 100, 50, 50, 20, 5, 200]

    l1 = [random.choices(symbols, weights=weights)[0] for _ in range(3)]
    l2 = [random.choices(symbols, weights=weights)[0] for _ in range(3)]
    l3 = [random.choices(symbols, weights=weights)[0] for _ in range(3)]

    winning_combinations = [
        [0, 0, 0], [1, 1, 1], [2, 2, 2], [0, 1, 2], [2, 1, 0],
        [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 2, 1], [1, 1, 0],
        [1, 1, 2], [2, 2, 1], [2, 1, 2]
    ]

    money = initial_money - stavka
    winning_lines = []
    multiplier = 0

    bonus_count = sum([l1.count('b'), l2.count('b'), l3.count('b')])

    if bonus_count >= 3:
        bonus_spins = {3: 8, 4: 10, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12}.get(bonus_count, 0)
        return {
            "l1": l1,
            "l2": l2,
            "l3": l3,
            "money": money,
            "winning_lines": None,
            "multiplier": None,
            "message": bonus_spins
        }
    
    def check_and_replace(f, s, t):
        nonlocal money, multiplier
        symbols_set = {l1[f], l2[s], l3[t]}
        if len(symbols_set) == 1 or ('w' in symbols_set and len(symbols_set) == 2):
            winning_lines.append((f, s, t))
            main_symbol = (symbols_set - {'w'}).pop() if 'w' in symbols_set else l1[f]
            if main_symbol == 'w':
                multiplier += 10
            elif main_symbol in [5, 6]:
                multiplier += 2
            elif main_symbol == 7:
                multiplier += 8
            else:
                multiplier += 1.3
            money += int(stavka * multiplier)

    for comb in winning_combinations:
        check_and_replace(comb[0], comb[1], comb[2])

    return {
        "l1": l1,
        "l2": l2,
        "l3": l3,
        "money": money,
        "winning_lines": winning_lines,
        "multiplier": multiplier
    }
