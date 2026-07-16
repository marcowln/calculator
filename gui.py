import tkinter as tk
from tkinter import ttk

from bmi import calculate_bmi, classify_bmi, round_bmi


WINDOW_WIDTH = 480
WINDOW_HEIGHT = 650

BACKGROUND = "#F7F8FA"
SURFACE = "#FFFFFF"
TEXT = "#172033"
MUTED_TEXT = "#667085"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
ACCENT_PRESSED = "#1E40AF"
FIELD_BORDER = "#D0D5DD"
RESULT_BACKGROUND = "#F2F4F7"
SUCCESS_BACKGROUND = "#ECFDF3"
SUCCESS_TEXT = "#067647"
ERROR_BACKGROUND = "#FEF3F2"
ERROR_TEXT = "#B42318"


def center_window(root: tk.Tk) -> None:
    """Positioniert das Fenster mittig auf dem Bildschirm."""

    root.update_idletasks()
    x = (root.winfo_screenwidth() - WINDOW_WIDTH) // 2
    y = (root.winfo_screenheight() - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def configure_styles(root: tk.Tk) -> None:
    """Definiert ein ruhiges, plattformübergreifendes ttk-Erscheinungsbild."""

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    style.configure("App.TFrame", background=BACKGROUND)
    style.configure("Card.TFrame", background=SURFACE)

    style.configure(
        "Title.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=("TkDefaultFont", 25, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=SURFACE,
        foreground=MUTED_TEXT,
        font=("TkDefaultFont", 11),
    )
    style.configure(
        "FieldLabel.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=("TkDefaultFont", 11, "bold"),
    )
    style.configure(
        "Hint.TLabel",
        background=SURFACE,
        foreground=MUTED_TEXT,
        font=("TkDefaultFont", 9),
    )

    style.configure(
        "Modern.TEntry",
        foreground=TEXT,
        fieldbackground=SURFACE,
        bordercolor=FIELD_BORDER,
        lightcolor=FIELD_BORDER,
        darkcolor=FIELD_BORDER,
        insertcolor=TEXT,
        font=("TkDefaultFont", 14),
        padding=(12, 11),
        borderwidth=1,
        relief="solid",
    )
    style.map(
        "Modern.TEntry",
        bordercolor=[("focus", ACCENT)],
        lightcolor=[("focus", ACCENT)],
        darkcolor=[("focus", ACCENT)],
    )

    style.configure(
        "Primary.TButton",
        background=ACCENT,
        foreground="#FFFFFF",
        bordercolor=ACCENT,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
        font=("TkDefaultFont", 11, "bold"),
        padding=(16, 13),
        borderwidth=0,
        relief="flat",
        anchor="center",
    )
    style.map(
        "Primary.TButton",
        background=[("pressed", ACCENT_PRESSED), ("active", ACCENT_HOVER)],
        bordercolor=[("pressed", ACCENT_PRESSED), ("active", ACCENT_HOVER)],
        lightcolor=[("pressed", ACCENT_PRESSED), ("active", ACCENT_HOVER)],
        darkcolor=[("pressed", ACCENT_PRESSED), ("active", ACCENT_HOVER)],
    )

    result_styles = {
        "Neutral": (RESULT_BACKGROUND, MUTED_TEXT),
        "Success": (SUCCESS_BACKGROUND, SUCCESS_TEXT),
        "Error": (ERROR_BACKGROUND, ERROR_TEXT),
    }
    for name, (background, color) in result_styles.items():
        style.configure(f"{name}.Result.TFrame", background=background)
        style.configure(
            f"{name}.ResultCaption.TLabel",
            background=background,
            foreground=color,
            font=("TkDefaultFont", 10, "bold"),
        )
        style.configure(
            f"{name}.ResultValue.TLabel",
            background=background,
            foreground=color,
            font=("TkDefaultFont", 29, "bold"),
        )
        style.configure(
            f"{name}.ResultDetail.TLabel",
            background=background,
            foreground=color,
            font=("TkDefaultFont", 10),
        )


def main() -> None:
    root = tk.Tk()
    root.title("BMI-Rechner")
    root.configure(background=BACKGROUND)
    root.resizable(False, False)
    configure_styles(root)
    center_window(root)

    app = ttk.Frame(root, style="App.TFrame", padding=(48, 34))
    app.grid(row=0, column=0, sticky="nsew")
    app.columnconfigure(0, weight=1)

    card = ttk.Frame(app, style="Card.TFrame", padding=(32, 28))
    card.grid(row=0, column=0, sticky="ew")
    card.columnconfigure(0, weight=1)

    ttk.Label(card, text="BMI-Rechner", style="Title.TLabel").grid(
        row=0, column=0
    )
    ttk.Label(
        card,
        text="Berechne deinen Body-Mass-Index",
        style="Subtitle.TLabel",
    ).grid(row=1, column=0, pady=(5, 28))

    ttk.Label(card, text="Gewicht", style="FieldLabel.TLabel").grid(
        row=2, column=0, sticky="w"
    )
    ttk.Label(card, text="in Kilogramm, z. B. 75", style="Hint.TLabel").grid(
        row=3, column=0, sticky="w", pady=(2, 7)
    )
    weight_entry = ttk.Entry(card, style="Modern.TEntry", font=("TkDefaultFont", 14))
    weight_entry.grid(row=4, column=0, sticky="ew")

    ttk.Label(card, text="Körpergröße", style="FieldLabel.TLabel").grid(
        row=5, column=0, sticky="w", pady=(20, 0)
    )
    ttk.Label(card, text="in Metern, z. B. 1,80", style="Hint.TLabel").grid(
        row=6, column=0, sticky="w", pady=(2, 7)
    )
    height_entry = ttk.Entry(card, style="Modern.TEntry", font=("TkDefaultFont", 14))
    height_entry.grid(row=7, column=0, sticky="ew")

    result_caption = tk.StringVar(value="Dein BMI")
    result_value = tk.StringVar(value="–")
    result_detail = tk.StringVar(value="Noch nicht berechnet")

    result_panel = ttk.Frame(
        card,
        width=320,
        height=132,
        style="Neutral.Result.TFrame",
        padding=(16, 13),
    )
    result_panel.grid(row=9, column=0, sticky="ew", pady=(24, 0))
    result_panel.grid_propagate(False)
    result_panel.columnconfigure(0, weight=1)

    caption_label = ttk.Label(
        result_panel,
        textvariable=result_caption,
        style="Neutral.ResultCaption.TLabel",
        anchor="center",
    )
    caption_label.grid(row=0, column=0, sticky="ew")
    value_label = ttk.Label(
        result_panel,
        textvariable=result_value,
        style="Neutral.ResultValue.TLabel",
        anchor="center",
    )
    value_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))
    detail_label = ttk.Label(
        result_panel,
        textvariable=result_detail,
        style="Neutral.ResultDetail.TLabel",
        anchor="center",
        justify="center",
        wraplength=280,
    )
    detail_label.grid(row=2, column=0, sticky="ew", pady=(1, 0))

    def set_result(state: str, caption: str, value: str, detail: str) -> None:
        result_panel.configure(style=f"{state}.Result.TFrame")
        caption_label.configure(style=f"{state}.ResultCaption.TLabel")
        value_label.configure(style=f"{state}.ResultValue.TLabel")
        detail_label.configure(style=f"{state}.ResultDetail.TLabel")
        result_caption.set(caption)
        result_value.set(value)
        result_detail.set(detail)

    def calculate() -> None:
        weight_text = weight_entry.get().strip()
        height_text = height_entry.get().strip()

        if not weight_text or not height_text:
            set_result(
                "Error", "Eingabe prüfen", "–", "Bitte fülle beide Felder aus."
            )
            return

        try:
            weight = float(weight_text.replace(",", "."))
            height = float(height_text.replace(",", "."))
        except ValueError:
            set_result("Error", "Eingabe prüfen", "–", "Bitte gib nur Zahlen ein.")
            return

        try:
            bmi = calculate_bmi(weight, height)
        except ValueError as error:
            set_result("Error", "Eingabe prüfen", "–", str(error))
            return

        rounded_bmi = round_bmi(bmi)
        category = classify_bmi(bmi)
        formatted_bmi = f"{rounded_bmi:.2f}".replace(".", ",")
        set_result("Success", "Dein BMI", formatted_bmi, category)

    calculate_button = ttk.Button(
        card,
        text="BMI berechnen",
        command=calculate,
        style="Primary.TButton",
        cursor="hand2",
    )
    calculate_button.grid(row=8, column=0, sticky="ew", pady=(24, 0))

    ttk.Label(
        card,
        text="Der BMI ist nur ein grober Richtwert.",
        style="Hint.TLabel",
        anchor="center",
    ).grid(row=10, column=0, sticky="ew", pady=(18, 0))

    root.bind("<Return>", lambda event: calculate())
    weight_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
