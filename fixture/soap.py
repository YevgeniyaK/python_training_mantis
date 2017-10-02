from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:
    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.config["soap"]["url"])
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False


    def get_project_list(self):
        client = Client(self.app.config["soap"]["url"])

        project_cache = []
        for data in client.service.mc_projects_get_user_accessible(self.app.config['web']['username'], self.app.config['web']['password']):
            project_cache.append(Project(name=data.name, status=data.status.name, enabled=data.enabled, description=data.description, project_id=data.id))

        return project_cache

