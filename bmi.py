def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Berechnet den Body-Mass-Index."""

    if weight_kg <= 0:
        raise ValueError("Das Gewicht muss größer als 0 sein.")

    if height_m <= 0:
        raise ValueError("Die Körpergröße muss größer als 0 sein.")

    return weight_kg / height_m**2


def round_bmi(bmi: float) -> float:
    """Rundet den BMI auf zwei Nachkommastellen."""

    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """Ordnet einen BMI grob einer Kategorie zu."""

    if bmi < 18.5:
        return "Untergewicht"
    if bmi < 25:
        return "Normalgewicht"
    if bmi < 30:
        return "Übergewicht"

    return "Adipositas"


def main() -> None:
    weight = float(input("Gewicht in Kilogramm: "))
    height = float(input("Körpergröße in Metern, z. B. 1.80: "))

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    rounded_bmi = round_bmi(bmi)

    print(f"Dein berechneter BMI beträgt: {rounded_bmi:.2f}")
    print(f"Kategorie: {category}")
    print("Hinweis: Der BMI ist nur ein grober Richtwert.")


if __name__ == "__main__":
    main()
