from fastapi import FastAPI, HTTPException
from app.database import read_db, write_db
from app.schemas import ClassCreate, StudentCreate

app = FastAPI(title="Gestion Ecole API")


@app.get("/")
def root():
    return {"message": "API gestion ecole fonctionne"}


@app.post("/classes")
def create_class(payload: ClassCreate):
    db = read_db()

    if any(c["name"].lower() == payload.name.lower() for c in db["classes"]):
        raise HTTPException(status_code=409, detail="Class name already exists")

    new_id = max([c["id"] for c in db["classes"]], default=0) + 1
    new_class = {"id": new_id, "name": payload.name, "student_ids": []}

    db["classes"].append(new_class)
    write_db(db)
    return new_class


@app.get("/classes")
def get_classes():
    db = read_db()
    return db["classes"]


@app.get("/classes/{class_id}")
def get_class_details(class_id: int):
    db = read_db()
    cls = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    students = [s for s in db["students"] if s["id"] in cls["student_ids"]]
    return {
        "id": cls["id"],
        "name": cls["name"],
        "students_count": len(cls["student_ids"]),
        "students": students
    }


@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    db = read_db()
    before = len(db["classes"])
    db["classes"] = [c for c in db["classes"] if c["id"] != class_id]

    if len(db["classes"]) == before:
        raise HTTPException(status_code=404, detail="Class not found")

    write_db(db)
    return {"deleted": True}


@app.get("/classes/{class_id}/students")
def list_students_of_class(class_id: int):
    db = read_db()
    cls = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    return [s for s in db["students"] if s["id"] in cls["student_ids"]]


@app.post("/students")
def create_student(payload: StudentCreate):
    db = read_db()

    new_id = max([s["id"] for s in db["students"]], default=100) + 1
    student = {
        "id": new_id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "grades": []
    }

    db["students"].append(student)
    write_db(db)
    return student


@app.get("/students/{student_id}")
def get_student(student_id: int):
    db = read_db()
    student = next((s for s in db["students"] if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/classes/{class_id}/students/{student_id}")
def add_student_to_class(class_id: int, student_id: int):
    db = read_db()

    cls = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    student = next((s for s in db["students"] if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student_id in cls["student_ids"]:
        raise HTTPException(status_code=409, detail="Student already in class")

    cls["student_ids"].append(student_id)
    write_db(db)
    return {"added": True, "class_id": class_id, "student_id": student_id}


@app.delete("/classes/{class_id}/students/{student_id}")
def remove_student_from_class(class_id: int, student_id: int):
    db = read_db()

    cls = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    if student_id not in cls["student_ids"]:
        raise HTTPException(status_code=404, detail="Student not in class")

    cls["student_ids"] = [sid for sid in cls["student_ids"] if sid != student_id]
    write_db(db)
    return {"removed": True, "class_id": class_id, "student_id": student_id}


@app.post("/students/{student_id}/grades")
def add_grade(student_id: int, grade: float):
    db = read_db()

    student = next((s for s in db["students"] if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if grade < 0 or grade > 20:
        raise HTTPException(status_code=400, detail="Grade must be between 0 and 20")

    student["grades"].append(grade)
    write_db(db)

    return {"student_id": student_id, "grade_added": grade}


@app.get("/students/{student_id}/average")
def student_average(student_id: int):
    db = read_db()

    student = next((s for s in db["students"] if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not student["grades"]:
        return {"student_id": student_id, "average": 0}

    avg = sum(student["grades"]) / len(student["grades"])
    return {"student_id": student_id, "average": round(avg, 2)}


@app.get("/classes/{class_id}/average")
def class_average(class_id: int):
    db = read_db()

    cls = next((c for c in db["classes"] if c["id"] == class_id), None)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    students = [s for s in db["students"] if s["id"] in cls["student_ids"]]

    all_grades = []
    for s in students:
        all_grades.extend(s["grades"])

    if not all_grades:
        return {"class_id": class_id, "average": 0}

    avg = sum(all_grades) / len(all_grades)
    return {"class_id": class_id, "average": round(avg, 2)}
