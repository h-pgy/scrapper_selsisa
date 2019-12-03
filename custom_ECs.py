#expected conditions criadas por mim

class element_is_enabled:
  """An expectation for checking that an element is enabled.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.is_enabled()
        return element
    else:
        return False

