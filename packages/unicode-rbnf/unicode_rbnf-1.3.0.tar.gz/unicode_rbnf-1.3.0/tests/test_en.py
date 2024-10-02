from unicode_rbnf import RbnfEngine, RulesetName


def test_english():
    engine = RbnfEngine.for_language("en")

    assert engine.format_number(7) == "seven"
    assert engine.format_number(15) == "fifteen"
    assert engine.format_number(42) == "forty-two"
    assert engine.format_number(100) == "one hundred"
    assert engine.format_number(143) == "one hundred forty-three"
    assert engine.format_number(1000) == "one thousand"
    assert engine.format_number(1234) == "one thousand two hundred thirty-four"
    assert engine.format_number(3144) == "three thousand one hundred forty-four"
    assert engine.format_number(10000) == "ten thousand"
    assert engine.format_number(83145) == "eighty-three thousand one hundred forty-five"
    assert engine.format_number(100000) == "one hundred thousand"
    assert (
        engine.format_number(683146)
        == "six hundred eighty-three thousand one hundred forty-six"
    )
    assert engine.format_number(1000000) == "one million"
    assert engine.format_number(10000000) == "ten million"
    assert engine.format_number(100000000) == "one hundred million"
    assert engine.format_number(1000000000) == "one billion"

    # Special rules
    assert engine.format_number(-1) == "minus one"
    assert engine.format_number(float("nan")) == "not a number"
    assert engine.format_number(float("inf")) == "infinite"

    # Fractions
    assert (
        engine.format_number(3.14, ruleset_name=RulesetName.CARDINAL)
        == "three point fourteen"
    )
    assert (
        engine.format_number("5.3", ruleset_name=RulesetName.CARDINAL)
        == "five point three"
    )

    # Ordinals
    assert engine.format_number(20, ruleset_name=RulesetName.ORDINAL) == "twentieth"
    assert engine.format_number(30, ruleset_name=RulesetName.ORDINAL) == "thirtieth"
    assert engine.format_number(99, ruleset_name=RulesetName.ORDINAL) == "ninety-ninth"
    assert engine.format_number(11, ruleset_name=RulesetName.ORDINAL) == "eleventh"

    # Years
    assert (
        engine.format_number(1999, ruleset_name=RulesetName.YEAR)
        == "nineteen ninety-nine"
    )
