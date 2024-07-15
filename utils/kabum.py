from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller


def scrape_kabum(query):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')

    # Automatically install the correct version of ChromeDriver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options)

    results = []

    try:
        # Access the link
        driver.get(
            f'https://www.kabum.com.br/busca/{query}?page_number=1&page_size=100')

        # Wait until the elements are present
        driver.implicitly_wait(10)

        # Locate all specified elements
        elements = driver.find_elements(
            By.XPATH, '//*[@id="listing"]/div[3]/div/div/div[2]/div/main/article')

        # Iterate through each found element and collect its data
        for element in elements:
            text = element.text.split('\n')
            if len(text) >= 4:
                item = {
                    'title': element.find_element(By.CLASS_NAME, 'nameCard').text,
                    'price': element.find_element(By.CLASS_NAME, 'priceCard').text,
                    'link': element.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    'image_link': element.find_element(By.TAG_NAME, 'img').get_attribute('src'),
                    'store': 'https://static.kabum.com.br/conteudo/icons/logo.svg',
                }
                results.append(item)

    finally:
        # Close the browser
        driver.quit()
        print('Kabum complete!')

    return results


if __name__ == "__main__":
    # Example usage
    query = '4060'
    data = scrape_kabum(query)
    for i, item in enumerate(data, start=1):
        print(f'Element {i}:')
        print('Title:', item['title'])
        print('Price:', item['price'])
        print('Link:', item['link'])
        print('Image Link:', item['image_link'])
        print('---')
