import os
from fuzzylogic.classes import Domain, Set, Rule
from matplotlib import pyplot
from fuzzylogic.functions import R, S, alpha
from fuzzylogic.functions import (sigmoid, gauss, trapezoid, 
                             triangular_sigmoid, rectangular, triangular)



pressure = Domain("Water Pressuer", 0, 100, res = 0.1)
pressure.low = S(0, 40)
#pressure.low.plot()
pressure.moderate = triangular(20, 60)
#pressure.moderate.plot()
pressure.high = R(40, 70)
#pressure.high.plot()
"""
pyplot.legend(["LOW", "MODERATE", "HIGH"])
pyplot.title("Water Pressure (psi)", fontweight = 'bold', fontsize = 15)
pyplot.show()"""


demand = Domain("Water Demand", 0, 100, res = 0.1)
demand.low = S(0,30)
#demand.low.plot()
demand.moderate = trapezoid(20, 40, 60, 80)
#demand.moderate.plot()
demand.high = trapezoid(60, 80, 100, 150)
#demand.high.plot()

"""pyplot.legend(["Low", "Moderate", "High"])
pyplot.title("Percentage of people using", fontweight ='bold', fontsize = 15)
pyplot.show()
"""
activation = Domain("Pump Activation", 0, 3, res=0.1)
activation.deactivate = S(0, 1)
#activation.deactivate.plot()
activation.half = trapezoid(0.5, 1, 2, 2.5)
#activation.half.plot()
activation.full = R(2, 3)
#activation.full.plot()

"""pyplot.legend(["Deactivate", "Half", "Full"], loc ="right")
pyplot.title("Pump Activation", fontweight = 'bold', fontsize = 15)
pyplot.show()
"""
rules = []
rules.append(Rule({(pressure.high, demand.low): activation.deactivate})) #1
rules.append(Rule({(pressure.high, demand.moderate): activation.deactivate})) #2
rules.append(Rule({(pressure.high, demand.high): activation.half})) #3
rules.append(Rule({(pressure.moderate, demand.low): activation.deactivate})) #4
rules.append(Rule({(pressure.moderate, demand.moderate): activation.deactivate})) #5
rules.append(Rule({(pressure.moderate, demand.high): activation.full})) #6
rules.append(Rule({(pressure.low, demand.low): activation.deactivate})) #7
rules.append(Rule({(pressure.low, demand.moderate): activation.half})) #8
rules.append(Rule({(pressure.low, demand.high): activation.full})) #9

"""RULES = Rule({(pressure.high, demand.low): activation.deactivate,
              (pressure.high, demand.moderate): activation.deactivate,
              (pressure.high, demand.high): activation.half,
              (pressure.moderate, demand.low): activation.deactivate,
              (pressure.moderate, demand.moderate): activation.deactivate,
              (pressure.moderate, demand.high): activation.full,
              (pressure.low, demand.low): activation.deactivate,
              (pressure.low, demand.moderate): activation.half,
              (pressure.low, demand.high): activation.full
})"""

imp = ["DEACTIVATE", "DEACTIVATE", "HALF", "DEACTIVATE", "DEACTIVATE", "FULL", "DEACTIVATE", "HALF", "FULL"]

def deactivate(u:float) -> float:
    if u >= 1:
        return 0
    return (1-u) / 1

def half(u:float) -> float:
    res = 0
    if u <= 0.5:
        return 0
    
    if u >= 0.5 and u <= 1:
        res = (u-0.5) / (1 - 0.5)
    elif u >= 1 and  u <= 2:
        res = 1.0
    elif u >= 2 and u <= 2.5:
        res = (u-2.5)/ (2.5 - 2)
    else:
        res = 0

    return res

def full(u:float) -> float:
    if u <= 2:
        return 0

    if u > 3:
        return 1.0
    return (u-2) / (3-2)

def low_pressure(u:float) -> float:
    if u >= 40:
        return 0
    
    #panaog
    return (40-u) / 40

def moderate_pressure(u:float) -> float:
    res = 0
    if u <= 20 or u >= 60:
        return 0
    
    #pasaka
    if u >= 20 and u <= 40:
        res = (u-20) / (40 - 20)
    #panaog
    elif u >= 40 and  u <= 60:
        res = (60 - u) / (60 - 40)
   
    return res

def high_pressure(u:float) -> float:
    if u <= 40:
        return 0

    #pasaka
    if u >= 40 and u <= 70:
        return (u-40)/ (70-40)
    
    return 1.0


def low_demand(u:float) -> float:
    if u >= 30:
        return 0
    return (30-u) / 30

def moderate_demand(u:float) -> float:
    res = 0
    if u <= 20 or u >= 80:
        return 0
    
    if u >= 20 and u <= 40:
        return (u-20) / (40-20)
    if u >= 40 and u <= 60:
        return 1.0
    if u >= 60 and  u <= 80:
        return (80-u)/ (80-60)
    

def high_demand(u:float) -> float:
    if u <= 60:
        return 0

    if u >= 60 and u <= 80:
        return (u-60)/ (80-60)
    
    return 1.0

def pressure_membership(press:float) -> list:
    return [low_pressure(press), moderate_pressure(press), high_pressure(press)]

def demand_membership(dem:float) -> list:
    return [low_demand(dem), moderate_demand(dem), high_demand(dem)]

def membership(cog:float) -> list:
    return [deactivate(cog), half(cog), full(cog)]


def max_idx(mem:list) -> int:
    max_value = mem[0]
    max_index = 0
    for i in range(1, len(mem)):
        if mem[i] > max_value:
            max_value = mem[i]
            max_index = i
    return max_index

if __name__ == "__main__":
    mem = ["Deactivate", "Half", "Full"]
    os.system("cls")
    while True:
        try:
            press = float(input("Enter pressure in (psi): "))
            dem = float(input("Enter demand in % (0-100): "))
            if dem < 0 or dem > 100:
                print("Invalid Input")
                input("Press enter to continue...")
                os.system("cls")
                continue    

            pres_mem = pressure_membership(press)
            dem_mem = demand_membership(dem)
            values = {pressure: press, demand: dem}
            print(f"Pressure Membership:  {pres_mem}")
            print(f"Demand Membership: {dem_mem}")

            """for i in range(len(rules)):
                
                print(f"Rule {i+ 1} : {rules[i](values)} -> {imp[i]}")
"""
            print(f"Rule {1} : {min(pres_mem[2], dem_mem[0])} -> {imp[0]}")
            print(f"Rule {2} : {min(pres_mem[2], dem_mem[1])} -> {imp[1]}")
            print(f"Rule {3} : {min(pres_mem[2], dem_mem[2])} -> {imp[2]}")
            print(f"Rule {4} : {min(pres_mem[1], dem_mem[0])} -> {imp[3]}")
            print(f"Rule {5} : {min(pres_mem[1], dem_mem[1])} -> {imp[4]}")
            print(f"Rule {6} : {min(pres_mem[1], dem_mem[2])} -> {imp[5]}")
            print(f"Rule {7} : {min(pres_mem[0], dem_mem[0])} -> {imp[6]}")
            print(f"Rule {8} : {min(pres_mem[0], dem_mem[1])} -> {imp[7]}")
            print(f"Rule {9} : {min(pres_mem[0], dem_mem[2])} -> {imp[8]}")
            COG = sum(rules)(values)

            print(f"\n\nCOG: {COG} ")
            print(f"Activation Membership: {membership(COG)}")  
            input("Press enter to exit...")
            os.system("cls")
            break
        except ValueError:
            print("Invalid Input")
            input("Press enter to continue...")
            os.system("cls")
            continue