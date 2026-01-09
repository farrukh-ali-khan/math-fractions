# draw_fraction.py
# Expert Python script to draw a fraction using Turtle, handling improper fractions and showing mixed/simplified forms.
# Run: python draw_fraction.py

import turtle                                     # import turtle for drawing graphics
import math                                       # import math for gcd and trig utilities
import sys                                        # import sys to handle exits on error/interrupts

def parse_fraction(input_str):                    # parse input like "25/5" or "25 5" into two integers
    s = input_str.strip()                          # remove leading/trailing whitespace
    if '/' in s:                                   # if input uses slash separator
        parts = s.split('/')                       # split into numerator and denominator parts
        if len(parts) != 2:                        # ensure exactly two parts are present
            raise ValueError("Invalid fraction format. Use numerator/denominator.")  # raise helpful error
        num_str, den_str = parts                   # unpack numerator and denominator strings
    else:                                          # fallback: accept space-separated input like "25 5"
        parts = s.split()                          # split on whitespace
        if len(parts) != 2:                        # require exactly two tokens for fallback
            raise ValueError("Invalid input. Use 'numerator/denominator' or 'numerator denominator'.")  # error
        num_str, den_str = parts                   # unpack tokens

    try:
        num = int(num_str)                         # try converting numerator to integer
        den = int(den_str)                         # try converting denominator to integer
    except ValueError:
        raise ValueError("Numerator and denominator must be integers.")  # non-integer inputs are not allowed

    if den == 0:                                   # denominator zero is invalid mathematically
        raise ValueError("Denominator cannot be zero.")  # raise error for zero denominator

    # Normalize sign so denominator is positive and sign resides in numerator
    if den < 0:                                    # if denominator negative
        den = -den                                 # make denominator positive
        num = -num                                 # move negative sign to numerator

    return num, den                                # return possibly-improper numerator and denominator

def simplify_fraction(n, d):                      # return simplified (num, den) by gcd reduction
    g = math.gcd(n, d)                             # greatest common divisor for reduction
    return n // g, d // g                          # return reduced numerator and denominator (integers)

def to_mixed_and_signed(n, d):                     # convert possibly improper fraction to (sign, whole, rem, den)
    sign = "-" if n < 0 else ""                    # determine sign string for labeling
    an = abs(n)                                    # use absolute numerator for arithmetic
    whole = an // d                                # integer (whole) part of the improper fraction
    rem = an % d                                   # remainder for the fractional part
    return sign, whole, rem, d                     # return sign, whole part, remainder, and denominator

