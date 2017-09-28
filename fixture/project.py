from model.project import Project
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


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
                project_id = a_name.get_attribute('href').split("=")[1]
                name = a_name.text
                status = cells[1].text
                description = cells[4].text

                try:
                    i_enabled = cells[2].find_element_by_tag_name("i")
                    enabled = i_enabled is not None
                except NoSuchElementException:
                    enabled = False

                self.project_cache.append(Project(name=name, status=status, enabled=enabled, description=description, project_id=project_id))
        return list(self.project_cache)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_edit_page(id)
        wd.find_element_by_xpath("//input[@value='Delete Project'][@type='submit']").click()
        # переходим на страницу подтверждения удаления проекта
        delay = 3
        try:
            del_elem = WebDriverWait(wd, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Delete Project'][@type='submit']")))
            del_elem.click()
        except TimeoutException:
            print ("can't open confirmation page")
        self.project_cache = None


    def open_edit_page(self, id):
        wd = self.app.wd
        wd.get(self.app.base_url + "manage_proj_edit_page.php?project_id=" + str(id))


    def count(self):
        wd = self.app.wd
        self.open_project_page()
        return len(wd.find_elements_by_xpath("//div[@class='table-responsive' and position()=2]/table/tbody/tr"))

