from model.project import Project
import random
from test.helper import random_string, random_status

def test_delete_project(app):
    if app.project.count() == 0:
        app.project.create(Project(name=random_string("qwerty", 10), status=random_status(), description="blablabla"))

    list_projects = app.project.get_project_list()
    project = random.choice(list_projects)
    app.project.delete_project_by_id(project.project_id)
    new_list = app.project.get_project_list()

    assert len(list_projects) - 1 == len(new_list)
