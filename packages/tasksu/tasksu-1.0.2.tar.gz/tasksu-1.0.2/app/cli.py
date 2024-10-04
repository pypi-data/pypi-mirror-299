import click
import importlib.metadata
from util.taskHelper import printTasks
from services import taskService

DATABASE = "tasks.json"
package_version = importlib.metadata.version('tasksu')

@click.group()
@click.version_option(package_version, prog_name="tasksu")
def cli():
    "Tasksu - a CLI Task Manager"

@cli.command(name="add")
@click.argument("title")
@click.argument("description")
def add(title, description):
    "Add a new task"
    taskService.saveTask(DATABASE, title, description)
    
@cli.command(name="update")
@click.argument("uid")
@click.argument("title")
@click.option(
    "-d",
    "--description",
    help="Updates the task description")
def update(uid, title, description):
    "Update the title or description of task"
    if str(uid).isdigit():
        taskService.updateById(DATABASE, int(uid), title, description)
    else:
        raise click.BadParameter("UID must be a valid interger.")
    
@cli.command(name="delete")
@click.argument("uid")
def delete(uid):
    "Delete a task"
    if str(uid).isdigit():
        taskService.deleteById(DATABASE, int(uid))
    else:
        raise click.BadParameter("UID must be a valid interger.")
    
    
@cli.command(name="list")
@click.option(
    "-s",
    "--status",
    help="Filter tasks by status: todo, in-progress, done",
)
def list(status):
    "Lists all tasks"
    tasks = []
    tasks = taskService.getAll(DATABASE, status)
    printTasks(tasks)
    
@cli.command(name="mark")
@click.argument("status")
@click.argument("uid")
def mark(status, uid):
    "Mark a task with an updated status"
    if not str(uid).isdigit():
        raise click.BadParameter("UID must be a valid interger.")
    if not isStatusValid(status):
        raise click.BadParameter("Error: Status input is invalid.")
    
    taskService.updateById(DATABASE, int(uid), status=status)
        
    
def isStatusValid(status):
    validStatus = { 
                    "todo", 
                    "in-progress", 
                    "done"
                    }
    return status in validStatus