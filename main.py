
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from math import pi

hide_debug_information()
set_website_style("water")
set_website_title("Orbital Period Calculator")
set_site_information(author="Andrew Duke"
                     description="Takes distance and mass and returns the orbital period."
                     sources="Drafter ocumentation website for coding, Dr. Bart's ChatGPT for proof reading and clarification on questions"
                     planning=["https://docs.google.com/document/d/1nQMaOD2Q09LW94_xwoZu4Bna7_5Nr-hczlVxnYFCLuA/edit?tab=t.0#heading=h.1xxqmmg350hh","https://docs.google.com/document/d/1AitzQAJGSq322cufJKIWop7OXJ5Vbv9s0oPeTdhtFtY/edit?tab=t.0#heading=h.1xxqmmg350hh"]
                     links="https://acduke1208-debug.github.io/Space-Calculator/"
)

# ORIGINAL ORBITAL PERIOD FUNCTION
def Orbital_Period(Mass_SM: float, Orbital_Distance_AU: float) -> float:
    '''
    Calculates the orbital period using central mass
    and orbital distance. Returns the period in days.
    Args:
    Mass_SM : float, mass of the central object in solar mass(1.989e30kg)
    Orbital_Distance_AU : float, distance of object from center in AU (1.496e11m)
    Returns:
    Orbital Period : float, orbital period in days
    '''
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
    
# TESTS FOR ORBITAL PERIOD
assert_equal(Orbital_Period(1, 1), 365.25)
assert_equal(Orbital_Period(1, 4), 2922.0)
assert_equal(Orbital_Period(1, 9), 9861.75)

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
    """Displays the homepage and orbital period input fields."""
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
    """Calculates and displays the orbital period."""
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

# TEST CALCULATE
test_state_c = State(1.0, 1.0, 0.0, "", [], "days")
calculate(test_state_c, "Earth", 1.0, 1.0, "days")
assert_equal(test_state_c.mass_sm, 1.0)
assert_equal(test_state_c.distance_au, 1.0)
assert_equal(test_state_c.object_name, "Earth")
assert_equal(test_state_c.orbital_period, 365.25)
assert_equal(test_state_c.period_unit, "days")

# SAVE CALCULATION
@route
def save_calculation(state: State) -> Page:
    """Saves the current calculation to calculation history."""
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


# TEST SAVE CALCULATION
test_state_sc = State(1.0, 1.0, 365.25, "Earth", [], "days")
save_calculation(test_state_sc)
assert_equal(len(test_state_sc.calculation_history), 1)
assert_equal(test_state_sc.calculation_history[0].object_name, "Earth")
assert_equal(test_state_sc.calculation_history[0].mass_sm, 1.0)
assert_equal(test_state_sc.calculation_history[0].distance_au, 1.0)
assert_equal(test_state_sc.calculation_history[0].orbital_period, 365.25)

# CALCULATION HISTORY
@route
def history(state: State) -> Page:
    """Displays all previously saved orbital calculations."""
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

#Test History
earth_test_h = OrbitalCalculation("Earth", 1.0, 1.0, 365.25)
mars_test_h = OrbitalCalculation("Mars", 1.0, 1.52, 687.19)
test_state_h = State(1.0, 1.0, 0.0, "", [earth_test_h, mars_test_h], "days")
history(test_state_h)
assert_equal(len(test_state_h.calculation_history), 2)
assert_equal(test_state_h.calculation_history[0].object_name, "Earth")
assert_equal(test_state_h.calculation_history[1].object_name, "Mars")


# DELETE CALCULATION
@route
def delete_calculation(state: State, index: int) -> Page:
    """Deletes a selected calculation from calculation history."""
    if index >= 0 and index < len(state.calculation_history):
        state.calculation_history.pop(index)

    return Page(state, [
        "CALCULATION DELETED",
        LineBreak(),
        Button("Return to History", "history"),
        LineBreak(),
        Button("Return Home", "index")
    ])

#Test Delete_Calculation
earth_test_dc = OrbitalCalculation("Earth", 1.0, 1.0, 365.25)
mars_test_dc = OrbitalCalculation("Mars", 1.0, 1.52, 687.19)
test_state_dc = State(1.0, 1.0, 0.0, "", [earth_test_dc, mars_test_dc], "days")
delete_calculation(test_state_dc, 0)
assert_equal(len(test_state_dc.calculation_history), 1)
assert_equal(test_state_dc.calculation_history[0].object_name, "Mars")

# COMPARE CALCULATIONS
@route
def compare_calculations(state: State) -> Page:
    """Compares the orbital periods of saved calculations."""
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

#Test Compare_Calculations
earth_test_cc = OrbitalCalculation("Earth", 1.0, 1.0, 365.25)
mars_test_cc = OrbitalCalculation("Mars", 1.0, 1.52, 687.19)
mercury_test_cc = OrbitalCalculation("Mercury", 1.0, 0.39, 87.97)
test_state_cc = State(
        1.0, 1.0, 0.0, "",
        [earth_test_cc, mars_test_cc, mercury_test_cc], "days"
    )
compare_calculations(test_state_cc)
assert_equal(len(test_state_cc.calculation_history), 3)
assert_equal(test_state_cc.calculation_history[0].object_name, "Earth")
assert_equal(test_state_cc.calculation_history[1].object_name, "Mars")
assert_equal(test_state_cc.calculation_history[2].object_name, "Mercury")

# VIEW CALCULATION DETAILS
@route
def view_calculation(state: State, index: int) -> Page:
    """Displays the details of an individual calculation."""
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

#Test View_Calculation
earth_test_vc = OrbitalCalculation("Earth", 1.0, 1.0, 365.25)
mars_test_vc = OrbitalCalculation("Mars", 1.0, 1.52, 687.19)
test_state_vc = State(1.0, 1.0, 0.0, "", [earth_test_vc, mars_test_vc], "days")
view_calculation(test_state_vc, 0)
assert_equal(test_state_vc.calculation_history[0].object_name, "Earth")
assert_equal(test_state_vc.calculation_history[0].orbital_period, 365.25)


# ABOUT PAGE
@route
def about(state: State) -> Page:
    """Explains orbital periods and the equations used."""
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


