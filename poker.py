#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

from typing import Iterable
import itertools
from collections import Counter


def hand_rank(hand: Iterable[str]):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand: Iterable[str]):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    rank_map = "23456789TJQKA"
    return sorted([rank_map.index(card[0]) for card in hand], reverse=True)


def flush(hand: Iterable[str]):
    """Возвращает True, если все карты одной масти"""
    return all([card[1] == hand[0][1] for card in hand])


def straight(ranks: Iterable[str]):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    for l_rank, r_rank in itertools.pairwise(ranks):
        if l_rank - r_rank != 1:
            return False
    return True


def kind(n: int, ranks: Iterable[int]):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    ranks_counts = Counter(ranks)
    for rank in ranks_counts:
        if ranks_counts[rank] == n:
            return rank
    return None


def two_pair(ranks: Iterable[int]):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    ranks_counts = Counter(ranks)
    most_common_ranks = ranks_counts.most_common(2)
    if most_common_ranks[0][1] == most_common_ranks[1][1]:
        return most_common_ranks[0][0], most_common_ranks[1][0]
    return None


def joker_values(joker: str):
    """Возвращает карты, которые может заменить джокер"""
    rank_map = "23456789TJQKA"
    if joker == "?B":
        suit_map = "SC"
    else:
        suit_map = "HD"
    return list(map(lambda card: "".join(card), itertools.product(rank_map, suit_map)))


def wild_hands(hand: Iterable[str]):
    """Возвращает все варианты "дикой" руки"""
    hands = []
    partial_hand = list(itertools.filterfalse(lambda card: "?" in card, hand))
    if "?B" in hand and "?R" in hand:
        black_joker_variants = joker_values("?B")
        red_joker_variants = joker_values("?R")
        jokers_variants = list(itertools.product(black_joker_variants, red_joker_variants))
        for joker_variant in jokers_variants:
            joker_value = [*joker_variant]
            joker_value.extend(partial_hand)
            hands.append(joker_value)
    else:
        (joker,) = filter(lambda card: "?" in card, hand)
        jokers_variants = joker_values(joker)
        for joker_variant in jokers_variants:
            joker_value = [joker_variant]
            joker_value.extend(partial_hand)
            hands.append(joker_value)
    return hands


def best_hand(hand: Iterable[str]):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт"""
    hand_combinations = itertools.combinations(hand, 5)
    hands_ranks = list(map(lambda hand: (hand, hand_rank(hand)), hand_combinations))
    return max(hands_ranks, key=lambda hand: hand[1])[0]


def best_wild_hand(hand: Iterable[str]):
    """best_hand но с джокерами"""
    hand_combinations = itertools.combinations(hand, 5)
    hands = []
    for hand_combiantion in hand_combinations:
        if "?B" in hand_combiantion or "?R" in hand_combiantion:
            hands.extend(wild_hands(hand_combiantion))
        else:
            hands.append(hand_combiantion)
    hands_ranks = list(map(lambda hand: (hand, hand_rank(hand)), hands))
    return max(hands_ranks, key=lambda hand: hand[1])[0]


def test_best_hand():
    print("test_best_hand...")
    assert sorted(best_hand("6C 7C 8C 9C TC 5C JS".split())) == ["6C", "7C", "8C", "9C", "TC"]
    assert sorted(best_hand("TD TC TH 7C 7D 8C 8S".split())) == ["8C", "8S", "TC", "TD", "TH"]
    assert sorted(best_hand("JD TC TH 7C 7D 7S 7H".split())) == ["7C", "7D", "7H", "7S", "JD"]
    print("OK")


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split())) == ["7C", "8C", "9C", "JC", "TC"]
    assert sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split())) == ["7C", "TC", "TD", "TH", "TS"]
    assert sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split())) == ["7C", "7D", "7H", "7S", "JD"]
    print("OK")


if __name__ == "__main__":
    test_best_hand()
    test_best_wild_hand()
