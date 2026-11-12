from bakery import assert_equal
from drafter import *
from math import pi

def Orbital_Period(Mass_SM: float, Orbital_Distance_AU: float) -> float:
    Gravitational_Constant = 6.6743 * (10 ** -11)
    Sun_Mass_kg = 1.989 * (10 ** 30)

    if Mass_SM == 1:
        return round(365.25 * (Orbital_Distance_AU ** 1.5), 2)
    else:
        Mass_kg = Mass_SM * Sun_Mass_kg
        Orbital_Distance_m = Orbital_Distance_AU * (1.496 * (10 ** 11))
        Numerator = 4 * (pi ** 2)
        Denominator = Gravitational_Constant * Mass_kg
        Period = (((Numerator / Denominator) *
                   (Orbital_Distance_m ** 3)) ** 0.5) / 86400
        return round(Period, 2)


@route
def index() -> Page:
    return Page([
        "ORBITAL PERIOD CALCULATOR",
        LineBreak(),
        LineBreak(),

        "Central Object Mass (solar masses)",
        LineBreak(),
        TextBox("mass_sm", 1.0, "number"),
        LineBreak(),
        LineBreak(),

        "Orbital Distance (AU)",
        LineBreak(),
        TextBox("distance_au", 1.0, "number"),
        LineBreak(),
        LineBreak(),

        Button("Calculate Orbital Period", "calculate")
    ])


@route
def calculate(mass_sm: float, distance_au: float) -> Page:
    if mass_sm <= 0 or distance_au <= 0:
        return Page([
            "INVALID INPUT",
            LineBreak(),
            "Mass and orbital distance must both be greater than zero.",
            LineBreak(),
            Button("Try Again", "index")
        ])

    Period = Orbital_Period(mass_sm, distance_au)

    return Page([
        "ORBITAL PERIOD RESULT",
        LineBreak(),
        LineBreak(),

        "Central Object Mass",
        LineBreak(),
        str(mass_sm) + " solar masses",
        LineBreak(),
        LineBreak(),

        "Orbital Distance",
        LineBreak(),
        str(distance_au) + " AU",
        LineBreak(),
        LineBreak(),

        "Orbital Period",
        LineBreak(),
        str(Period) + " days",
        LineBreak(),
        "Approximately " + str(round(Period / 365.25, 2)) + " Earth years",
        LineBreak(),
        LineBreak(),

        Button("Calculate Another", "index")
    ])

start_server()
