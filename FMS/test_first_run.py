from selenium import webdriver as wd

def test_lambdatest_playground():
    driver = wd.Chrome()
    driver.maximize_window()
    driver.get("https://richie003.pythonanywhere.com/blog/7/")
    print(f"Title: {driver.title}")

if __name__ == "__main__":
    test_lambdatest_playground()