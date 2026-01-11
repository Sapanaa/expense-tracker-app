import re
from typing import List, Tuple


PRICE_PATTERN = re.compile(r"(\d+\.\d{2}|\d+)")


def parse_items_and_prices(text: str) -> Tuple[List[str], List[float], float]:
    """
    Parse OCR text to extract items, prices, and total.

    Args:
        text (str): Raw OCR text

    Returns:
        items (List[str])
        prices (List[float])
        total (float)
    """

    items = []
    prices = []
    total = 0.0

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Normalize common OCR mistakes
        clean_line = line.replace("|", "I").replace("O", "0")

        # Extract numbers
        numbers = PRICE_PATTERN.findall(clean_line)

        if not numbers:
            continue

        price = float(numbers[-1])

        # Detect total line
        if re.search(r"total|amount|sum", clean_line, re.IGNORECASE):
            total = price
            continue

        # Extract item name (remove price)
        item_name = re.sub(PRICE_PATTERN, "", clean_line).strip()

        # Clean item name
        item_name = re.sub(r"[^A-Za-z\s]", "", item_name)
        item_name = re.sub(r"\s+", " ", item_name)

        if len(item_name) >= 2:
            items.append(item_name)
            prices.append(price)

    # Fallback: calculate total if missing
    if total == 0.0 and prices:
        total = round(sum(prices), 2)

    return items, prices, total
