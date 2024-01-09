from selenium import webdriver as wd

def test_lambdatest_playground():
    driver = wd.Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000")
    print(f"Title: {driver.title}")

# if __name__ == "__main__":
#     test_lambdatest_playground()