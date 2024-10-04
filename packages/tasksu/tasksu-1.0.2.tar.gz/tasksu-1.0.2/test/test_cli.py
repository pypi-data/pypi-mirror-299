import pytest
import os
import datetime
from app import cli
from click.testing import CliRunner
from app.repositories.taskRepository import loadJson

@pytest.fixture()
def runner():
    cli.DATABASE = "tasks_test.json"
    yield CliRunner()
    #Teardown
    if os.path.exists(cli.DATABASE):
        os.remove(cli.DATABASE)

@pytest.fixture(scope="session")
def teardown():
    yield "Session scope"
    

def test_add(runner):  
    expectedUid = 1
    expectedTitle = "Hello World"
    expectedDesc = "Much wow"   
    result = runner.invoke(cli.add, [expectedTitle, expectedDesc])
    assert result.exit_code == 0
    results = loadJson(cli.DATABASE)
    assert expectedUid == results[0]['uid'], "Add command failed: UID is incorrect."
    assert expectedTitle in results[0]['title'], "Add command failed: Title is incorrect."
    assert expectedDesc in results[0]['description'], "Add command failed: Description is incorrect."

def test_list(runner):
    expectedTitle = "Title One"
    expectedDesc = "Something"   
    expectedStatus = "todo"
    expectedCreatedAt = datetime.date.today().strftime("%B %d, %Y")
    runner.invoke(cli.add, [expectedTitle, expectedDesc])
    result = runner.invoke(cli.list)
    assert result.exit_code == 0
    assert expectedTitle in result.output, "List command failed: Title is incorrect."
    assert expectedDesc in result.output, "List command failed: Description is incorrect."
    assert expectedStatus in result.output, "List command failed: Status is incorrect."
    assert expectedCreatedAt in result.output, "List command failed: Created At is incorrect."

def test_update(runner):
    uid = "1"
    firstTitle = 'Hello World'
    firstDesc = 'Much wow'
    expectedTitle = 'Goodbye World'
    expectedDesc = "I was updated!"
    runner.invoke(cli.add, [firstTitle, firstDesc])
    result = runner.invoke(cli.update, [uid, expectedTitle, "-d", expectedDesc])
    assert result.exit_code == 0
    results = loadJson(cli.DATABASE)
    assert expectedTitle in results[0]['title'], "Update command failed: Title is incorrect."
    assert expectedDesc in results[0]['description'], "Update command failed: Description is incorrect."
    assert results[0]['createdAt'] != results[0]['updatedAt'], "Update command failed: UpdatedAt is incorrect."
    assert firstTitle not in results[0]['title'], "Update command failed: Original title still exists."
    assert firstDesc not in results[0]['description'], "Update command failed: Original description still exists."
    
def test_updateInvalidUid(runner):
    uid = "asdf"
    expectedError = "Error: Invalid value: UID must be a valid interger."
    result = runner.invoke(cli.update, [uid, "Hello World"])
    assert result.exit_code == 2
    assert expectedError in result.output

def test_delete(runner):
    uidToDelete = "2"
    size = 1
    expectedTitle = 'Goodbye World'
    expectedDesc = "I was updated!"
    runner.invoke(cli.add, ['Hello World', 'Much wow'])
    runner.invoke(cli.add, [expectedTitle, expectedDesc])
    result = runner.invoke(cli.delete, [uidToDelete])
    assert result.exit_code == 0
    results = loadJson(cli.DATABASE)
    assert size == len(results), "Delete command failed: Size is incorrect."
    assert expectedTitle not in results[0]['title'], "Delete command failed: Title is incorrect."
    assert expectedDesc not in results[0]['description'], "Delete command failed: Description is incorrect."
    
def test_deleteInvalidUid(runner):
    uid = "asdf"
    expectedError = "Error: Invalid value: UID must be a valid interger."
    result = runner.invoke(cli.delete, [uid])
    assert result.exit_code == 2
    assert expectedError in result.output

def test_mark(runner):
    uid = "1"
    expectedStatus = "in-progress"
    runner.invoke(cli.add, ['Hello World', 'Much wow'])
    result = runner.invoke(cli.mark, [expectedStatus, uid])
    assert result.exit_code == 0
    results = loadJson(cli.DATABASE)
    assert expectedStatus in results[0]['status'], "Update command failed: Status is incorrect."
    
def test_markInvalid(runner):
    uid = "1"
    status = "invalid-status"
    expectedError = "Error: Status input is invalid."
    runner.invoke(cli.add, ['Hello World', 'Much wow'])
    result = runner.invoke(cli.mark, [status, uid])
    assert result.exit_code == 2
    assert expectedError in result.output