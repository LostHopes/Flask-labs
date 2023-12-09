# Лабораторна №13 API for CRUD Todo

## 1. Requests (Запити)

Вміст файлу *views.py* блюпринта api

### 1.1 GET /todos - get list of todos (Отримання всіх завдань)

```python
@api.route("/todos/")
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        todo_dict = {
            "id": todo.id,
            "task": todo.task,
            "status": todo.status,
            "category": todo.category,
            "user_id": todo.user_id
        }
        todos_list.append(todo_dict)
    return jsonify(todos_list), 200
```

### 1.2 POST /todos - create a new task (Створення завдання)

```python
@api.route("/todos/", methods=["POST"])
def create_task():
    data = request.get_json()
    task = data.get("task")
    user_id = data.get("user_id")
    todo = Todo(task=task, user_id=user_id)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "Task was added to the todo list"}), 201
```

### 1.3 GET /todos/id - get task info (Отримання одного завдання)

```python
@api.route("/todos/<int:id>")
def get_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "task": task.task,
        "status": task.status,
        "category": task.category,
        "user_id": task.user_id
    }), 200
```

### 1.4 PUT /todos/id - update task (Оновлення завдання)

```python
@api.route("/todos/<int:id>", methods=["PUT"])
def update_task(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    todo.task = data.get("task")
    todo.status = data.get("status")
    todo.category = data.get("category")
    todo.user_id = data.get("user_id")
    db.session.commit()

    return jsonify({"message": "Task was updated"}), 200
```

### 1.5 DELETE /todos/id - delete task (Видалення завдання)

```python
@api.route("/todos/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"The task with id {id} was deleted"}), 200
```

## 2. TODO API tests (Тестування TODO API за допомогою Postman)

### 2.1 GET /todos - get list of todos (Отримання всіх завдань)

![image](/screenshots/lab13/lab13_1.png)

### 2.2 POST /todos - create a new task (Створення завдання)

![image](/screenshots/lab13/lab13_2.png)

Створене завдання

![image](/screenshots/lab13/lab13_3.png)

### 2.3 GET /todos/id - get task info (Отримання одного завдання)

![image](/screenshots/lab13/lab13_4.png)

### 2.4 PUT /todos/id - update task (Оновлення завдання)

![image](/screenshots/lab13/lab13_5.png)

Оновлене завдання

![image](/screenshots/lab13/lab13_6.png)

### 2.5 DELETE /todos/id - delete task (Видалення завдання)

![image](/screenshots/lab13/lab13_7.png)

Видалене завдання

![image](/screenshots/lab13/lab13_8.png)