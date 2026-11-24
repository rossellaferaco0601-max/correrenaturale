#!/usr/bin/env python3
"""Parole di YTCN 26 tra due tempi del sorgente (con inizio e fine): python3 scripts/g_words.py 269.5 280"""
import json, sys
ws = json.load(open("src/cn/words26.json")); a, b = float(sys.argv[1]), float(sys.argv[2])
print(" ".join(f"{x['text'].strip()}[{x['startMs'] / 1000:.2f}-{x['endMs'] / 1000:.2f}]" for x in ws if a <= x["startMs"] / 1000 <= b))
