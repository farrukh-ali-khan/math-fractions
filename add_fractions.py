# ------------------------------
# Get fractions with same denominator from user
# ------------------------------
num1 = int(input("First fraction - top: "))  # Numerator of first fraction
num2 = int(input("Second fraction - top: ")) # Numerator of second fraction
den = int(input("Common bottom number: "))   # Denominator (same for both)

# ------------------------------
# Add the fractions
# ------------------------------
total_top = num1 + num2      # Add numerators
total_bottom = den           # Denominator stays the same

# Show the result
print(f"{num1}/{den} + {num2}/{den} = {total_top}/{den}")

# ------------------------------
# Convert to mixed number if numerator >= denominator
# ------------------------------
if total_top >= total_bottom:
    whole_part = total_top // total_bottom   # Whole number part
    remainder = total_top % total_bottom    # Fraction remainder
    
    if remainder == 0:
        print(f"= {whole_part}")            # Only whole number
    else:
        print(f"= {whole_part} {remainder}/{den}")  # Mixed number

# ------------------------------
# Simplify fraction if possible
# ------------------------------
simplified = False
for i in range(2, min(total_top, total_bottom) + 1):
    if total_top % i == 0 and total_bottom % i == 0:
        new_top = total_top // i
        new_bottom = total_bottom // i
        print(f"Simplified: {new_top}/{new_bottom}")
        simplified = True
        break

# ------------------------------
# Already in simplest form check
# ------------------------------
if not simplified and total_top < total_bottom:
    print("Already in simplest form")
