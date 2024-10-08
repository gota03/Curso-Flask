from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    print(data)
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    print(new_task)
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({
        'message': 'Tarefa criada com sucesso'
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        'task': task_list,
        'total_tasks': len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({'message': 'Não encontrada task'}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if task == None:
        return jsonify({'message': 'Não foi possível encontrar a task'}), 404
    
    data = request.get_json()
    task.title =  data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({'message': 'Tarefa atualizada com sucesso'})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({
            'message': 'Nenhuma tarefa encontrada'
        }), 404

    tasks.remove(task)
    return jsonify({
        'message': 'Tarefa deletada com sucesso'
    })


if __name__ == '__main__':
    app.run(debug=True)
