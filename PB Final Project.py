# ============================================================
# PROJECT:  MenuMix – Recipe Cost & Profitability Analyzer
# COURSE:   Programming for Business | Spring 2026
# GROUP:    [Member 1 Name] | [Member 2 Name] | [Member 3 Name] | [Member 4 Name]
#
# ── WHO DID WHAT ────────────────────────────────────────────
#  Member 1: Lead Programmer   — wrote this entire Python file
#  Member 2: Business Analyst  — designed test data & validated all outputs
#  Member 3: Report Writer     — wrote the formal project report document
#  Member 4: Presentation Lead — built the slides & prepared the demo script
# ============================================================


# ── SHARED DATA ──────────────────────────────────────────────
ingredients = {}   # { "Tomato Sauce": {"cost": 120.0, "unit": "kg"}, ... }
recipes     = {}   # { "Margherita Pizza": {"Tomato Sauce": {"qty": 0.25, "unit": "kg"}, ...}, ... }
dish_data   = {}   # { "Margherita Pizza": {ingredient_cost, cost_price, selling_price, gross_profit, margin_pct, weekly_sales, category} }

dish_options = [
    "Pizza",
    "Burger",
    "Ice Cream",
    "Alfredo Pasta",
    "Lasagna",
    "Club Sandwitches",
    "Kunafa",
    "Cake",
    "Shwarma",
    "Roll",
    "Lychee Sulshie",
    "Lemonade",
    "Mint Margarita",
    "Mocha",
    "Coffee",
    "Fries",
    "Tenders",
]


# ── HELPERS ──────────────────────────────────────────────────

def format_currency(amount):
    return f"PKR {amount:,.2f}"


def normalize_name(value):
    return value.strip().title()


def choose_dish_from_menu():
    print("\n  1st option: Which dish?")
    for index, dish_name in enumerate(dish_options, start=1):
        print(f"    {index}. {dish_name}")

    while True:
        choice = input("  Enter a dish number or name (or 'back' to return): ").strip()
        if choice.lower() == "back":
            return None
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(dish_options):
                return dish_options[index - 1]
        normalized_choice = choice.lower()
        for dish_name in dish_options:
            if dish_name.lower() == normalized_choice:
                return dish_name
        print("  Please choose a valid dish number or name from the list.")


def find_ingredient(name):
    normalized = name.strip().lower()
    for ingredient_name in ingredients:
        if ingredient_name.lower() == normalized:
            return ingredient_name
    return None


def normalize_unit(value):
    unit = value.strip().lower()
    synonyms = {
        "g": "g",
        "gram": "g",
        "grams": "g",
        "kg": "kg",
        "kilogram": "kg",
        "kilograms": "kg",
        "l": "litre",
        "litre": "litre",
        "liter": "litre",
        "litres": "litre",
        "liters": "litre",
        "ml": "ml",
        "millilitre": "ml",
        "milliliter": "ml",
        "millilitres": "ml",
        "milliliters": "ml",
    }
    return synonyms.get(unit)


def get_cost_base_unit(unit):
    if unit in {"g", "kg"}:
        return "kg"
    if unit in {"ml", "litre"}:
        return "litre"
    return None


def convert_to_base_unit(quantity, unit):
    canonical = normalize_unit(unit)
    if canonical == "g":
        return quantity / 1000.0, "kg"
    if canonical == "kg":
        return quantity, "kg"
    if canonical == "ml":
        return quantity / 1000.0, "litre"
    if canonical == "litre":
        return quantity, "litre"
    return None, None


def convert_cost_to_base_unit(cost, unit):
    canonical = normalize_unit(unit)
    if canonical == "g":
        return cost * 1000.0, "kg"
    if canonical == "kg":
        return cost, "kg"
    if canonical == "ml":
        return cost * 1000.0, "litre"
    if canonical == "litre":
        return cost, "litre"
    return None, None


