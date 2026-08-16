from itertools import product


class AridhiGenerator:

    # =====================================================
    # USER-ADJUSTABLE CONSTANT
    # =====================================================

    # Maximum number of times the same complete sollu
    # can occur consecutively in an x-sollu.
    r = 3

    def __init__(self, n, level):

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
    # SIMPLE
    #
    # n = 3x + 2y
    # =====================================================

    def generate_simple(self):

        for x in range(
            0,
            self.n // 3 + 1
        ):

            remaining = self.n - 3 * x

            if remaining % 2 != 0:
                continue

            y = remaining // 2

            if (
                x > y
                and x != y
                and y != 1
            ):

                self.aridhis.append(
                    (x, y, x, y, x)
                )

    # =====================================================
    # MODERATE
    #
    # (x-l) + y + x + y + (x+l)
    #
    # n = 3x + 2y
    # =====================================================

    def generate_moderate(self):

        for x in range(
            0,
            self.n // 3 + 1
        ):

            remaining = self.n - 3 * x

            if remaining % 2 != 0:
                continue

            y = remaining // 2

            if (
                x > y
                and x != y
                and y != 1
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

                        self.aridhis.append(
                            (a, y, x, y, b)
                        )

    # =====================================================
    # HARD
    #
    # n = 3x + y + z
    #
    # y = 2z OR z = 2y
    # =====================================================

    def generate_hard(self):

        for v in range(
            self.n - 1,
            0,
            -1
        ):

            if v % 3 != 0:
                continue

            x = v // 3

            remaining = self.n - v

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

                        self.aridhis.append(
                            (a, y, x, z, b)
                        )

    # =====================================================
    # GENERATE ARIDHIS
    # =====================================================

    def generate_aridhis(self):

        if self.level == "Simple":

            self.generate_simple()

        elif self.level == "Moderate":

            self.generate_moderate()

        elif self.level == "Hard":

            self.generate_hard()

        else:

            print("\nInvalid level.")

            return

        # Remove numerical duplicates
        self.aridhis = list(
            dict.fromkeys(
                self.aridhis
            )
        )

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
    # SIMPLE SOLLU COMBINATIONS
    # =====================================================

    def generate_simple_group_aridhi(
        self,
        aridhi,
        group,
        karvai
    ):

        x = aridhi[0]
        y = aridhi[1]

        x_options = self.get_group_sollus(
            x,
            group,
            karvai
        )

        if not x_options:
            return []

        # -------------------------------------------------
        # y = 0
        # -------------------------------------------------

        if y == 0:

            result = []

            for x_sollu in x_options:

                result.append(
                    " | ".join(
                        [
                            x_sollu,
                            x_sollu,
                            x_sollu
                        ]
                    )
                )

            return sorted(
                set(result)
            )

        y_options = self.get_yz_sollus(
            y,
            karvai
        )

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

        return sorted(
            set(result)
        )

    # =====================================================
    # MODERATE / HARD SOLLU COMBINATIONS
    # =====================================================

    def generate_group_aridhi(
        self,
        aridhi,
        group,
        karvai
    ):

        x1 = aridhi[0]
        y = aridhi[1]
        x2 = aridhi[2]
        z = aridhi[3]
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
            y,
            karvai
        )

        z_options = self.get_yz_sollus(
            z,
            karvai
        )

        if not y_options or not z_options:
            return []

        result = []

        for sx1 in x1_options:

            for sy in y_options:

                if (
                    y != 0
                    and not self.valid_yz_for_x(
                        sy,
                        sx1,
                        karvai
                    )
                ):
                    continue

                for sx2 in x2_options:

                    for sz in z_options:

                        if (
                            z != 0
                            and not self.valid_yz_for_x(
                                sz,
                                sx2,
                                karvai
                            )
                        ):
                            continue

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

        return sorted(
            set(result)
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
                "(a = Adi, r = rUpakam): "
            ).strip().lower()

            if talam in [
                "a",
                "r"
            ]:

                return talam

            print(
                "Please enter a or r."
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

        if talam == "a":
            number_of_aksharas = 8
            aksharas_per_row = 2
        else:
            number_of_aksharas = 3
            aksharas_per_row = 3

        total_matras = number_of_aksharas * 4

        visual_units = visual_units[:]

        while len(visual_units) < total_matras:
            visual_units.append("_")

        # ---------------------------------------------
        # Print rows
        # ---------------------------------------------

        for row_start in range(
            0,
            number_of_aksharas,
            aksharas_per_row
        ):

            row_aksharas = min(
                aksharas_per_row,
                number_of_aksharas - row_start
            )

            row_units = visual_units[
                row_start * 4:
                (row_start + row_aksharas) * 4
            ]

            # =============================================
            # tALam row
            # =============================================

            talam_parts = []

            for i in range(row_aksharas):

                akshara = row_start + i + 1

                talam_parts.extend([
                    str(akshara),
                    "#",
                    "#",
                    "#"
                ])

            # Add vertical line AFTER every akshara
            talam_string = ""

            for i in range(row_aksharas):

                start = i * 4
                end = start + 4

                block = talam_parts[start:end]

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

            for i in range(row_aksharas):

                start = i * 4
                end = start + 4

                block = row_units[start:end]

                while len(block) < 4:
                    block.append("_")

                sollu_string += (
                    "   ".join(
                        f"{item:<4}"
                        for item in block
                    )
                )

                sollu_string += "   |   "

            print(sollu_string.rstrip())

            print()
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

        if talam == "a":

            avartana_size = 32

        else:

            avartana_size = 12

        # -------------------------------------------------
        # Smallest complete Avartana >= n
        #
        # 32 -> 32
        # 33 -> 64
        # 12 -> 12
        # 13 -> 24
        # -------------------------------------------------

        avartana = (
            (
                n + avartana_size - 1
            )
            // avartana_size
        ) * avartana_size

        blank = avartana - n

        # -------------------------------------------------
        # Convert sollu to individual mAtrAs
        # -------------------------------------------------

        sollu_units = (
            self.sollu_to_matra_units(
                selected_sollu
            )
        )

        # -------------------------------------------------
        # Blank mAtrAs occur BEFORE the korvai
        # -------------------------------------------------

        visual_units = (
            ["_"] * blank
            + sollu_units
        )

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        print(
            "\n" + "=" * 70
        )

        if talam == "a":

            print("ADI tALam")

        else:

            print("rUpakam tALam")

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
            "\nVisualization:\n"
        )

        # -------------------------------------------------
        # Print complete Avartana(s)
        # -------------------------------------------------

        remaining = visual_units[:]

        while remaining:

            if talam == "a":

                cycle_size = 32

            else:

                cycle_size = 12

            current = remaining[
                :cycle_size
            ]

            remaining = remaining[
                cycle_size:
            ]

            while len(current) < cycle_size:

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
        # GROUP 1
        # =================================================

        if self.level == "Simple":

            group1 = (
                self.generate_simple_group_aridhi(
                    selected,
                    self.group1,
                    karvai
                )
            )

        else:

            group1 = (
                self.generate_group_aridhi(
                    selected,
                    self.group1,
                    karvai
                )
            )

        # =================================================
        # GROUP 2
        # =================================================

        if self.level == "Simple":

            group2 = (
                self.generate_simple_group_aridhi(
                    selected,
                    self.group2,
                    karvai
                )
            )

        else:

            group2 = (
                self.generate_group_aridhi(
                    selected,
                    self.group2,
                    karvai
                )
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
