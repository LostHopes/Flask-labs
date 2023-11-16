import json
import os


my_skills = {
        1: [
            "Programming", "Languages: Python, C++, JavaScript, PHP, Java Frameworks: Flask, Django, Spring", 75],
        2: ["Running", "Skills 2", 50],
        3: ["Linguistics", "Skill 3", 50],
        4: ["Soft skills", "Skill 4", 50],
        5: ["Fast reading and comprehension", "Skill 5", 100],
        6: ["Tinkering", "Skill 6", 75]
}


def auth(user=None, password=None):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.json")

    with open(path, "r") as f:
        data = json.load(f)

    if user is not None and password is not None:
        data["user"] = user
        data["password"] = password
        with open(path, 'w') as f:
            json.dump(data, f)
    return data