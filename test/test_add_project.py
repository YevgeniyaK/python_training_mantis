from model.project import Project
from test.helper import random_string, random_status


def test_add_project(app):
    old_projects = app.soap.get_project_list()

    new_project = Project(name=random_string("qwerty", 10), status=random_status(), description="blablabla")
    app.project.create(new_project)
    new_projects = app.soap.get_project_list()

    assert len(old_projects) + 1 == len(new_projects)

    num_found = 0
    for project in new_projects:
        if project.name == new_project.name:
            num_found = num_found + 1
            new_project.project_id = project.project_id

    assert num_found > 0

    old_projects.append(new_project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

