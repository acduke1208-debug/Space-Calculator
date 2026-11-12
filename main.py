
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from math import pi


# ORIGINAL ORBITAL PERIOD FUNCTION
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

# SECOND DATACLASS
@dataclass
class OrbitalCalculation:
    object_name: str
    mass_sm: float
    distance_au: float
    orbital_period: float

# STATE DATACLASS
@dataclass
class State:
    mass_sm: float
    distance_au: float
    orbital_period: float
    object_name: str
    calculation_history: list
    period_unit: str

# HOMEPAGE
@route
def index(state: State) -> Page:
    return Page(state, [
        "ORBITAL PERIOD CALCULATOR",
        LineBreak(),
        LineBreak(),

        "Object Name",
        LineBreak(),
        TextBox("object_name", "Earth", "text"),
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

        "Preferred Period Unit",
        LineBreak(),
        SelectBox("period_unit", ["days", "years"]),
        LineBreak(),
        LineBreak(),

        Button("Calculate Orbital Period", "calculate"),
        LineBreak(),
        Button("View Calculation History", "history"),
        LineBreak(),
        Button("About Orbital Periods", "about")
    ])

# CALCULATE ORBITAL PERIOD
@route
def calculate(state: State, object_name: str,
              mass_sm: float, distance_au: float,
              period_unit: str) -> Page:

    if mass_sm <= 0 or distance_au <= 0:
        return Page(state, [
            "INVALID INPUT",
            LineBreak(),
            "Mass and orbital distance must both be greater than zero.",
            LineBreak(),
            Button("Try Again", "index")
        ])

    if object_name == "":
        return Page(state, [
            "INVALID INPUT",
            LineBreak(),
            "Please enter an object name.",
            LineBreak(),
            Button("Try Again", "index")
        ])

    state.mass_sm = mass_sm
    state.distance_au = distance_au
    state.object_name = object_name
    state.period_unit = period_unit

    state.orbital_period = Orbital_Period(mass_sm, distance_au)

    Display_Period = state.orbital_period

    if period_unit == "years":
        Display_Period = round(state.orbital_period / 365.25, 2)

    return Page(state, [
        "ORBITAL PERIOD RESULT",
        LineBreak(),
        LineBreak(),

        "Object Name:",
        LineBreak(),
        object_name,
        LineBreak(),
        LineBreak(),

        "Central Object Mass:",
        LineBreak(),
        str(mass_sm) + " solar masses",
        LineBreak(),
        LineBreak(),

        "Orbital Distance:",
        LineBreak(),
        str(distance_au) + " AU",
        LineBreak(),
        LineBreak(),

        "Orbital Period:",
        LineBreak(),
        str(Display_Period) + " " + period_unit,
        LineBreak(),
        LineBreak(),

        Button("Save Calculation", "save_calculation"),
        LineBreak(),
        Button("Calculate Another", "index"),
        LineBreak(),
        Button("View History", "history")
    ])

# SAVE CALCULATION
@route
def save_calculation(state: State) -> Page:

    New_Calculation = OrbitalCalculation(
        state.object_name,
        state.mass_sm,
        state.distance_au,
        state.orbital_period
    )

    state.calculation_history.append(New_Calculation)

    return Page(state, [
        "CALCULATION SAVED!",
        LineBreak(),
        "Your calculation has been saved.",
        LineBreak(),
        LineBreak(),
        Button("View History", "history"),
        LineBreak(),
        Button("Return Home", "index")
    ])

# CALCULATION HISTORY
@route
def history(state: State) -> Page:

    Content = [
        "CALCULATION HISTORY",
        LineBreak(),
        LineBreak()
    ]

    if len(state.calculation_history) == 0:
        Content.append("You have no saved calculations.")

    else:
        # LOOP THROUGH SAVED CALCULATIONS
        for calculation in state.calculation_history:

            Content.extend([
                "Object: " + calculation.object_name,
                LineBreak(),
                "Central Mass: " + str(calculation.mass_sm) +
                " solar masses",
                LineBreak(),
                "Orbital Distance: " + str(calculation.distance_au) +
                " AU",
                LineBreak(),
                "Orbital Period: " + str(calculation.orbital_period) +
                " days",
                LineBreak(),
                LineBreak()
            ])

    Content.extend([
        Button("Compare Calculations", "compare_calculations"),
        LineBreak(),
        Button("Return Home", "index")
    ])

    return Page(state, Content)

