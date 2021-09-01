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


def string_subtract(big_str: str, sml_str: str):
    """
        Parameters
        ----------
        big_str : str
            Big string to be subtracted
        sml_string : str
            Small string that we want to know if it's at the beginning or at the end of the big_str

        Returns
        ----------
        If the sml_str is found at the beginning or at the end of the big_str, a tuple with the fragmentation is return, otherwise None.
        """
    # Check on the left
    if (big_str[:len(sml_str)] == sml_str):
        return sml_str, big_str[len(sml_str):]
    # Check on the right
    if (big_str[len(big_str)-len(sml_str):] == sml_str):
        return big_str[:len(big_str)-len(sml_str)], sml_str
    return None, None
