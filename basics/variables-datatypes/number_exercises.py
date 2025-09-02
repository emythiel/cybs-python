import sys

# Future age
# Script that asks for age (input) and stores it as a variable.
# - Print how old you will be in 100 years
# - Print what year it will be, when you turn 100. Assume current year is 2025.

age_input = input("Input your age: ")
if age_input.isdigit() == False:
    sys.exit("That's not a number!")

age = int(age_input)

print("Age after 100 years: " + str(age + 100))
print("Year when you turn 100: " + str(((100 - age)) + 2025))


# Skateboarding
# Two friends skateboard and does tricks. But they suck at math.
# They want to know what direction their skateboard would be facing,
# if they add the angle from their favourite tricks together.
# - spinning_heelflip = 360
# - vert_900 = 900
# - pop_shove_it = 270
# Make a program that calculate final angle, keeping in mind that a full turn is 360 degrees, and start point is 0.

spinning_heelflip = 360
vert_900 = 900
pop_shove_it = 270

total_spin = spinning_heelflip + vert_900 + pop_shove_it
final_angle = total_spin % 360
print("Final angle: " + str(final_angle) + "°")

print("Number of spins: " + str(total_spin / 360))