# DELETE CALCULATION
@route
def delete_calculation(state: State, index: int) -> Page:

    if index >= 0 and index < len(state.calculation_history):
        state.calculation_history.pop(index)

    return Page(state, [
        "CALCULATION DELETED",
        LineBreak(),
        Button("Return to History", "history"),
        LineBreak(),
        Button("Return Home", "index")
    ])

# COMPARE CALCULATIONS
@route
def compare_calculations(state: State) -> Page:

    Content = [
        "COMPARE ORBITAL CALCULATIONS",
        LineBreak(),
        LineBreak()
    ]

    if len(state.calculation_history) < 2:
        Content.append(
            "You need at least two saved calculations to compare them."
        )

    else:
        Shortest = state.calculation_history[0]
        Longest = state.calculation_history[0]

        for calculation in state.calculation_history:

            Content.extend([
                "Object: " + calculation.object_name,
                LineBreak(),
                "Orbital Period: " +
                str(calculation.orbital_period) + " days",
                LineBreak(),
                LineBreak()
            ])

            if calculation.orbital_period < Shortest.orbital_period:
                Shortest = calculation

            if calculation.orbital_period > Longest.orbital_period:
                Longest = calculation

        Content.extend([
            "COMPARISON RESULTS",
            LineBreak(),
            "Shortest Period: " + Shortest.object_name,
            LineBreak(),
            "Longest Period: " + Longest.object_name,
            LineBreak(),
            LineBreak()
        ])

    Content.extend([
        Button("Return to History", "history"),
        LineBreak(),
        Button("Return Home", "index")
    ])

    return Page(state, Content)

# VIEW CALCULATION DETAILS
@route
def view_calculation(state: State, index: int) -> Page:

    if index < 0 or index >= len(state.calculation_history):
        return Page(state, [
            "Calculation not found.",
            LineBreak(),
            Button("Return to History", "history")
        ])

    calculation = state.calculation_history[index]

    return Page(state, [
        "CALCULATION DETAILS",
        LineBreak(),
        LineBreak(),
        "Object: " + calculation.object_name,
        LineBreak(),
        "Central Mass: " + str(calculation.mass_sm),
        LineBreak(),
        "Orbital Distance: " + str(calculation.distance_au),
        LineBreak(),
        "Orbital Period: " + str(calculation.orbital_period) + " days",
        LineBreak(),
        "Orbital Period in Years: " +
        str(round(calculation.orbital_period / 365.25, 2)),
        LineBreak(),
        LineBreak(),
        Button("Return to History", "history")
    ])

# ABOUT PAGE
@route
def about(state: State) -> Page:

    return Page(state, [
        "ABOUT ORBITAL PERIODS",
        LineBreak(),
        LineBreak(),

        "An orbital period is the amount of time an object takes "
        "to complete one full orbit around another object.",
        LineBreak(),
        LineBreak(),

        "This calculator uses Kepler's Third Law and Newton's "
        "law of universal gravitation.",
        LineBreak(),
        LineBreak(),

        "P = 2π√(r³ / GM)",
        LineBreak(),
        LineBreak(),

        "P = Orbital Period",
        LineBreak(),
        "r = Orbital Distance",
        LineBreak(),
        "G = Gravitational Constant",
        LineBreak(),
        "M = Central Object Mass",
        LineBreak(),
        LineBreak(),

        Button("Return Home", "index")
    ])

# START WEBSITE
start_server(State(
    mass_sm=1.0,
    distance_au=1.0,
    orbital_period=0.0,
    object_name="",
    calculation_history=[],
    period_unit="days"
))


