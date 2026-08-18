# Aridhi Generator

A command-line Python tool that mathematically generates **aridhis** (Carnatic percussion rhythmic phrase structures) and their corresponding **sollus** (spoken mnemonic syllables, e.g. `ta.ka.di.mi`), then visualizes the chosen sollu laid out against a tALam (rhythmic cycle) grid.

---

## Table of Contents

- [Overview](#overview)
- [Domain Concepts](#domain-concepts)
- [Files](#files)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Full Walkthrough Example](#full-walkthrough-example)
- [Program Flow](#program-flow)
- [Class Reference: `AridhiGenerator`](#class-reference-aridhigenerator)
  - [Constructor & Data Setup](#constructor--data-setup)
  - [Sollu Utility Methods](#sollu-utility-methods)
  - [Mini-Aridhi Generation (Simple / Moderate / Hard)](#mini-aridhi-generation-simple--moderate--hard)
  - [Outer Aridhi Generation](#outer-aridhi-generation)
  - [Sollu Combination Building](#sollu-combination-building)
  - [User Interaction Methods](#user-interaction-methods)
  - [tALam Visualization](#talam-visualization)
  - [Top-Level Orchestration](#top-level-orchestration)
- [Validation Rules Summary](#validation-rules-summary)
- [Customization Guide](#customization-guide)
- [Known Limitations](#known-limitations)
- [License](#license)

---

## Overview

The tool works in two phases:

1. **Numeric phase** — given a total mAtrA (beat) count `n` and a difficulty `level`, it computes every valid numeric aridhi structure of the form:

   ```
   x + y + x + y + x
   ```

   where `x` itself is built from a smaller "mini-aridhi" whose shape depends on the chosen level (Simple, Moderate, or Hard).

2. **Sollu phase** — once a numeric structure is chosen, it fills in actual spoken syllable phrases (sollus) for every `x` and `y` slot, from two independent sollu vocabularies ("Group 1" and "Group 2"), applying musical validity rules (no excessive repetition, no matching start/end syllable, correct kArvai placement, etc.).

Finally, it can lay out the chosen sollu's individual mAtrAs against a tALam grid (Adi, rUpakam, khaNDa cApu, or mizra cApu), padding with blank mAtrAs so the phrase lands on a full rhythmic cycle (avartana).

---

## Domain Concepts

| Term | Meaning |
|---|---|
| **mAtrA** | A single rhythmic beat/time unit. |
| **Aridhi** | A 5-part rhythmic structure `x + y + x + y + x` (mAtrA counts). |
| **Mini-aridhi** | The internal structure that makes up `x` itself, shaped by the selected level. |
| **Sollu** | A spoken syllable phrase (e.g. `ta.ka.di.mi`) that fills a given number of mAtrAs. |
| **Group 1 / Group 2** | Two independent vocabularies of sollu phrases, each usable to fill the same numeric slots. |
| **Y/Z sollus** | A smaller vocabulary reserved for the `y` (and `z`) mAtrA counts (2–5 mAtrAs), which may include `dhim` syllables used specifically for kArvai. |
| **kArvai** | An optional rhythmic silence/pause. When enabled, sollus are allowed (and in the y/z case, required) to end in a `dhim` syllable; when disabled, `dhim` is excluded and phrases can't start/end on the same syllable as their neighbor. |
| **tALam** | A rhythmic cycle used to visually lay out mAtrAs. Four are supported: Adi (32 mAtrAs), rUpakam (12), khaNDa cApu (10), mizra cApu (14). |
| **Avartana** | One complete cycle of the chosen tALam. The visualization pads the sollu with leading blank mAtrAs (`_`) so it ends exactly on an avartana boundary. |
| **Akshara** | A named beat/count marker within a tALam cycle (e.g. beat "1", "2", …), each spanning several mAtrAs. |
| **Āsu** | The base sollu / solkattu around which the entire rhythmic pattern is built upon (e.g. 'ta.ka.di.mi', 'ta.di.ki.Ta.tom' ) |


**Definition of Simple, Moderate and Hard**

The aridhi is of the form g + h + i + j + k, where g, i and k are always greater than h and j for all aridhis. The sollus that come in the place of g, i and k are hereby referred to as main sollus and, the sollus that replace h and j as connecting sollus.

Simple: A main sollu is constructed based on the Āsu and is repeated thrice without any changes in it, connected by a different sollu(shorter than the main sollu) or a kĀrvai. The repeated connecting sollu or the kĀrvai are of the same mĀtra length both the times.

Conditions: g = i = k; h = j

Aridhi form: g + h + g + h + g

Moderate: The main sollus are in an arithmetic progression and the connecting sollus (in both filled sollus and kārvais) are equal in Mātrā.

Condition: g = i - m; k = i + m; -i/2 <= m <= i/2; h = j

Aridhi form: i-m + h + i + h + i+m

Hard: The main sollus are in arithmetic progression and one connecting sollu is twice the length of the other connecting sollu ((both filled sollus and kārvais).

Condition: g = i - m; k = i + m; -i/2 <= m <= i/2; j = nh where n ∈ {0.5,2}

Aridhi form: i-m + h + i + nh + i+m

When n > 60, only simple form of the aridhi is formed, that is of the form x + y + x + y + x. Each x is considered as a mini aridhi and and the simple, moderate and hard concept to applied to it.

---

## Files

| File | Purpose |
|---|---|
| `Generate.py` | Entry point. Collects user input (mAtrA count, level) and drives the `AridhiGenerator`. |
| `Aridhi.py` | Defines the `AridhiGenerator` class — all generation, validation, and visualization logic. |

---

## Requirements

- Python 3.7+
- No third-party dependencies — only the standard library modules `itertools` and `re` are used.

---

## How to Run

```bash
python Generate.py
```

You will be prompted for:

1. **Total mAtrA** — an integer from 1 to 128 (`n`).
2. **Level** — one of `Simple`, `Moderate`, `Hard` (case-sensitive, as typed). This controls the internal shape of `x`.

The program then:

1. Prints every valid numeric aridhi for that `n`/level and asks you to pick one by number.
2. Asks about kArvai (yes/no) — skipped automatically if `y == 0`.
3. Prints all valid Group 1 and Group 2 sollus for the chosen numeric aridhi, each numbered (e.g. `1.1`, `1.2`, `2.1`, …).
4. Asks whether you want to visualize one of them in a tALam, and if so, which one and which tALam.
5. Prints a tALam grid with the sollu's syllables placed underneath the beat numbers.

---

## Full Walkthrough Example

```
Enter the total mAtrA: 40
What level of aridhi do you want? Simple, Moderate, Hard? Simple

Possible Aridhis:

1. 6 + 8 + 6 + 8 + 6
2. 7 + 9 + 7 + 9 + 7
...

Select an aridhi: 1

Selected Aridhi:
6 + 8 + 6 + 8 + 6

Do you want kArvai? (yes/no): no

kArvai: NO

======================================================================
GROUP 1
======================================================================
1.1  ta.ka.di.mi ta.ka.di.mi | ta.ki.Ta.ta.ki.Ta.ta.ka.ta.ki.Ta | ...

======================================================================
GROUP 2
======================================================================
2.1  ki.Ta.ta.ka ta.di.ki.Ta.tom | ...

Do you want to visualise one of these sollus in tALam? (yes/no): yes

Enter the sollu number (for example 1.1 or 2.3).
Select sollu: 1.1

Enter tALam (a = Adi, r = rUpakam, k = khaNDa cApu, m = mizra cApu): a

======================================================================
ADI tALam
======================================================================

Aridhi mAtrAs : 40
Avartana      : 64
Blank mAtrAs  : 24
Avartana size : 32

Visualization:

1    #    #    #    2    #    #    #    3    #    #    #    4    #    #    #
_    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _

5    #    #    #    6    #    #    #    7    #    #    #    8    #    #    #
_    _    _    _    _    _    _    _    ta   ka   di   mi   ta   ka   di   mi
...
```

---

## Program Flow

```
Generate.py
  |- AridhiGenerator(n, level)   -> validates inputs, builds sollu dictionaries,
  |                                 calls generate_aridhis()
  |- generator.print_sollus()
       |- select_aridhi()            -> prints numeric list, gets user's pick
       |- select_karvai(selected)    -> asks yes/no (or skips if y == 0)
       |- generate_outer_group_aridhi(selected, group1, karvai)
       |- generate_outer_group_aridhi(selected, group2, karvai)
       |- prints GROUP 1 / GROUP 2 sollu lists
       |- optional visualization loop
            |- select_talam()
            |- visualise_aridhi(selected, selected_sollu)
                 |- sollu_to_matra_units(selected_sollu)
                 |- print_talam_visualization(talam, units)  (repeated per avartana)
```

---

## Class Reference: `AridhiGenerator`

### Constructor & Data Setup

#### `__init__(self, n, level)`
- Validates `n` is an `int` in `[1, 128]`, raises `TypeError`/`ValueError` otherwise.
- Validates `level` is one of `"Simple"`, `"Moderate"`, `"Hard"`.
- Stores `self.n`, `self.level`.
- Defines three sollu vocabularies as dictionaries keyed by mAtrA count:
  - `self.group1` — mAtrA counts 2–9, each mapping to a list of candidate sollu phrases.
  - `self.group2` — same range, an independent/alternate vocabulary.
  - `self.yz_sollus` — mAtrA counts 2–5, used to fill the `y`/`z` slots of an aridhi; includes `dhim` variants for kArvai.
- Initializes `self.aridhis = []` and immediately calls `self.generate_aridhis()` to populate it.

#### Class constant `r = 3`
The maximum number of times the *same* sollu unit may repeat consecutively within a phrase. Enforced by `valid_repetition()`.

---

### Sollu Utility Methods

#### `get_sollu_units(self, sollu)`
Splits a sollu string on whitespace into its component units (each unit itself being a `.`-joined syllable group, e.g. `"ta.ka.di.mi"`).

#### `valid_repetition(self, sollu)`
Walks the sollu's units and rejects the phrase if the same unit appears more than `self.r` (3) times in a row.

#### `valid_start_end(self, sollu, karvai)`
- Always returns `True` if `karvai` is enabled, or if the sollu has 1 or fewer units.
- Otherwise requires the first and last unit of the sollu to differ (prevents an awkward repeated boundary syllable).

#### `replace_consecutive_taka(self, sollu, group)`
Post-processing pass: if two consecutive `"ta.ka"` units appear in a sollu, they're merged into a single richer unit — `"ta.ka.di.mi"` for Group 1, `"ki.Ta.ta.ka"` for Group 2 — to avoid monotonous repetition. No-ops for any other group.

#### `normalize_sollu(self, sollu)`
Strips dots, whitespace, and `|` separators from a sollu string (keeping `_` for kArvai) — used as a dictionary key to detect duplicate phrases that differ only in formatting.

#### `deduplicate_sollus(self, sollus)`
Deduplicates a list of sollu strings using `normalize_sollu()` as the key, returning a sorted, unique list.

#### `sollu_to_matra_units(self, sollu)`
Converts a full generated sollu string (which may contain `|` as an aridhi-part separator and `.`-joined syllables) into a flat list of individual mAtrA-level syllable tokens, used for the tALam visualization.

---

### Mini-Aridhi Generation (Simple / Moderate / Hard)

The **mini-aridhi** is the internal structure of `x` in the outer `x + y + x + y + x` shape. Its form depends on `level`:

#### `generate_mini_aridhis(self, total, level)`
Given a target mAtrA total for `x`, returns a list of 5-tuples `(a, y, x, y_or_z, b)` representing valid internal breakdowns:

- **Simple**: solves `total = 3x + 2y` for all `x`, keeping only combinations where `x > y`, `x != y`, `y != 1`, `y > 0`. Result tuples are `(x, y, x, y, x)`.
- **Moderate**: same `3x + 2y` base, but perturbs the outer legs by an offset `l` (`(x-l, y, x, y, x+l)`), requiring `l != 0` and both perturbed legs to stay `> y` and `!= y`. This produces slightly asymmetric variants.
- **Hard**: solves `total = 3x + y + z` where `y` and `z` must satisfy `y == 2z` or `z == 2y` (with `x` strictly greater than both, `y != z`, neither equal to 1), then applies the same asymmetric perturbation `l` as Moderate, producing `(x-l, y, x, z, x+l)`.

Duplicate tuples are removed via `dict.fromkeys()` before returning.

#### `valid_mini_aridhi(self, mini_aridhi)`
Checks that the "inner" y (and for Hard, also z) of the mini-aridhi tuple is restricted to `{2, 3, 4}` — these are the only mAtrA counts with usable sollu phrases at that granularity.

#### `valid_outer_y(self, y, mini_aridhi)`
Ensures the *outer* `y` (from the top-level `x + y + x + y + x` aridhi) is strictly greater than the mini-aridhi's internal y (and z, for Hard) — this keeps the rhythmic structure properly nested/hierarchical.

#### Backward-compatible shortcuts
- `generate_simple()`, `generate_moderate()`, `generate_hard()` — set `self.level` and re-run `generate_aridhis()`. Present for convenience/compatibility; the main flow sets level once at construction instead.

---

### Outer Aridhi Generation

#### `generate_aridhis(self)`
The core numeric-structure generator, called automatically by `__init__`:

1. Iterates candidate `x` from `1` to `n // 3`.
2. Computes `y = (n - 3x) / 2`, skipping if not a non-negative integer, or if `x <= y`, `x == y`, `y <= 0`, or `y == 1`.
3. If `n > 60`, additionally restricts to `y <= 15` (keeps large aridhis' outer gaps from becoming unwieldy).
4. Requires `x` to itself decompose into at least one valid mini-aridhi (via `generate_mini_aridhis(x, self.level)`) that passes both `valid_mini_aridhi()` and `valid_outer_y(y, mini_aridhi)`.
5. Appends `(x, y, x, y, x)` to `self.aridhis` for every `x` that qualifies.
6. Deduplicates the final list.

This produces the numbered list the user picks from in `select_aridhi()`.

---

### Sollu Combination Building

Once a numeric aridhi and kArvai choice are fixed, these methods generate the actual spoken sollu phrases.

#### `get_count_combinations(self, number, minimum=2, maximum=9)`
A recursive helper that returns every ordered combination of integers in `[minimum, maximum]` summing to `number` (each combination sorted ascending internally via the recursion's `start` bound). Used to break down mAtrA counts that don't have a directly-defined sollu (i.e., values above 9) into sums of smaller, defined values.

#### `get_group_sollus(self, value, group, karvai)`
Returns all valid sollu phrases (from `group1` or `group2`) that fill exactly `value` mAtrAs:
- If `value` is directly defined in the group's dictionary (2–9), returns those phrases after applying `replace_consecutive_taka`, `valid_repetition`, and `valid_start_end`.
- Otherwise (value > 9, or not directly defined), uses `get_count_combinations()` to find all ways to split `value` into smaller defined counts, builds the Cartesian product of sollu choices for each part (via `itertools.product`), joins them with spaces, and applies the same validity filters. Deduplicated results are returned sorted.

#### `get_yz_sollus(self, value, karvai)`
Returns sollus from `self.yz_sollus` for a given `value` (2–5), filtered by kArvai state:
- If `karvai` is `True`: only phrases whose **last unit** starts with `"dhim"` are kept.
- If `karvai` is `False`: phrases containing **any** `"dhim"` unit are excluded.
- `value == 0` returns `[""]` (an empty placeholder, used when the mini-aridhi's y/z leg is zero-length).

#### `valid_yz_for_x(self, yz_sollu, x_sollu, karvai)`
When kArvai is off, prevents a y/z sollu from sharing its first or last unit with the boundary syllables of the adjacent x sollu (avoids a jarring repeated syllable at the seam). Always `True` when kArvai is on.

#### `get_y_piece_sollus(self, y, x_group, karvai)`
Builds the sollu options for the **outer** `y` slot of the top-level aridhi:
- If `y <= 5`: pulls directly from `get_yz_sollus(y, karvai)`.
- If `y > 5`: instead borrows x-style sollus from the **opposite** group (Group 2's vocabulary if building Group 1's outer aridhi, and vice versa) via `get_group_sollus()`, since the small y/z vocabulary only covers up to 5 mAtrAs.

#### `generate_simple_group_aridhi(self, aridhi, group, karvai)`
Builds sollu phrases for a **Simple**-level mini-aridhi tuple `(x, y, x, y, x)`: gets all x-sollus and y-sollus, filters y-sollus per `valid_yz_for_x`, then combines every `x_sollu + y1 + x_sollu + y2 + x_sollu` pairing (`|`-joined) and deduplicates.

#### `generate_group_aridhi(self, aridhi, group, karvai)`
The equivalent builder for **Moderate/Hard**-level mini-aridhi tuples `(x1, y, x2, z, x3)`, where the three x-legs can differ (due to the `l` perturbation) and there are two distinct inner values `y` and `z`. Builds nested combinations of `x1`, valid-`y`-for-`x1`, `x2`, valid-`z`-for-`x2`, and `x3`, joining each combination with `|` and deduplicating.

#### `generate_mini_group_aridhi(self, mini_aridhi, group, karvai)`
Dispatches to `generate_simple_group_aridhi` for `level == "Simple"`, or `generate_group_aridhi` otherwise (Moderate/Hard share the same asymmetric-tuple shape).

#### `generate_outer_group_aridhi(self, aridhi, group, karvai)`
The top-level combinator, called once per group (Group 1, Group 2) from `print_sollus()`:
1. Regenerates all mini-aridhis for the outer `x`.
2. For each mini-aridhi that's valid (`valid_mini_aridhi`) and compatible with the outer `y` (`valid_outer_y`), builds its sollu phrases via `generate_mini_group_aridhi()` — these become the outer-level "x sollu" options.
3. Builds the outer `y` sollu options via `get_y_piece_sollus()`.
4. Filters valid `y`-sollu/`x`-sollu pairings with `valid_yz_for_x()`.
5. Combines every `x_sollu + y1 + x_sollu + y2 + x_sollu` (`|`-joined) and deduplicates the final list.

This is the function whose output becomes the numbered "1.x" / "2.x" list the user sees and picks from.

---

### User Interaction Methods

#### `print_aridhis(self)`
Prints the numbered list of numeric aridhis (`self.aridhis`) as `"x + y + x + y + x"` strings, or a "No valid aridhis found." message if empty.

#### `select_aridhi(self)`
Calls `print_aridhis()`, then loops reading an integer choice from the user, validating it's in range, and returns the corresponding tuple (or `None` if there were no aridhis to choose from).

#### `select_karvai(self, selected)`
- Returns `None` immediately (no prompt) if `level` is Simple/Moderate **and** the selected aridhi's `y == 0` (kArvai is meaningless with no gap).
- Otherwise loops asking "Do you want kArvai? (yes/no)" until a valid `yes`/`no` (or `y`/`n`) answer is given, returning `True`/`False`.

#### `get_aridhi_count(self, aridhi)`
Recomputes the total mAtrA count from an aridhi tuple based on `self.level`:
- Simple/Moderate: `3x + 2y`.
- Hard: `3x + y + z`.

#### `select_talam(self)`
Loops asking the user to choose a tALam (`a`/`r`/`k`/`m`) until valid, returning the single-letter code.

---

### tALam Visualization

#### `print_talam_row(self, start_akshara, sollu_units)`
*(Legacy/unused-by-default helper for a fixed 4-akshara-per-row, 4-mAtrA-per-akshara layout — largely superseded by `print_talam_visualization`, which supports all four tALam shapes.)* Prints one row of 4 aksharas (each spanning 4 mAtrAs) with beat numbers and `#` placeholders above the corresponding sollu syllables.

#### `print_talam_visualization(self, talam, visual_units)`
The general-purpose renderer supporting all four tALams:

| Code | Name | Akshara pattern (mAtrAs per akshara) | Aksharas/row | Total mAtrAs |
|---|---|---|---|---|
| `a` | Adi tALam | `[4,4,4,4,4,4,4,4]` | 2 | 32 |
| `r` | rUpakam tALam | `[4,4,4]` | 3 | 12 |
| `k` | khaNDa cApu | `[4,2,4]` | 3 | 10 |
| `m` | mizra cApu | `[2,4,4,4]` | 4 | 14 |

For each row of aksharas it prints:
1. A tALam line — beat number followed by `#` filler for each remaining mAtrA in that akshara, aksharas separated by `|`.
2. A sollu line — the corresponding syllables (or `_` for blank/missing mAtrAs) aligned under the tALam line.

Pads `visual_units` with trailing `_` if shorter than the tALam's total mAtrA count.

#### `visualise_aridhi(self, selected, selected_sollu)`
The top-level visualization driver:
1. Prompts for tALam via `select_talam()`.
2. Computes the aridhi's mAtrA count `n` via `get_aridhi_count()`.
3. Computes `avartana` — the smallest multiple of the tALam's cycle size that's `>= n` — and `blank = avartana - n`.
4. Converts the chosen sollu string into individual mAtrA units via `sollu_to_matra_units()`.
5. Prepends `blank` copies of `"_"` **before** the sollu (blank mAtrAs occur at the start of the cycle, not the end).
6. Prints a header (tALam name, mAtrA count, avartana size, blank count).
7. Slices the padded unit list into avartana-sized chunks and calls `print_talam_visualization()` once per chunk, padding the final chunk with trailing `_` if needed.

---

### Top-Level Orchestration

#### `print_sollus(self)`
Called by `Generate.py` after construction. This is the full user-facing flow:

1. `select_aridhi()` — get the numeric structure; returns early if none available.
2. Prints the selected aridhi.
3. `select_karvai(selected)` — get the kArvai choice; prints "YES" / "NO" / "Not applicable".
4. `generate_outer_group_aridhi(selected, self.group1, karvai)` and the same for `self.group2` — build both groups' sollu lists.
5. Prints "GROUP 1" and "GROUP 2" sections, each numbered (`1.1`, `1.2`, … / `2.1`, `2.2`, …), or "No valid combinations." if empty.
6. Builds a combined `numbered_sollus` list mapping label to sollu string; returns early if totally empty.
7. Loops asking "Do you want to visualise one of these sollus in tALam?":
   - On "no" -> returns.
   - On "yes" -> loops reading a sollu label (e.g. `1.1`) until it matches an entry, then calls `visualise_aridhi(selected, selected_sollu)` and returns.

---

## Validation Rules Summary

| Rule | Enforced by | Effect |
|---|---|---|
| No same sollu unit repeated more than `r` (3) times consecutively | `valid_repetition()` | Avoids monotonous phrases. |
| A sollu's first and last unit must differ (unless kArvai) | `valid_start_end()` | Avoids awkward phrase boundaries. |
| Consecutive `"ta.ka" "ta.ka"` merged into a richer unit | `replace_consecutive_taka()` | Musical variety. |
| Mini-aridhi's internal y (and z) restricted to `{2, 3, 4}` | `valid_mini_aridhi()` | Only granularities with defined sollus are usable. |
| Outer y must exceed mini-aridhi's internal y/z | `valid_outer_y()` | Keeps nested structure proportionate. |
| y/z sollu must contain `dhim` (kArvai on) or must not (kArvai off) | `get_yz_sollus()` | Correct kArvai semantics. |
| y/z sollu can't share first/last unit with adjacent x sollu (kArvai off) | `valid_yz_for_x()` | Avoids repeated syllable at a seam. |
| `n > 60` restricts outer `y` to `<= 15` | `generate_aridhis()` | Keeps large aridhis' gaps reasonable. |

---

## Customization Guide

- **Allow more/fewer consecutive repeats**: change `AridhiGenerator.r` (class attribute, default `3`).
- **Add new sollu vocabulary**: extend `self.group1`, `self.group2`, or `self.yz_sollus` dictionaries inside `__init__` — keys are mAtrA counts, values are lists of `.`-joined syllable phrases (space-separated for multi-unit phrases).
- **Add a new tALam**: add an entry to both `talam_patterns` and `row_sizes`/`talam_names` dictionaries (present in both `print_talam_visualization()` and `visualise_aridhi()` — keep them in sync), and update the `select_talam()` prompt/validation list.
- **Change the max mAtrA input**: adjust the bounds check (`n < 1 or n > 128`) in `__init__`.

---

## Known Limitations

- Input validation for `Generate.py`'s `int(input(...))` call is not wrapped in a `try/except`, so a non-numeric mAtrA entry will raise an uncaught `ValueError` and crash the program.
- The `level` input to `Generate.py` is case-sensitive and must exactly match `"Simple"`, `"Moderate"`, or `"Hard"` (extra whitespace is stripped, but casing/typos are not corrected).
- `print_talam_row()` is a legacy fixed-layout helper not actually invoked by the current visualization path (`print_talam_visualization()` is used instead) — kept for reference/compatibility.
- Sollu vocabularies (`group1`, `group2`, `yz_sollus`) only have entries up to 9 (or 5 for yz) mAtrAs; larger values rely on combinatorial splitting via `get_count_combinations()`, which can produce a large number of candidate phrases for bigger inputs.

---

## License

Add a license of your choice (e.g. MIT) before publishing to GitHub.
