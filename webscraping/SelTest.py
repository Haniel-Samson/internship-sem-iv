from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.python.org")
#driver.save_screenshot('screnshot.png')
print(driver.title)
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")

elem.clear()
elem.send_keys("applw")
elem.send_keys(Keys.RETURN)


assert "No results found."  not in driver.find_element(By.CLASS_NAME, "list-recent-events.menu")
driver.close()