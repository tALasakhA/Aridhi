from itertools import product
import re


class AridhiGenerator:

    # =====================================================
    # USER-ADJUSTABLE CONSTANT
    # =====================================================

    # Maximum number of times the same complete sollu
    # can occur consecutively in an x-sollu.
    r = 3

    def __init__(self, n, level):

        # -------------------------------------------------
        # User input limits
        # -------------------------------------------------

        if not isinstance(n, int):
            raise TypeError("mAtrA count must be an integer.")

        if n < 1 or n > 128:
            raise ValueError(
                "mAtrA count must be between 1 and 128."
            )

        if level not in [
            "Simple",
            "Moderate",
            "Hard"
        ]:
            raise ValueError(
                "Level must be Simple, Moderate, or Hard."
            )

        self.n = n
        self.level = level

        # =================================================
        # GROUP 1
        # =================================================

        self.group1 = {

            2: [
                "ta.ka"
            ],

            3: [
                "ta.ki.Ta"
            ],

            4: [
                "ta.ka.di.mi"
            ],

            5: [
                "ta.ka.ta.ki.Ta"
            ],

            6: [
                "ta.ka.ta.ka.di.mi",
                "ta.ki.Ta.ta.ki.Ta",
                "ki.Ta.ki.Ta.tom._"
            ],

            7: [
                "ta.ka.di.mi.ta.ki.Ta",
                "ta.ki.Ta.ta.ka.di.mi"
            ],

            8: [
                "ta.ka.di.mi.ta.ka.di.mi",
                "ta.ki.Ta.ta.ka.ta.ki.Ta",
                "ta.ka.ta.ki.Ta.ta.ki.Ta",
                "ta.ki.Ta.ta.ki.Ta.ta.ka",
                "ta.ka.ta.ri.ki.Ta.ta.ka"
            ],

            9: [
                "ta.ka.ta.ki.Ta.ta.ka.di.mi",
                "ta.ka.di.mi.ta.ka.ta.ki.Ta"
            ]
        }

        # =================================================
        # GROUP 2
        # =================================================

        self.group2 = {

            2: [
                "ta.ka"
            ],

            3: [
                "ta.ki.Ta"
            ],

            4: [
                "ki.Ta.ta.ka"
            ],

            5: [
                "ta.di.ki.Ta.tom"
            ],

            6: [
                "ta.di._.ki.Ta.tom"
            ],

            7: [
                "ta._.di._.ki.Ta.tom"
            ],

            8: [
                "ta.di._.ta.di.ki.Ta.tom",
                "ta.ki.Ta.ta.di.ki.Ta.tom"
            ],

            9: [
                "ta._.di._.ta.di.ki.Ta.tom",
                "ta.ki.Ta.ta.di._.ki.Ta.tom"
            ]
        }

        # =================================================
        # Y / Z SOLLUS
        # =================================================

        self.yz_sollus = {

            2: [
                "ta.ka",
                "dhim._"
            ],

            3: [
                "ta.ki.Ta",
                "dhim._._"
            ],

            4: [
                "ki.Ta.ta.ka",
                "ta.ka.di.mi",
                "dhim._._._"
            ],

            5: [
                "ta.ka.ta.ki.Ta",
                "dhim._.dhim._._"
            ]
        }

        self.aridhis = []

        self.generate_aridhis()

    # =====================================================
    # SOLLU UNITS
    # =====================================================

    def get_sollu_units(self, sollu):

        return sollu.split()

    # =====================================================
    # REPETITION CHECK
    # =====================================================

    def valid_repetition(self, sollu):

        units = self.get_sollu_units(sollu)

        if not units:
            return True

        count = 1
        previous = units[0]

        for unit in units[1:]:

            if unit == previous:

                count += 1

                if count > self.r:
                    return False

            else:

                previous = unit
                count = 1

        return True

    # =====================================================
    # START / END CHECK
    # =====================================================

    def valid_start_end(self, sollu, karvai):

        if karvai:
            return True

        units = self.get_sollu_units(sollu)

        if len(units) <= 1:
            return True

        return units[0] != units[-1]

    # =====================================================
    # REPLACE CONSECUTIVE TAKA
    # =====================================================

    def replace_consecutive_taka(self, sollu, group):

        if group is self.group1:

            replacement = "ta.ka.di.mi"

        elif group is self.group2:

            replacement = "ki.Ta.ta.ka"

        else:

            return sollu

        units = self.get_sollu_units(sollu)

        result = []

        i = 0

        while i < len(units):

            if (
                i + 1 < len(units)
                and units[i] == "ta.ka"
                and units[i + 1] == "ta.ka"
            ):

                result.append(replacement)

                i += 2

            else:

                result.append(units[i])

                i += 1

        return " ".join(result)

    # =====================================================
    # MINI ARIDHI GENERATION
    #
    # The selected level now applies to x.
    # =====================================================

    def generate_mini_aridhis(
        self,
        total,
        level
    ):

        result = []

        # -------------------------------------------------
        # SIMPLE MINI ARIDHI
        # total = 3x + 2y
        # -------------------------------------------------

        if level == "Simple":

            for x in range(
                0,
                total // 3 + 1
            ):

                remaining = total - 3 * x

                if remaining % 2 != 0:
                    continue

                y = remaining // 2

                if (
                    x > y
                    and x != y
                    and y != 1
                    and y > 0
                ):

                    result.append(
                        (x, y, x, y, x)
                    )

        # -------------------------------------------------
        # MODERATE MINI ARIDHI
        #
        # (x-l) + y + x + y + (x+l)
        # total = 3x + 2y
        # -------------------------------------------------

        elif level == "Moderate":

            for x in range(
                0,
                total // 3 + 1
            ):

                remaining = total - 3 * x

                if remaining % 2 != 0:
                    continue

                y = remaining // 2

                if (
                    x > y
                    and x != y
                    and y != 1
                    and y > 0
                ):

                    for l in range(
                        -(x // 2),
                        x // 2 + 1
                    ):

                        a = x - l
                        b = x + l

                        if (
                            l != 0
                            and a > y
                            and b > y
                            and a != y
                            and b != y
                        ):

                            result.append(
                                (a, y, x, y, b)
                            )

        # -------------------------------------------------
        # HARD MINI ARIDHI
        #
        # total = 3x + y + z
        # y = 2z OR z = 2y
        # -------------------------------------------------

        elif level == "Hard":

            for v in range(
                total - 1,
                0,
                -1
            ):

                if v % 3 != 0:
                    continue

                x = v // 3
                remaining = total - v

                for y in range(
                    1,
                    remaining
                ):

                    z = remaining - y

                    if not (
                        x != 0
                        and x > y
                        and x > z
                        and y != 0
                        and z != 0
                        and y != z
                        and (
                            y == 2 * z
                            or z == 2 * y
                        )
                        and y != 1
                        and z != 1
                    ):
                        continue

                    for l in range(
                        -x,
                        x + 1
                    ):

                        a = x - l
                        b = x + l

                        if (
                            a > y
                            and a > z
                            and b > y
                            and b > z
                        ):

                            result.append(
                                (a, y, x, z, b)
                            )

        return list(
            dict.fromkeys(result)
        )

    # =====================================================
    # CHECK MINI-ARIDHI
    #
    # The internal y (or y/z for Hard) is the y_mini.
    # y_mini can only be 2, 3, or 4.
    # =====================================================

    def valid_mini_aridhi(
        self,
        mini_aridhi
    ):

        if self.level in [
            "Simple",
            "Moderate"
        ]:

            y_mini = mini_aridhi[1]

            return y_mini in [
                2,
                3,
                4
            ]

        if self.level == "Hard":

            y_mini = mini_aridhi[1]
            z_mini = mini_aridhi[3]

            return (
                y_mini in [2, 3, 4]
                and z_mini in [2, 3, 4]
            )

        return False

    # =====================================================
    # OUTER Y VALIDATION
    #
    # The outer y must always be greater than y_mini.
    # For Hard, it must be greater than both mini y/z.
    # =====================================================

    def valid_outer_y(
        self,
        y,
        mini_aridhi
    ):

        if self.level in [
            "Simple",
            "Moderate"
        ]:

            return y > mini_aridhi[1]

        return (
            y > mini_aridhi[1]
            and y > mini_aridhi[3]
        )

    # =====================================================
    # OUTER ARIDHI GENERATION
    #
    # The outer aridhi is always:
    #
    #       x + y + x + y + x
    #
    # but x itself must be a mini aridhi of the
    # level selected by the user.
    #
    # For n > 60:
    #       y <= 15
    # =====================================================

    def generate_aridhis(self):

        self.aridhis = []

        # -------------------------------------------------
        # Only Simple outer structure is used now.
        # The selected level controls x.
        # -------------------------------------------------

        for x in range(
            1,
            self.n // 3 + 1
        ):

            remaining = self.n - 3 * x

            if remaining < 0 or remaining % 2 != 0:
                continue

            y = remaining // 2

            if (
                x <= y
                or x == y
                or y <= 0
                or y == 1
            ):
                continue

            # For large aridhis, restrict y.
            if self.n > 60 and y > 15:
                continue

            # x must itself be a valid mini aridhi.
            mini_aridhis = self.generate_mini_aridhis(
                x,
                self.level
            )

            if not mini_aridhis:
                continue

            # Every mini-aridhi of x must use only
            # y_mini values 2, 3, or 4, and the outer
            # y must be larger than y_mini.
            valid_mini = False

            for mini_aridhi in mini_aridhis:

                if self.valid_mini_aridhi(
                    mini_aridhi
                ) and self.valid_outer_y(
                    y,
                    mini_aridhi
                ):

                    valid_mini = True
                    break

            if not valid_mini:
                continue

            self.aridhis.append(
                (x, y, x, y, x)
            )

        self.aridhis = list(
            dict.fromkeys(
                self.aridhis
            )
        )

    # =====================================================
    # BACKWARD-COMPATIBLE GENERATORS
    # =====================================================

    def generate_simple(self):
        self.level = "Simple"
        self.generate_aridhis()

    def generate_moderate(self):
        self.level = "Moderate"
        self.generate_aridhis()

    def generate_hard(self):
        self.level = "Hard"
        self.generate_aridhis()

    # =====================================================
    # COUNT COMBINATIONS
    # =====================================================

    def get_count_combinations(
        self,
        number,
        minimum=2,
        maximum=9
    ):

        combinations = []

        def recurse(
            remaining,
            start,
            current
        ):

            if remaining == 0:

                combinations.append(
                    tuple(current)
                )

                return

            for value in range(
                start,
                min(
                    maximum,
                    remaining
                ) + 1
            ):

                recurse(
                    remaining - value,
                    value,
                    current + [value]
                )

        recurse(
            number,
            minimum,
            []
        )

        return combinations

    # =====================================================
    # GET X SOLLUS
    # =====================================================

    def get_group_sollus(
        self,
        value,
        group,
        karvai
    ):

        if value < 2:
            return []

        # -------------------------------------------------
        # Directly defined sollus
        # -------------------------------------------------

        if (
            value in group
            and group[value]
        ):

            valid = []

            for sollu in group[value]:

                sollu = self.replace_consecutive_taka(
                    sollu,
                    group
                )

                if not self.valid_repetition(
                    sollu
                ):
                    continue

                if not self.valid_start_end(
                    sollu,
                    karvai
                ):
                    continue

                valid.append(sollu)

            return sorted(
                set(valid)
            )

        # -------------------------------------------------
        # Higher values
        # -------------------------------------------------

        all_sollus = set()

        for counts in self.get_count_combinations(
            value
        ):

            choices = []

            valid = True

            for count in counts:

                if count not in group:

                    valid = False
                    break

                options = []

                for sollu in group[count]:

                    if self.valid_repetition(
                        sollu
                    ):

                        options.append(
                            sollu
                        )

                if not options:

                    valid = False
                    break

                choices.append(
                    options
                )

            if not valid:
                continue

            for combination in product(
                *choices
            ):

                sollu = " ".join(
                    combination
                )

                sollu = self.replace_consecutive_taka(
                    sollu,
                    group
                )

                if not self.valid_repetition(
                    sollu
                ):
                    continue

                if not self.valid_start_end(
                    sollu,
                    karvai
                ):
                    continue

                all_sollus.add(
                    sollu
                )

        return sorted(
            all_sollus
        )

    # =====================================================
    # Y / Z SOLLUS
    # =====================================================

    def get_yz_sollus(
        self,
        value,
        karvai
    ):

        if value == 0:
            return [""]

        if value not in self.yz_sollus:
            return []

        result = []

        for sollu in self.yz_sollus[value]:

            if karvai:

                units = self.get_sollu_units(
                    sollu
                )

                if not units:
                    continue

                # kArvai requires dhim as the
                # final component.

                if not units[-1].startswith(
                    "dhim"
                ):
                    continue

            else:

                # No dhim when kArvai is off.

                if any(
                    unit.startswith("dhim")
                    for unit in self.get_sollu_units(
                        sollu
                    )
                ):
                    continue

            result.append(
                sollu
            )

        return result

    # =====================================================
    # CHECK Y/Z AGAINST X
    # =====================================================

    def valid_yz_for_x(
        self,
        yz_sollu,
        x_sollu,
        karvai
    ):

        if karvai:
            return True

        x_units = self.get_sollu_units(
            x_sollu
        )

        yz_units = self.get_sollu_units(
            yz_sollu
        )

        if not x_units:
            return True

        first = x_units[0]
        last = x_units[-1]

        for unit in yz_units:

            if (
                unit == first
                or unit == last
            ):

                return False

        return True

    # =====================================================
    # NORMALIZE SOLLU FOR DUPLICATE COMPARISON
    # =====================================================

    def normalize_sollu(
        self,
        sollu
    ):

        # Ignore dots, spaces, and aridhi separators.
        # Keep "_" because it represents kArvai.
        return re.sub(
            r"[.\s|]",
            "",
            sollu
        )

    def deduplicate_sollus(
        self,
        sollus
    ):

        unique = {}

        for sollu in sollus:

            key = self.normalize_sollu(
                sollu
            )

            if key not in unique:
                unique[key] = sollu

        return sorted(
            unique.values()
        )

    # =====================================================
    # MINI-ARIDHI SOLLUS
    # =====================================================

    def generate_simple_group_aridhi(
        self,
        aridhi,
        group,
        karvai
    ):

        x = aridhi[0]
        y_mini = aridhi[1]

        x_options = self.get_group_sollus(
            x,
            group,
            karvai
        )

        if not x_options:
            return []

        y_options = self.get_yz_sollus(
            y_mini,
            karvai
        )

        if not y_options:
            return []

        result = []

        for x_sollu in x_options:

            valid_y = []

            for y_sollu in y_options:

                if self.valid_yz_for_x(
                    y_sollu,
                    x_sollu,
                    karvai
                ):
                    valid_y.append(
                        y_sollu
                    )

            for y1 in valid_y:

                for y2 in valid_y:

                    result.append(
                        " | ".join(
                            [
                                x_sollu,
                                y1,
                                x_sollu,
                                y2,
                                x_sollu
                            ]
                        )
                    )

        return self.deduplicate_sollus(
            result
        )

    # =====================================================
    # MODERATE / HARD MINI-ARIDHI SOLLUS
    # =====================================================

    def generate_group_aridhi(
        self,
        aridhi,
        group,
        karvai
    ):

        x1 = aridhi[0]
        y_mini = aridhi[1]
        x2 = aridhi[2]
        z_mini = aridhi[3]
        x3 = aridhi[4]

        x1_options = self.get_group_sollus(
            x1,
            group,
            karvai
        )

        x2_options = self.get_group_sollus(
            x2,
            group,
            karvai
        )

        x3_options = self.get_group_sollus(
            x3,
            group,
            karvai
        )

        if not (
            x1_options
            and x2_options
            and x3_options
        ):
            return []

        y_options = self.get_yz_sollus(
            y_mini,
            karvai
        )

        z_options = self.get_yz_sollus(
            z_mini,
            karvai
        )

        if not y_options or not z_options:
            return []

        result = []

        for sx1 in x1_options:

            valid_y = []

            for sy in y_options:

                if self.valid_yz_for_x(
                    sy,
                    sx1,
                    karvai
                ):
                    valid_y.append(sy)

            for sy in valid_y:

                for sx2 in x2_options:

                    valid_z = []

                    for sz in z_options:

                        if self.valid_yz_for_x(
                            sz,
                            sx2,
                            karvai
                        ):
                            valid_z.append(sz)

                    for sz in valid_z:

                        for sx3 in x3_options:

                            result.append(
                                " | ".join(
                                    [
                                        sx1,
                                        sy,
                                        sx2,
                                        sz,
                                        sx3
                                    ]
                                )
                            )

        return self.deduplicate_sollus(
            result
        )

    def generate_mini_group_aridhi(
        self,
        mini_aridhi,
        group,
        karvai
    ):

        if self.level == "Simple":

            return self.generate_simple_group_aridhi(
                mini_aridhi,
                group,
                karvai
            )

        return self.generate_group_aridhi(
            mini_aridhi,
            group,
            karvai
        )

    # =====================================================
    # BUILD OUTER Y SOLLUS
    #
    # y <= 5:
    #       use the original Y/Z sollus.
    #
    # y > 5:
    #       use x-sollus from the opposite group.
    # =====================================================

    def get_y_piece_sollus(
        self,
        y,
        x_group,
        karvai
    ):

        if y <= 5:

            return self.get_yz_sollus(
                y,
                karvai
            )

        # -------------------------------------------------
        # y > 5 must use the opposite x-sollu group.
        # get_group_sollus() also handles values > 9 by
        # combining the smaller defined group sollus.
        # -------------------------------------------------

        opposite_group = (
            self.group2
            if x_group is self.group1
            else self.group1
        )

        return self.get_group_sollus(
            y,
            opposite_group,
            karvai
        )

    # =====================================================
    # OUTER ARIDHI SOLLU COMBINATIONS
    # =====================================================

    def generate_outer_group_aridhi(
        self,
        aridhi,
        group,
        karvai
    ):

        x = aridhi[0]
        y = aridhi[1]

        mini_aridhis = self.generate_mini_aridhis(
            x,
            self.level
        )

        result = []

        for mini_aridhi in mini_aridhis:

            if not self.valid_mini_aridhi(
                mini_aridhi
            ):
                continue

            if not self.valid_outer_y(
                y,
                mini_aridhi
            ):
                continue

            x_options = self.generate_mini_group_aridhi(
                mini_aridhi,
                group,
                karvai
            )

            if not x_options:
                continue

            y_options = self.get_y_piece_sollus(
                y,
                group,
                karvai
            )

            if not y_options:
                continue

            for x_sollu in x_options:

                valid_y = []

                for y_sollu in y_options:

                    if self.valid_yz_for_x(
                        y_sollu,
                        x_sollu,
                        karvai
                    ):

                        valid_y.append(
                            y_sollu
                        )

                for y1 in valid_y:

                    for y2 in valid_y:

                        result.append(
                            " | ".join(
                                [
                                    x_sollu,
                                    y1,
                                    x_sollu,
                                    y2,
                                    x_sollu
                                ]
                            )
                        )

        return self.deduplicate_sollus(
            result
        )

    # =====================================================
    # PRINT NUMERICAL ARIDHIS
    # =====================================================

    def print_aridhis(self):

        if not self.aridhis:

            print(
                "\nNo valid aridhis found."
            )

            return

        print(
            "\nPossible Aridhis:\n"
        )

        for i, aridhi in enumerate(
            self.aridhis,
            1
        ):

            print(
                f"{i}. "
                + " + ".join(
                    map(str, aridhi)
                )
            )

    # =====================================================
    # SELECT ARIDHI
    # =====================================================

    def select_aridhi(self):

        self.print_aridhis()

        if not self.aridhis:
            return None

        while True:

            try:

                choice = int(
                    input(
                        "\nSelect an aridhi: "
                    )
                )

                if (
                    1 <= choice
                    <= len(self.aridhis)
                ):

                    return self.aridhis[
                        choice - 1
                    ]

                print(
                    "Invalid selection."
                )

            except ValueError:

                print(
                    "Please enter an integer."
                )

    # =====================================================
    # SELECT kArvai
    # =====================================================

    def select_karvai(
        self,
        selected
    ):

        # y = 0 -> no kArvai question

        if (
            self.level in [
                "Simple",
                "Moderate"
            ]
            and selected[1] == 0
        ):

            return None

        while True:

            answer = input(
                "\nDo you want kArvai? "
                "(yes/no): "
            ).strip().lower()

            if answer in [
                "yes",
                "y"
            ]:

                return True

            if answer in [
                "no",
                "n"
            ]:

                return False

            print(
                "Please enter yes or no."
            )

    # =====================================================
    # GET ARIDHI MATRAs
    # =====================================================

    def get_aridhi_count(
        self,
        aridhi
    ):

        if self.level in [
            "Simple",
            "Moderate"
        ]:

            x = aridhi[2]
            y = aridhi[1]

            return 3 * x + 2 * y

        if self.level == "Hard":

            x = aridhi[2]
            y = aridhi[1]
            z = aridhi[3]

            return 3 * x + y + z

        return 0

    # =====================================================
    # SELECT TALAM
    # =====================================================

    def select_talam(self):

        while True:

            talam = input(
                "\nEnter tALam "
                "(a = Adi, r = rUpakam, "
                "k = khaNDa cApu, m = mizra cApu): "
            ).strip().lower()

            if talam in [
                "a",
                "r",
                "k",
                "m"
            ]:

                return talam

            print(
                "Please enter a, r, k, or m."
            )

    # =====================================================
    # CONVERT SOLLU TO MATRAs
    # =====================================================

    def sollu_to_matra_units(self, sollu):

        units = []

        # The | is only an aridhi separator,
        # NOT a mAtrA/sollu unit.
        for complete_sollu in sollu.split("|"):

            complete_sollu = complete_sollu.strip()

            if not complete_sollu:
                continue

            for part in complete_sollu.split():

                parts = part.split(".")

                for p in parts:

                    # Ignore separators if any remain
                    if p == "|":
                        continue

                    units.append(p)

        return units

    # =====================================================
    # PRINT ONE TALAM ROW
    #
    # Four aksharas per row.
    #
    # Example:
    #
    # 1    #    #    #    2    #    #    #
    # ta   ka   di   mi   ta   ki   Ta   ta
    # =====================================================

    def print_talam_row(
        self,
        start_akshara,
        sollu_units
    ):

        talam_row = []
        sollu_row = []

        for i in range(4):

            akshara = start_akshara + i

            talam_row.extend(
                [
                    str(akshara),
                    "#",
                    "#",
                    "#"
                ]
            )

            start = i * 4

            current = sollu_units[
                start:start + 4
            ]

            while len(current) < 4:

                current.append("_")

            sollu_row.extend(
                current
            )

        # -------------------------------------------------
        # No vertical splitter.
        # Four aksharas are simply printed continuously.
        # -------------------------------------------------

        print(
            "   ".join(
                f"{item:<4}"
                for item in talam_row
            )
        )

        print(
            "   ".join(
                f"{item:<4}"
                for item in sollu_row
            )
        )

        print()

    # =====================================================
    # PRINT TALAM VISUALIZATION
    #
    # Adi:
    #
    # 1 # # # 2 # # # 3 # # # 4 # # #
    # ta ...
    #
    # 5 # # # 6 # # # 7 # # # 8 # # #
    # ...
    #
    # rUpakam:
    #
    # 1 # # # 2 # # # 3 # # #
    # ...
    # =====================================================

    def print_talam_visualization(
        self,
        talam,
        visual_units
    ):

        # mAtrAs in each akshara:
        #
        # Adi:
        #       1### 2### 3### 4### ...
        #
        # rUpakam:
        #       1### 2### 3###
        #
        # khaNDa cApu:
        #       1### 2# 3###
        #
        # mizra cApu:
        #       1# 2### 3### 4###

        talam_patterns = {
            "a": [4, 4, 4, 4, 4, 4, 4, 4],
            "r": [4, 4, 4],
            "k": [4, 2, 4],
            "m": [2, 4, 4, 4]
        }

        row_sizes = {
            "a": 2,
            "r": 3,
            "k": 3,
            "m": 4
        }

        pattern = talam_patterns[talam]
        aksharas_per_row = row_sizes[talam]

        total_matras = sum(pattern)

        visual_units = visual_units[:]

        while len(visual_units) < total_matras:
            visual_units.append("_")

        matra_index = 0

        for row_start in range(
            0,
            len(pattern),
            aksharas_per_row
        ):

            row_pattern = pattern[
                row_start:row_start + aksharas_per_row
            ]

            # =============================================
            # tALam row
            # =============================================

            talam_string = ""

            for i, matra_count in enumerate(row_pattern):

                akshara = row_start + i + 1

                block = [str(akshara)] + ["#"] * (
                    matra_count - 1
                )

                talam_string += (
                    "   ".join(
                        f"{item:<4}"
                        for item in block
                    )
                )

                talam_string += "   |   "

            print(talam_string.rstrip())

            # =============================================
            # Sollu row
            # =============================================

            sollu_string = ""
            row_matra_index = matra_index

            for matra_count in row_pattern:

                block = visual_units[
                    row_matra_index:
                    row_matra_index + matra_count
                ]

                while len(block) < matra_count:
                    block.append("_")

                sollu_string += (
                    "   ".join(
                        f"{item:<4}"
                        for item in block
                    )
                )

                sollu_string += "   |   "

                row_matra_index += matra_count

            print(sollu_string.rstrip())
            print()

            matra_index = row_matra_index


    # =====================================================
    # VISUALISE SELECTED ARIDHI
    # =====================================================

    def visualise_aridhi(
        self,
        selected,
        selected_sollu
    ):

        talam = self.select_talam()

        n = self.get_aridhi_count(
            selected
        )

        # -----------------------------------------------------
        # tALam definitions
        #
        # Adi:
        #       8 × 4 = 32 mAtrAs
        #
        # rUpakam:
        #       3 × 4 = 12 mAtrAs
        #
        # khaNDa cApu:
        #       4 + 2 + 4 = 10 mAtrAs
        #
        # mizra cApu:
        #       2 + 4 + 4 + 4 = 14 mAtrAs
        # -----------------------------------------------------

        talam_patterns = {
            "a": [4, 4, 4, 4, 4, 4, 4, 4],
            "r": [4, 4, 4],
            "k": [4, 2, 4],
            "m": [2, 4, 4, 4]
        }

        talam_names = {
            "a": "ADI tALam",
            "r": "rUpakam tALam",
            "k": "khaNDa cApu",
            "m": "mizra cApu"
        }

        pattern = talam_patterns[talam]
        avartana_size = sum(pattern)

        # -----------------------------------------------------
        # Smallest complete Avartana >= n
        # -----------------------------------------------------

        avartana = (
            (
                n + avartana_size - 1
            )
            // avartana_size
        ) * avartana_size

        blank = avartana - n

        # -----------------------------------------------------
        # Convert sollu to individual mAtrAs
        # -----------------------------------------------------

        sollu_units = (
            self.sollu_to_matra_units(
                selected_sollu
            )
        )

        # -----------------------------------------------------
        # Blank mAtrAs occur BEFORE the korvai
        # -----------------------------------------------------

        visual_units = (
            ["_"] * blank
            + sollu_units
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        print(
            "\n" + "=" * 70
        )

        print(
            talam_names[talam]
        )

        print(
            "=" * 70
        )

        print(
            f"\nAridhi mAtrAs : {n}"
        )

        print(
            f"Avartana      : {avartana}"
        )

        print(
            f"Blank mAtrAs  : {blank}"
        )

        print(
            f"Avartana size : {avartana_size}"
        )

        print(
            "\nVisualization:\n"
        )

        # -----------------------------------------------------
        # Print complete Avartana(s)
        # -----------------------------------------------------

        remaining = visual_units[:]

        while remaining:

            current = remaining[
                :avartana_size
            ]

            remaining = remaining[
                avartana_size:
            ]

            while len(current) < avartana_size:
                current.append("_")

            self.print_talam_visualization(
                talam,
                current
            )

    # =====================================================
    # PRINT FINAL SOLLUS
    # =====================================================

    def print_sollus(self):

        # -------------------------------------------------
        # Select numerical aridhi ONCE
        # -------------------------------------------------

        selected = self.select_aridhi()

        if selected is None:
            return

        print(
            "\nSelected Aridhi:"
        )

        print(
            " + ".join(
                map(str, selected)
            )
        )

        # -------------------------------------------------
        # kArvai
        # -------------------------------------------------

        karvai = self.select_karvai(
            selected
        )

        if karvai is True:

            print(
                "\nkArvai: YES"
            )

        elif karvai is False:

            print(
                "\nkArvai: NO"
            )

        else:

            print(
                "\nkArvai: Not applicable"
            )

        # =================================================
        # GROUP 1 / GROUP 2
        #
        # The selected level applies to x as a mini-aridhi.
        # =================================================

        group1 = self.generate_outer_group_aridhi(
            selected,
            self.group1,
            karvai
        )

        group2 = self.generate_outer_group_aridhi(
            selected,
            self.group2,
            karvai
        )

        # =================================================
        # PRINT GROUP 1
        # =================================================

        print(
            "\n" + "=" * 70
        )

        print("GROUP 1")

        print(
            "=" * 70
        )

        if group1:

            for i, sollu in enumerate(
                group1,
                1
            ):

                print(
                    f"1.{i}  {sollu}"
                )

        else:

            print(
                "No valid combinations."
            )

        # =================================================
        # PRINT GROUP 2
        # =================================================

        print(
            "\n" + "=" * 70
        )

        print("GROUP 2")

        print(
            "=" * 70
        )

        if group2:

            for i, sollu in enumerate(
                group2,
                1
            ):

                print(
                    f"2.{i}  {sollu}"
                )

        else:

            print(
                "No valid combinations."
            )

        # =================================================
        # BUILD NUMBERED SOLLU LIST
        # =================================================

        numbered_sollus = []

        for i, sollu in enumerate(
            group1,
            1
        ):

            numbered_sollus.append(
                (
                    f"1.{i}",
                    sollu
                )
            )

        for i, sollu in enumerate(
            group2,
            1
        ):

            numbered_sollus.append(
                (
                    f"2.{i}",
                    sollu
                )
            )

        if not numbered_sollus:

            print(
                "\nNo sollu combinations available."
            )

            return

        # =================================================
        # VISUALIZATION
        # =================================================

        while True:

            visualize = input(
                "\nDo you want to visualise "
                "one of these sollus in tALam? "
                "(yes/no): "
            ).strip().lower()

            if visualize in [
                "no",
                "n"
            ]:

                return

            if visualize not in [
                "yes",
                "y"
            ]:

                print(
                    "Please enter yes or no."
                )

                continue

            print(
                "\nEnter the sollu number "
                "(for example 1.1 or 2.3)."
            )

            while True:

                choice = input(
                    "Select sollu: "
                ).strip()

                selected_sollu = None

                for number, sollu in numbered_sollus:

                    if choice == number:

                        selected_sollu = sollu

                        break

                if selected_sollu is not None:

                    break

                print(
                    "Invalid selection. "
                    "Use numbers such as "
                    "1.1, 1.2, 2.1, etc."
                )

            # -------------------------------------------------
            # Visualize selected sollu
            # -------------------------------------------------

            self.visualise_aridhi(
                selected,
                selected_sollu
            )

            return
