# ------------------------------
# Get first fraction from user
# ------------------------------
num1 = int(input("First fraction - top: "))   # Numerator of first fraction
den1 = int(input("First fraction - bottom: ")) # Denominator of first fraction

# ------------------------------
# Get second fraction from user
# ------------------------------
num2 = int(input("Second fraction - top: "))   # Numerator of second fraction
den2 = int(input("Second fraction - bottom: ")) # Denominator of second fraction

# ------------------------------
# Convert fractions to decimals for easy comparison
# ------------------------------
value1 = num1 / den1  # First fraction as decimal
value2 = num2 / den2  # Second fraction as decimal

# ------------------------------
# Compare the decimal values
# ------------------------------
if value1 > value2:
    print(f"{num1}/{den1} is larger than {num2}/{den2}")
elif value2 > value1:
    print(f"{num2}/{den2} is larger than {num1}/{den1}")
else:
    print(f"{num1}/{den1} equals {num2}/{den2}")

# ------------------------------
# Show decimal values for clarity
# ------------------------------
print(f"({value1:.3f} vs {value2:.3f})")