def validate_unit_for_ingredient(unit, ingredient_unit):
    canonical = normalize_unit(unit)
    if ingredient_unit == "kg":
        return canonical in {"g", "kg"}
    if ingredient_unit == "litre":
        return canonical in {"ml", "litre"}
    return False


# ════════════════════════════════════════════════════════════
#  MODULE 1 — Ingredient & Recipe Input
# ════════════════════════════════════════════════════════════

def add_ingredient():
    """Ask the user for an ingredient name and cost, save to ingredients dict."""
    print("\n--- Add Ingredient ---")

    while True:
        name = input("Ingredient name (or 'back' to return): ").strip()
        if name.lower() == "back":
            return
        if not name:
            print("  Ingredient name cannot be blank.")
            continue

        normalized_name = normalize_name(name)
        existing_name = find_ingredient(normalized_name)
        if existing_name:
            info = ingredients[existing_name]
            print(f"  Ingredient '{existing_name}' already exists with cost {format_currency(info['cost'])} per {info['unit']}.")
            answer = input("  Do you want to update the cost? (y/n): ").strip().lower()
            if answer != "y":
                print("  Ingredient not updated.")
                return
            normalized_name = existing_name
        break

    while True:
        cost_text = input(f"Cost amount for '{normalized_name}' in PKR: ").strip()
        try:
            cost = float(cost_text)
            if cost < 0:
                raise ValueError()
            break
        except ValueError:
            print("  Please enter a valid positive number for the cost.")

    while True:
        unit_text = input("  Unit for this ingredient (kg / g / litre / ml): ").strip()
        cost_unit = normalize_unit(unit_text)
        if cost_unit in {"g", "kg", "ml", "litre"}:
            break
        print("  Please enter one of the following units: kg, g, litre, ml.")

    base_value, base_unit = convert_cost_to_base_unit(cost, cost_unit)
    if base_unit is None:
        print("  Failed to process the unit. Ingredient not saved.")
        return

    ingredients[normalized_name] = {
        "cost": round(base_value, 2),
        "unit": base_unit,
    }
    print(f"  Saved '{normalized_name}' at {format_currency(ingredients[normalized_name]['cost'])} per {base_unit}.")


def create_recipe():
    """Build a recipe by linking ingredients + quantities to a dish name."""
    print("\n--- Create Recipe ---")

    if not ingredients:
        print("  No ingredients are available yet. Add ingredients first.")
        return

    while True:
        dish_name = input("Dish name (or 'back' to return): ").strip()
        if dish_name.lower() == "back":
            return
        if not dish_name:
            print("  Dish name cannot be blank.")
            continue
        dish_name = normalize_name(dish_name)
        break

    if dish_name in recipes:
        answer = input(f"  Recipe for '{dish_name}' already exists. Overwrite? (y/n): ").strip().lower()
        if answer != "y":
            print("  Recipe creation cancelled.")
            return

    recipe = {}
    print("  Enter ingredient names and quantities for one dish.")
    print("  Type 'done' when you have finished adding ingredients.")

    while True:
        ingredient_input = input("    Ingredient name (or 'done'): ").strip()
        if ingredient_input.lower() == "done":
            break
        if not ingredient_input:
            print("    Ingredient name cannot be blank.")
            continue

        found_name = find_ingredient(ingredient_input)
        if not found_name:
            print("    Ingredient not found. Use one of these stored ingredients:")
            for name in sorted(ingredients):
                print(f"      - {name}")
            continue

        ingredient_unit = ingredients[found_name]["unit"]

        while True:
            qty_text = input(f"    Quantity of '{found_name}' used per dish: ").strip()
            try:
                qty = float(qty_text)
                if qty <= 0:
                    raise ValueError()
                break
            except ValueError:
                print("    Please enter a valid positive number for quantity.")

        while True:
            unit_text = input("    Unit for this quantity (kg / g / litre / ml): ").strip()
            qty_unit = normalize_unit(unit_text)
            if not qty_unit:
                print("    Please enter kg, g, litre, or ml.")
                continue
            if not validate_unit_for_ingredient(qty_unit, ingredient_unit):
                print(f"    Please enter a unit compatible with the ingredient cost unit '{ingredient_unit}'.")
                continue
            break

        base_qty, base_qty_unit = convert_to_base_unit(qty, qty_unit)
        if base_qty_unit != ingredient_unit:
            print(f"    Cannot convert '{qty_unit}' to '{ingredient_unit}'.")
            continue

        recipe[found_name] = {
            "qty": round(base_qty, 4),
            "unit": ingredient_unit,
            "display_qty": round(qty, 2),
            "display_unit": qty_unit,
        }
        print(f"    Added {recipe[found_name]['display_qty']} {recipe[found_name]['display_unit']} of '{found_name}'.")

    if not recipe:
        print("  No ingredients were added. Recipe was not saved.")
        return

    recipes[dish_name] = recipe
    print(f"  Recipe for '{dish_name}' saved with {len(recipe)} ingredient(s).")


