import re
from typing import List, Tuple, Optional, Dict


PRICE_PATTERN = re.compile(r"(\d+\.\d{2}|\d+)")


IGNORE_KEYWORDS = [
    "subtotal",
    "tax",
    "vat",
    "cgst",
    "sgst",
    "igst",
    "balance",
    "change"
]


def parse_items_and_prices(text: str) -> Dict:
    """
    Parse OCR text to extract purchasable items, prices, and totals.

    Returns:
        {
            items: List[str],
            prices: List[float],
            calculated_total: float,
            detected_total: Optional[float],
            final_total: float
        }
    """

    items: List[str] = []
    prices: List[float] = []
    detected_total: Optional[float] = None

    lines = text.splitlines()

    for line in lines:
        original_line = line.strip()
        if not original_line:
            continue

        lower_original = original_line.lower()

        # Normalize only for number extraction
        normalized_line = (
            original_line.replace("|", "I")
                          .replace("O", "0")
        )

        numbers = PRICE_PATTERN.findall(normalized_line)
        if not numbers:
            continue

        price = float(numbers[-1])

        # Detect TOTAL separately
        if "total" in lower_original or "amount" in lower_original:
            detected_total = price
            continue

        # Ignore tax-related lines
        if any(keyword in lower_original for keyword in IGNORE_KEYWORDS):
            continue

        # Extract item name
        item_name = re.sub(PRICE_PATTERN, "", original_line)
        item_name = re.sub(r"[^A-Za-z\s]", "", item_name)
        item_name = re.sub(r"\s+", " ", item_name).strip()

        if len(item_name) >= 2:
            items.append(item_name)
            prices.append(price)

    # Always calculate total from items
    calculated_total = round(sum(prices), 2)

    # Prefer detected total if available
    final_total = detected_total if detected_total is not None else calculated_total

    return {
        "items": items,
        "prices": prices,
        "calculated_total": calculated_total,
        "detected_total": detected_total,
    }
