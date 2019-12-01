from aocd import data


total_fuel = 0
real_total_fuel = 0

modules = [int(module) for module in data.splitlines()]

for module in modules:
    fuel = module // 3 - 2
    total_fuel += fuel
    real_total_fuel += fuel

    while True:
        fuel = fuel // 3 - 2
        if fuel > 0:
            real_total_fuel += fuel
        else:
            break

print('Part 1:', total_fuel)
print('Part 2:', real_total_fuel)
