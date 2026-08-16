# =========================================================
# MAIN
# =========================================================
from Aridhi import AridhiGenerator

n = int(
    input(
        "Enter the total mAtrA: "
    )
)

level = input(
    "What level of aridhi do you want? "
    "Simple, Moderate, Hard? "
).strip()


generator = AridhiGenerator(
    n,
    level
)

generator.print_sollus()