def display_ingredients():
    """Print all stored ingredients and their costs."""
    print("\n--- Stored Ingredients ---")
    if not ingredients:
        print("  No ingredients have been added yet.")
        return

    for ingredient_name in sorted(ingredients):
        ingredient_info = ingredients[ingredient_name]
        print(f"  - {ingredient_name}: {format_currency(ingredient_info['cost'])} per {ingredient_info['unit']}")


# ════════════════════════════════════════════════════════════
#  MODULE 2 — Cost & Profit Calculations
# ════════════════════════════════════════════════════════════

def calculate_dish_cost(dish_name):
    """
    Calculate total ingredient cost for one dish from its recipe.
    Returns cost as float. If the dish has no recipe, returns 0.0.
    """
    recipe = recipes.get(dish_name)
    if recipe is None:
        return 0.0

    total_cost = 0.0
    for ingredient_name, qty_info in recipe.items():
        ingredient_info = ingredients.get(ingredient_name)
        if ingredient_info is None:
            print(f"  Error: '{ingredient_name}' is missing from stored ingredients.")
            return None
        total_cost += ingredient_info["cost"] * qty_info["qty"]

    return round(total_cost, 2)


def get_cost_price_selling_price_and_sales(dish_name):
    """Ask the user for cost price, selling price, and weekly units sold for a dish."""
    print("  2nd option: Enter the cost price")
    while True:
        cost_text = input(f"  Cost price for '{dish_name}' in PKR: ").strip()
        try:
            cost_price = float(cost_text)
            if cost_price < 0:
                raise ValueError()
            break
        except ValueError:
            print("    Please enter a valid non-negative number for the cost price.")

    print("  3rd option: Enter the selling price")
    while True:
        selling_text = input(f"  Selling price for '{dish_name}' in PKR: ").strip()
        try:
            selling_price = float(selling_text)
            if selling_price <= 0:
                raise ValueError()
            break
        except ValueError:
            print("    Please enter a valid positive number for the selling price.")

    print("  4th option: Enter the quantity")
    while True:
        sales_text = input(f"  Weekly units sold for '{dish_name}': ").strip()
        try:
            weekly_sales = int(sales_text)
            if weekly_sales < 0:
                raise ValueError()
            break
        except ValueError:
            print("    Please enter a valid whole number for weekly sales.")

    return round(cost_price, 2), round(selling_price, 2), weekly_sales


