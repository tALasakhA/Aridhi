# Aridhi

A Python tool for generating **aridhis** (numerical patterns used as musical punctuations) and their corresponding **sollu** (rhythmic syllable) realizations for Carnatic percussion (mridangam / konnakol / similar instruments), with an interactive tālam visualization.

Given a total mātrā (beat unit) count and a difficulty level, `AridhiGenerator` computes valid numerical patterns (`x`, `y`, `z` combinations), lets you pick one, fills it with sollus from two sollu "groups," and can render the final phrase against an Ādi or Rūpakam tālam grid. For now, the code employs only caturaśra gati.

---

## Table of Contents

- [Background & Terminology](#background--terminology)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
  - [1. Numerical Aridhi Generation](#1-numerical-aridhi-generation)
  - [2. Sollu Groups](#2-sollu-groups)
  - [3. Sollu Combination Generation](#3-sollu-combination-generation)
  - [4. Kārvai](#4-kārvai)
  - [5. Tālam Visualization](#5-tālam-visualization)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Example Session](#example-session)
- [License](#license)

---

## Background & Terminology

| Term | Meaning |
|---|---|
| **Aridhi** | A numerical rhythmic pattern that is used for punctuating rhythmic flow of syllables. |
| **Mātrā** | The smallest counted rhythmic unit (beat subdivision). |
| **Sollu** | A spoken/played rhythmic syllable phrase (e.g. `ta.ka.di.mi`). |
| **Kārvai** | A pause/extension (rendered with `dhim` sollus) inserted between repeated phrases. |
| **Tālam** | The rhythmic cycle used to frame the phrase — this tool supports **Ādi tālam** (8 aksharas / 32 mātrās per cycle) and **Rūpakam tālam** (3 aksharas / 12 mātrās per cycle). (More tALams coming soon)|
| **Akshara** | A beat count within a tālam cycle, subdivided into 4 mātrās each in this tool's model. |
| **Āsu** | The base *sollu / solkattu* around which the entire rhythmic pattern is built upon (e.g. 'ta.ka.di.mi', 'ta.di.ki.Ta.tom' )

**Definition of Simple, Moderate and Hard**

The *aridhi* is of the form *g + h + i + j + k*, where g, i and k are always greater than h and j for all *aridhis*. The *sollus* that come in the place of g, i and k are hereby referred to as *main sollus* and, the *sollus* that replace h and j as *connecting sollus*.

**Simple**: A main *sollu* is constructed based on the Āsu and is repeated thrice without any changes in it, connected by a different sollu(shorter than the main sollu) or a kĀrvai. The repeated connecting *sollu* or the kĀrvai are of the same mĀtra length both the times. 

Conditions: g = i = k; h = j

Aridhi form: g + h + g + h + g

**Moderate**: The main *sollus* are in an arithmetic progression and the connecting sollus (in both filled *sollus* and *kārvais*) are equal in Mātrā.

Condition: g = i - m; k = i + m; -i/2 <= m <= i/2; h = j

Aridhi form: i-m + h + i + h + i+m

**Hard**: The main *sollus* are in arithmetic progression and one connecting sollu is twice the length of the other connecting sollu ((both filled *sollus* and *kārvais*). 

Condition: g = i - m; k = i + m; -i/2 <= m <= i/2; j = nh where $n \in \lbrace 0.5, 2 \rbrace$

Aridhi form: i-m + h + i + nh + i+m

---

## Requirements

- Python 3.7+
- No third-party dependencies (uses only `itertools` from the standard library)

---

## Installation

Clone or copy the two files into the same directory:

```
project/
├── Aridhi.py     # contains the AridhiGenerator class
└── main.py       # entry point / CLI driver
```

No `pip install` is required.

---

## Usage

Run the driver script from the command line:

```bash
python main.py
```

You will be prompted for:

1. **Total mātrā** (`n`) — an integer, e.g. `128`
2. **Level** — one of `Simple`, `Moderate`, or `Hard` (case-sensitive as typed, matched exactly)

The tool then:

1. Lists all valid numerical aridhis for that `n` and level.
2. Lets you select one by number.
3. Asks whether you want **kārvai** (skipped automatically when not applicable).
4. Generates and prints all valid **Group 1** and **Group 2** sollu realizations.
5. Optionally lets you pick one sollu combination and visualize it against a tālam grid (Ādi or Rūpakam).

---

## How It Works

### 1. Numerical Aridhi Generation

Aridhis are generated as tuples of integers according to the selected `level`. Each level defines a different structural equation and constraint set.

#### Simple — `generate_simple()`

Structure: `(x, y, x, y, x)`
Equation: `n = 3x + 2y`

Constraints:
- `x > y`
- `x != y`
- `y != 1`

#### Moderate — `generate_moderate()`

Structure: `(x-l, y, x, y, x+l)`
Equation: `n = 3x + 2y` (base), varied by an offset `l`

Constraints (in addition to the Simple constraints on the base `x, y`):
- `l != 0`
- Both `a = x - l` and `b = x + l` must be `> y` and `!= y`

#### Hard — `generate_hard()`

Structure: `(a, y, x, z, b)`
Equation: `n = 3x + y + z`, with `a = x - l`, `b = x + l`

Constraints:
- `x != 0`, `x > y`, `x > z`
- `y != 0`, `z != 0`, `y != z`
- Either `y == 2z` or `z == 2y`
- `y != 1`, `z != 1`
- `a > y`, `a > z`, `b > y`, `b > z`

After generation, duplicate tuples are removed while preserving order (`dict.fromkeys`).

---

### 2. Sollu Groups

Three sollu dictionaries map a mātrā count to one or more canonical sollu phrases:

- **`group1`** — the primary sollu vocabulary (`ta.ka.di.mi` style phrases), covering counts 2–9.
- **`group2`** — a secondary vocabulary (`ta.di.ki.Ta.tom` style phrases), covering counts 2–9.
- **`yz_sollus`** — connector phrases used for the `y`/`z` positions between repeated `x` phrases, covering counts 2–5, including `dhim`-based kārvai variants.

Each sollu string is a `.`-delimited sequence of syllables, with `_` representing a silent mātrā (e.g. `"ki.Ta.ki.Ta.tom._"`).

---

### 3. Sollu Combination Generation

For a given numerical aridhi, the generator builds sollu phrases for each `x`, `y`, `z` position:

- **`get_group_sollus(value, group, karvai)`**
  If `value` is directly defined in the group dictionary, its listed sollus are used (after normalization). Otherwise, the value is decomposed into a sum of smaller counts (2–9) via `get_count_combinations`, and every valid combination of known sub-sollus is concatenated to build phrases of the required length.

- **`replace_consecutive_taka(sollu, group)`**
  Collapses two consecutive `"ta.ka"` units into a single 4-mātrā phrase (`"ta.ka.di.mi"` for Group 1, `"ki.Ta.ta.ka"` for Group 2) to avoid monotonous repetition.

- **`valid_repetition(sollu)`**
  Rejects any sollu where the same complete syllable unit repeats more than `r` times consecutively (see [Configuration](#configuration)).

- **`valid_start_end(sollu, karvai)`**
  Without kārvai, rejects sollus whose first and last syllable unit are identical (to avoid an awkward loop-back).

- **`valid_yz_for_x(yz_sollu, x_sollu, karvai)`**
  Without kārvai, ensures the connecting `y`/`z` sollu doesn't reuse the first or last syllable of the adjacent `x` sollu.

Two top-level combination builders assemble the final phrase, joining sections with `" | "`:

- **`generate_simple_group_aridhi`** — for `Simple`/`Moderate`-style `(x, y, x, y, x)` aridhis (special-cased when `y == 0`, tripling the `x` sollu).
- **`generate_group_aridhi`** — for `Hard`-style `(x1, y, x2, z, x3)` aridhis, pairing independent `y` and `z` connectors.

---

### 4. Kārvai

- If the selected aridhi's `y` value is `0` (Simple/Moderate only), the kārvai question is skipped (`select_karvai` returns `None`).
- Otherwise the user is asked yes/no.
- When kārvai is **on**, `y`/`z` connector sollus are restricted to `dhim`-ending phrases from `yz_sollus`, and the start/end and adjacency repetition checks are relaxed.
- When kārvai is **off**, `dhim` phrases are excluded, and the stricter start/end/adjacency checks apply.

---

### 5. Tālam Visualization

- **`select_talam()`** prompts for `a` (Ādi, 32 mātrās/cycle) or `r` (Rūpakam, 12 mātrās/cycle).
- **`get_aridhi_count(aridhi)`** computes the total mātrā count of the selected numerical aridhi (`3x + 2y` for Simple/Moderate, `3x + y + z` for Hard).
- **`visualise_aridhi(selected, selected_sollu)`**:
  1. Rounds the aridhi's mātrā count up to the next full avartana (cycle) of the chosen tālam.
  2. Left-pads the sollu with blank (`_`) mātrās so the phrase lands correctly at the end of the cycle.
  3. Splits the chosen sollu string into individual mātrā units via `sollu_to_matra_units` (the `|` aridhi-section separator is stripped out).
  4. Prints the result as a grid of tālam beat counters (`1 # # #  2 # # # ...`) aligned under each mātrā, row by row, cycling through as many avartanas as needed.

---

## API Reference

### `AridhiGenerator(n, level)`

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` | Total mātrā count for the aridhi. |
| `level` | `str` | One of `"Simple"`, `"Moderate"`, `"Hard"`. |

**Key attributes**

| Attribute | Description |
|---|---|
| `r` (class constant) | Max allowed consecutive repeats of an identical sollu unit. Default `3`. |
| `group1`, `group2` | Dictionaries of canonical sollus keyed by mātrā count. |
| `yz_sollus` | Dictionary of connector sollus keyed by mātrā count. |
| `aridhis` | List of generated numerical aridhi tuples (populated on init). |

**Key public methods**

| Method | Purpose |
|---|---|
| `print_aridhis()` | Print all generated numerical aridhis, numbered. |
| `select_aridhi()` | Prompt the user to pick one aridhi; returns the tuple. |
| `select_karvai(selected)` | Prompt for kārvai on/off (or `None` if not applicable). |
| `print_sollus()` | Full interactive flow: select aridhi → kārvai → generate & print Group 1/2 sollus → optional visualization. |
| `select_talam()` | Prompt for Ādi (`a`) or Rūpakam (`r`). |
| `visualise_aridhi(selected, selected_sollu)` | Render the chosen sollu against the tālam grid. |

---

## Configuration

The only user-adjustable constant is defined at the top of the class:

```python
class AridhiGenerator:
    r = 3  # max consecutive identical sollu units allowed
```

Increase or decrease `r` to loosen or tighten how repetitive a generated sollu phrase is permitted to be.

---


```

---

## License

Refer to LICENSE document.
