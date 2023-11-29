from flask import jsonify
from app import app
from ..skills.data import data


app.add_url_rule("/api/skills/", endpoint="get_skills")
app.add_url_rule("/api/skills/<int:idx>", endpoint="get_skills")

@app.endpoint("get_skills")
def get_skills(idx=None) -> dict|int:
    my_skills = data.my_skills
    if idx is None:
        return jsonify(my_skills)
    return jsonify(my_skills.get(idx))