def calculate_profit(dish_name):
    """
    Calculate gross profit and margin % for a dish.
    Saves all results into dish_data dictionary.
    """
    ingredient_cost = calculate_dish_cost(dish_name)
    if ingredient_cost is None:
        ingredient_cost = 0.0

    cost_price, selling_price, weekly_sales = get_cost_price_selling_price_and_sales(dish_name)
    gross_profit = round(selling_price - cost_price, 2)
    margin_pct = round((gross_profit / selling_price) * 100, 2) if selling_price else 0.0

    dish_data[dish_name] = {
        "ingredient_cost": ingredient_cost,
        "cost_price": cost_price,
        "selling_price": selling_price,
        "gross_profit": gross_profit,
        "margin_pct": margin_pct,
        "weekly_sales": weekly_sales,
        "category": dish_data.get(dish_name, {}).get("category", "Unclassified"),
    }

    print(f"  Saved pricing for '{dish_name}': cost={format_currency(cost_price)}, price={format_currency(selling_price)}, sales={weekly_sales}")


def process_all_dishes():
    """Run calculate_profit() for a selected dish from the predefined list."""
    print("\n--- Enter Cost Price, Selling Price & Weekly Sales ---")
    dish_name = choose_dish_from_menu()
    if dish_name is None:
        print("  Returning to the main menu.")
        return

    print(f"\nDish: {dish_name}")
    calculate_profit(dish_name)

    print("\n  Pricing and sales data entry is complete.")


# ════════════════════════════════════════════════════════════
#  MODULE 3 — Menu Engineering Matrix
# ════════════════════════════════════════════════════════════

def get_averages():
    """
    Calculate average profit margin % and average weekly sales across all dishes.
    Returns (avg_margin, avg_sales).
    """
    if not dish_data:
        print("  No dish pricing and sales data is available yet.")
        return 0.0, 0.0

    total_margin = sum(data["margin_pct"] for data in dish_data.values())
    total_sales = sum(data["weekly_sales"] for data in dish_data.values())
    count = len(dish_data)
    return round(total_margin / count, 2), round(total_sales / count, 2)


def classify_dishes():
    """
    Classify every dish into one of 4 Matrix categories using dynamic averages.

    Star       = above-avg profit  +  above-avg sales   → promote these
    Plow Horse = below-avg profit  +  above-avg sales   → reprice these
    Puzzle     = above-avg profit  +  below-avg sales   → investigate these
    Dog        = below-avg profit  +  below-avg sales   → consider removing
    """
    if not dish_data:
        if not recipes:
            print("  No recipes and dish data are available. Add ingredients and recipes first.")
        else:
            print("  Please enter cost price, selling price and weekly sales first using option 3.")
        return

    avg_margin, avg_sales = get_averages()
    print(f"\n  Average margin: {avg_margin}%   |   Average weekly sales: {avg_sales}")

    for dish_name, data in dish_data.items():
        profit_above = data["margin_pct"] >= avg_margin
        sales_above = data["weekly_sales"] >= avg_sales

        if profit_above and sales_above:
            category = "Star"
        elif not profit_above and sales_above:
            category = "Plow Horse"
        elif profit_above and not sales_above:
            category = "Puzzle"
        else:
            category = "Dog"

        data["category"] = category

    print("  Dishes classified according to the Menu Engineering Matrix.")


def display_matrix():
    """Print the Menu Engineering Matrix — each dish grouped by category."""
    if not dish_data:
        print("  No dish data available to display matrix.")
        return

    matrix_groups = {
        "Star": [],
        "Plow Horse": [],
        "Puzzle": [],
        "Dog": [],
        "Unclassified": [],
    }

    for dish_name, data in dish_data.items():
        category = data.get("category", "Unclassified")
        if category not in matrix_groups:
            category = "Unclassified"
        matrix_groups[category].append(dish_name)

    print("\n" + "-" * 60)
    print("  MENU ENGINEERING MATRIX")
    print("-" * 60)
    for category in ["Star", "Plow Horse", "Puzzle", "Dog"]:
        print(f"\n{category}:")
        if matrix_groups[category]:
            for dish_name in sorted(matrix_groups[category]):
                data = dish_data[dish_name]
                print(f"  - {dish_name} (margin={data['margin_pct']}%, sales={data['weekly_sales']})")
        else:
            print("  None")