def draw_fraction(numerator, denominator, radius=200):  # draw the fraction on a turtle canvas
    # Create and configure the screen
    screen = turtle.Screen()                        # create a turtle graphics screen
    screen.setup(width=800, height=800)             # set window size for comfortable viewing
    screen.title(f"Fraction: {numerator}/{denominator}")  # title shows original (possibly improper) fraction
    screen.bgcolor("white")                         # white background for contrast

    t = turtle.Turtle()                             # create the turtle pen
    t.hideturtle()                                  # hide the arrow cursor for clean drawing
    t.speed(0)                                      # set drawing speed to fastest (no animation delay)
    t.pensize(1)                                    # set pen thickness for outlines

    # Prepare fraction info: mixed number and simplified forms
    sign, whole, rem, den = to_mixed_and_signed(numerator, denominator)  # compute sign, whole, remainder
    simp_num, simp_den = simplify_fraction(abs(numerator), denominator)  # simplified form of absolute fraction
    # If the whole part is non-zero, compute simplified remainder as well
    if rem != 0:
        simp_rem, simp_rem_den = simplify_fraction(rem, den)             # reduced remainder/denominator
    else:
        simp_rem, simp_rem_den = 0, 1                                    # default for zero remainder

    angle = 360.0 / den                             # angle per sector (in degrees)
    start_offset = 90                               # start at 12 o'clock (top) for first wedge

    # Draw circle outline first
    t.penup()                                       # lift pen to position without drawing
    t.goto(0, -radius)                              # move to bottom of circle to draw circle from there
    t.pendown()                                     # place pen down to draw outline
    t.pencolor("black")                             # use black outline for circle
    t.circle(radius)                                # draw the circle boundary
    t.penup()                                       # lift pen when done with outline

    # Determine drawing behavior:
    # - If remainder == 0 and whole > 0 -> entire circle is fully shaded (integer)
    # - Else shade only 'rem' sectors
    should_fill_entire = (rem == 0 and whole > 0)   # boolean flag indicating full-circle shading
    sectors_to_shade = rem if not should_fill_entire else den  # number of sectors to shade (den for full circle)

    # Draw and fill each sector (shade sectors_to_shade count)
    for i in range(den):                             # loop through each sector index
        start_angle = start_offset - i * angle      # compute starting angle for this sector
        end_angle = start_angle - angle             # compute end angle (not used explicitly here)
        should_shade = (i < sectors_to_shade)       # shade the first 'sectors_to_shade' sectors clockwise from top

        # Choose a fill color for shaded sectors; leave unshaded sectors transparent
        if should_shade:
            # If whole parts exist, use a slightly different color for clarity (blue)
            fill_color = "#1f77b4"                  # blue for shaded/filled sectors
        else:
            fill_color = ""                         # empty string -> no fill

        # Draw the wedge: center -> arc -> center
        t.penup()                                   # lift pen to move to center
        t.goto(0, 0)                                # go to circle center
        t.setheading(start_angle)                   # face the start angle direction
        t.pendown()                                 # start drawing this wedge boundary

        if should_shade:                            # if this wedge should be filled
            t.fillcolor(fill_color)                 # set the turtle fill color
            t.begin_fill()                          # start the fill region

        t.forward(radius)                           # draw radial line out to circumference at start angle
        t.left(90)                                  # orient so circle() draws arc outward
        t.circle(radius, angle)                     # draw the arc for this sector
        t.left(90)                                  # orient back toward center
        t.forward(radius)                           # draw radial line back to center to close wedge

        if should_shade:                            # if fill started for this wedge
            t.end_fill()                            # finish filling the wedge with color

        t.penup()                                   # lift pen to avoid stray marks
        t.home()                                    # reset position and heading for next wedge
        t.hideturtle()                              # keep turtle hidden

    # Draw radial divider lines for clarity (thin lines)
    t.pencolor("black")                              # black lines between sectors
    t.pensize(1)                                     # make sure lines are thin
    for i in range(den):                             # draw each radial line
        angle_deg = math.radians(start_offset - i * angle)  # convert heading to radians for trig
        x = radius * math.cos(angle_deg)             # x coordinate on circumference
        y = radius * math.sin(angle_deg)             # y coordinate on circumference
        t.penup()                                    # move without drawing
        t.goto(0, 0)                                 # go to center
        t.pendown()                                  # start drawing radial
        t.goto(x, y)                                 # draw radial line to circle edge

    # If whole part > 1, add a small text indicator showing how many whole circles are represented
    t.penup()                                        # lift pen to position for text
    t.goto(0, -radius - 30)                          # place text below the circle
    t.pencolor("black")                              # set text color
    # Build descriptive labels:
    # original fraction as entered
    original_label = f"Original: {numerator}/{denominator}"   # show original (possibly improper) fraction
    # simplified absolute fraction
    simplified_label = f"Simplified (abs): {simp_num}/{simp_den}"  # simplified form of absolute fraction
    # mixed-number label e.g. "1 3/4" or "5" if remainder==0
    if rem == 0:
        mixed_label = f"Mixed: {sign}{whole}"        # if remainder zero -> whole number only
    elif whole == 0:
        mixed_label = f"Mixed: {sign}{rem}/{den}"    # proper fractional part only (no whole)
    else:
        mixed_label = f"Mixed: {sign}{whole} {rem}/{den}"  # mixed number with whole and remainder

    # Simplify remainder display too (like 6/8 -> 3/4)
    if rem != 0:
        rem_simplified_label = f"Remainder reduced: {simp_rem}/{simp_rem_den}"
    else:
        rem_simplified_label = "Remainder reduced: 0/1"

    # Write the three informative lines centered under the circle
    t.goto(0, -radius - 30)                          # first line position
    t.write(original_label, align="center", font=("Arial", 14, "normal"))  # write original fraction
    t.goto(0, -radius - 55)                          # second line position
    t.write(simplified_label, align="center", font=("Arial", 14, "normal"))  # write simplified absolute fraction
    t.goto(0, -radius - 80)                          # third line position
    t.write(mixed_label + " — " + rem_simplified_label, align="center", font=("Arial", 14, "normal"))  # mixed and reduced remainder

    # Extra note if there are whole circle counts beyond the single drawn circle
    if whole > 1:
        t.goto(0, radius + 10)                       # position above the circle
        t.write(f"(Represents {whole} whole circle(s): drawn 1 circle + remainder)", align="center", font=("Arial", 12, "italic"))  # explanatory text

    # Wait for user click to close the window (explicit, user-friendly)
    screen.exitonclick()                             # keep window open until user clicks inside it

def main():                                        # main entrypoint for script
    try:
        user_input = input("Enter a fraction as numerator/denominator (e.g. 7/4 or 25/5): ")  # prompt for input
    except (EOFError, KeyboardInterrupt):            # handle user abort
        print("\nInput cancelled. Exiting.")         # notify and exit gracefully
        sys.exit(0)                                  # exit successfully

    try:
        num, den = parse_fraction(user_input)        # parse input to integers
    except ValueError as e:                          # catch parse/validation errors
        print(f"Error: {e}")                         # print error message
        sys.exit(1)                                 # exit with failure status

    # Draw the fraction (the drawing routine will handle improper fractions and labels)
    draw_fraction(num, den, radius=200)             # call drawing function with default radius 200 pixels

if __name__ == "__main__":                          # only run main when executed as a script
    main()                                          # start interactive prompt and drawing