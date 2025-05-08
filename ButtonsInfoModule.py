import operator

ButtonsInfoTable = {
    1: {"Size": (65, 65), "Position": (55, 350)},
    2: {"Size": (65, 65), "Position": (130, 350)},
    3: {"Size": (65, 65), "Position": (205, 350)},
    4: {"Size": (65, 65), "Position": (55, 275)},
    5: {"Size": (65, 65), "Position": (130, 275)},
    6: {"Size": (65, 65), "Position": (205, 275)},
    7: {"Size": (65, 65), "Position": (55, 200)},
    8: {"Size": (65, 65), "Position": (130, 200)},
    9: {"Size": (65, 65), "Position": (205, 200)},
    0: {"Size": (135, 65), "Position": (92, 425)},
    ".": {"Size": (65, 65), "Position": (205, 425)},
    "AC": {"Size": (65, 65), "Position": (280, 200)},
    "DEL": {"Size": (65, 65), "Position": (280, 275)},
    "=": {"Size": (65, 65), "Position": (355, 425)},
    "+": {"Size": (65, 135), "Position": (280, 386)},
    "-": {"Size": (65, 65), "Position": (355, 350)},
    "×": {"Size": (65, 65), "Position": (355, 275)},
    "÷": {"Size": (65, 65), "Position": (355, 200)},
    "+/-": {"Size": (65, 65), "Position": (355, 500)},
    "√": {"Size": (65, 65), "Position": (55, 500)},
    "n√": {"Size": (65, 65), "Position": (130, 500)},
    "x²": {"Size": (65, 65), "Position": (205, 500)},
    "x^y": {"Size": (65, 65), "Position": (280, 500)},
}

KeyboardValues = {
    "x": "×",
    "+": "+",
    "-": "-",
    "/": "÷"
}

OperationsTable = {
    "+": operator.add,
    "-": operator.sub,
    "×": operator.mul,
    "÷": operator.truediv,
}