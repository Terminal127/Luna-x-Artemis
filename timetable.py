import pandas as pd

class_names = {
    "DBMS": "Database Management System",
    "COA": "Computer Architecture",
    "OOPJ": "Object Oriented Programming Lab",
    "VT(L)": "AWS Lab",
    "DSS": "Discrete Maths",
    "OS": "Operating System",
    "STW": "Scientific and Technical writing",
    "ICOA": "Introduction to Computer Organization and Architecture",
    "OS(L)": "Operating System LAB",
    "DBMS(L)": "Database Management LAB"
}

def get_classes(day):
    
    data = pd.read_csv("timetable.csv")
    classes = data[data["DAY"] == day.upper()].iloc[:, 2:-2]
    classes = classes.fillna("").stack().dropna()

    classes = classes.map(class_names)
    return classes

# Get the day from the user
day = input("Enter the day (MON, TUE, WED, THU, FRI, SAT): ").upper()

classes = get_classes(day)

if classes.empty:
    print("You don't have any classes on", day)
else:
    print("Your classes on", day, "are:")
    for time, class_name in classes.items():
        print(f"- {time}: {class_name}")
