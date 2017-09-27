from model.project import Project
from selenium.common.exceptions import NoSuchElementException

class ProjectHelper:


    def __init__(self, app):
        self.app = app
        self.project_cache = None

    def open_add_project_page(self):
        wd = self.app.wd
        wd.get(self.app.base_url + "manage_proj_create_page.php")

    def open_project_page(self):
        wd = self.app.wd
        wd.get(self.app.base_url + "manage_proj_page.php")


    def create(self, project):
        wd = self.app.wd
        self.open_add_project_page()

        elm_name = wd.find_element_by_id("project-name")
        elm_name.click()
        elm_name.clear()
        elm_name.send_keys(project.name)

        wd.find_element_by_xpath("//select[@id='project-status']/option[text()='" + project.status + "']").click()

        elm_descr = wd.find_element_by_id("project-description")
        elm_descr.click()
        elm_descr.clear()
        elm_descr.send_keys(project.description)

        wd.find_element_by_xpath("//input[@type='submit']").click()
        self.project_cache = None

    def get_project_list(self):
        self.open_project_page()
        if self.project_cache is None:
            wd = self.app.wd
            self.project_cache = []
            for element in wd.find_elements_by_xpath("//div[@class='table-responsive' and position()=2]/table/tbody/tr"):
                cells = element.find_elements_by_tag_name("td")
                a_name = cells[0].find_element_by_tag_name("a")
                name = a_name.text
                status = cells[1].text
                description = cells[4].text

                try:
                    i_enabled = cells[2].find_element_by_tag_name("i")
                    enabled = i_enabled is not None
                except NoSuchElementException:
                    enabled = False

                self.project_cache.append(Project(name=name, status=status, enabled=enabled, description=description))
        return list(self.project_cache)
