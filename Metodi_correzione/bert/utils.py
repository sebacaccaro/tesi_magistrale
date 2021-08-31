import re


def cleanOutput(output: str):
    output = output.replace(" , ", ", ")
    output = output.replace(" ' ", "'")
    output = output.replace("' ", "'")
    output = output.replace(" ’ ", "’")
    output = output.replace(" ’", "’")
    output = output.replace(" . ", ". ")
    output = output.replace(" .", ".")
    output = output.replace(" : ", ": ")
    output = output.replace(" ; ", "; ")
    output = re.sub(r'\s\s+', " ", output)
    output = output.strip()
    return output