# ════════════════════════════════════════════════════════════
#  MODULE 4 — Reports, Recommendations & Main Program
# ════════════════════════════════════════════════════════════

def calculate_weekly_totals():
    """Return total weekly revenue, dish cost, and profit across all dishes."""
    total_revenue = 0.0
    total_cost = 0.0
    for data in dish_data.values():
        total_revenue += data["selling_price"] * data["weekly_sales"]
        total_cost += data["cost_price"] * data["weekly_sales"]

    total_profit = total_revenue - total_cost
    return round(total_revenue, 2), round(total_cost, 2), round(total_profit, 2)


def generate_report():
    """Print the full analysis report with all metrics per dish."""
    if not dish_data:
        print("\nNo analysis data available. Enter cost price, selling price and weekly sales first.")
        return

    print("\n" + "=" * 70)
    print("                MENUMIX REPORT")
    print("=" * 70)
    print(f"{'Dish':<25} {'Cost':>10} {'Price':>10} {'Profit':>10} {'Margin':>10} {'Sales':>8} {'Category':>14}")
    print("-" * 70)

    for dish_name, data in dish_data.items():
        cost_str = format_currency(data["cost_price"])
        price_str = format_currency(data["selling_price"])
        profit_str = format_currency(data["gross_profit"])
        margin_str = f"{data['margin_pct']}%"
        print(f"{dish_name:<25} {cost_str:>10} {price_str:>10} {profit_str:>10} {margin_str:>10} {data['weekly_sales']:>8} {data['category']:>14}")

    total_revenue, total_cost, total_profit = calculate_weekly_totals()
    print("-" * 70)
    print(f"{'TOTALS':<25} {format_currency(total_cost):>10} {format_currency(total_revenue):>10} {format_currency(total_profit):>10}")
    print("=" * 70)

    display_matrix()


def print_recommendations():
    """Print actionable business recommendations based on Matrix categories."""
    if not dish_data:
        print("\nNo recommendations available until the report has been generated.")
        return

    categories = {
        "Star": [],
        "Plow Horse": [],
        "Puzzle": [],
        "Dog": [],
    }

    for dish_name, data in dish_data.items():
        category = data.get("category", "Unclassified")
        if category in categories:
            categories[category].append(dish_name)

    print("\n--- Recommendations ---")
    print(f"PROMOTE (Stars):           {', '.join(sorted(categories['Star'])) or 'None'}")
    print(f"REPRICE (Plow Horses):     {', '.join(sorted(categories['Plow Horse'])) or 'None'}")
    print(f"INVESTIGATE (Puzzles):     {', '.join(sorted(categories['Puzzle'])) or 'None'}")
    print(f"CONSIDER REMOVING (Dogs):  {', '.join(sorted(categories['Dog'])) or 'None'}")


def show_menu():
    """Display the main menu and return the user's choice as a string."""
    print("\n" + "=" * 50)
    print("       MENUMIX — Restaurant Profit Analyzer")
    print("=" * 50)
    print("  1. Choose Dish & Enter Cost/Price")
    print("  2. Create Recipe")
    print("  3. Run Full Analysis & Show Report")
    print("  4. View Stored Ingredients")
    print("  5. Exit")
    print("=" * 50)
    return input("  Your choice: ").strip()


def main():
    """Main program loop — entry point for the full MenuMix system."""
    print("\n" + "=" * 50)
    print("  Welcome to MenuMix!")
    print("  Recipe Cost & Profitability Analyzer")
    print("  Group: [M1] | [M2] | [M3] | [M4]")
    print("=" * 50)

    while True:
        choice = show_menu()

        if choice == "1":
            process_all_dishes()
        elif choice == "2":
            create_recipe()
        elif choice == "3":
            classify_dishes()
            generate_report()
            print_recommendations()
        elif choice == "4":
            display_ingredients()
        elif choice == "5":
            print("\nThank you for using MenuMix. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter a number between 1 and 5.")


# ── ENTRY POINT ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
