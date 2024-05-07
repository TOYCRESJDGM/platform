import os
from time import sleep
from logger import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.common.exceptions import NoSuchElementException


def scrapper_platform(cufe):
    """Scrapes information related to the given CUFE from the DIAN website.

    Parameters:
    cufe (str): The CUFE (Código Único de Factura Electrónica) to be searched.

    Returns:
        tuple: A tuple containing information about the invoice if found, otherwise None.
    """

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    opts.add_argument("--disable-extensions")
    opts.add_experimental_option("detach", True)
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument('--disable-extensions')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-infobars')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-browser-side-navigation')
    opts.add_argument('--disable-gpu')
    opts.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    logger.info('Obteniendo información...')

    driver.get(os.getenv('VPFE_URL'))
    sleep(5) # proteccion Recaptcha

    num_attempts = int(os.getenv('ATTEMPTS', 3))

    for attempt in range(num_attempts):
    
        try:
            input = driver.find_element(By.XPATH, "//input[@id='DocumentKey']")

            if input:
                input.clear()
                input.send_keys(cufe)

                driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Buscar')]").click()

                receptor, transmitter, total_taxes, invoice_info = get_data(driver)
                url_pdf = get_pdf(driver)
                events = records_events(driver)


            driver.quit()

            return  receptor, transmitter, total_taxes, invoice_info, url_pdf, events

        except NoSuchElementException as e:
            logger.error("Error: No se encontró el elemento")
            if attempt < num_attempts - 1:
                sleep(2)
                logger.info("Intentando nuevamente...")
                continue
            else:
                logger.info("Se agotaron los intentos")
                break
    
    driver.quit()
    return None
   
def get_data(driver):
    """Locates all elements in the HTML to extract information.

    Parameters:
    driver (webdriver): The Selenium WebDriver instance.

    Returns:
        receptor (dict): Information about the receiver.
        transmitter (dict): Information about the transmitter.
        total_taxes (dict): Information about the total and taxes.
        invoice_info (dict): Information about the invoice.
    """
    logger.info('Obteniendo información de la factura')
    # Localiza el elemento que contiene la información del receptor y el emisor
    data_transmitter = driver.find_element(By.XPATH, "//p[span[contains(@class, 'datos-receptor') and contains(text(), 'EMISOR')]]")
    data_receptor = driver.find_element(By.XPATH, "//p[span[contains(@class, 'datos-receptor') and contains(text(), 'RECEPTOR')]]")

    # Localiza el elemento que contiene la información de totales e impuestos
    data_total = driver.find_element(By.XPATH, "//div[p[contains(text(), 'TOTALES E IMPUESTOS')]]")

    # Localiza el elemento que contiene la información de la factura
    invoice_information = driver.find_element(By.XPATH, "//p[span[contains(@class, 'tipo-doc')]]")

    receptor = map_data(data_receptor.text)
    transmitter = map_data(data_transmitter.text)
    total_taxes = map_data(data_total.text)
    invoice_info = map_data(invoice_information.text)
    
    return receptor, transmitter, total_taxes, invoice_info


def map_informacion(data):
    """Maps information about the receiver, transmitter, and totals.

    Parameters:
    data (list): A list containing lines of data.

    Returns:
        total_data (dict): A dictionary containing mapped information.
    """

    #Mapea la información del receptor, emisor y totales
    total_data = {}
    for linea in data:
        key, value = linea.split(':')
        total_data[key.strip()] = value.strip()
    return total_data


def map_factura(data):
    """Maps information about the invoice.

    Parameters:
    data (list): A list containing lines of data.

    Returns:
        invoice_data (dict): A dictionary containing mapped invoice information.
    """
    #Mapea la información de la factura
    invoice_data = {}
    for linea in data:
        if 'Descargar PDF' in linea:
            continue
        key, value = linea.split(':')
        invoice_data[key.strip()] = value.strip()
    return invoice_data
 
  
def map_data(entity_data: str ):
    """Maps the given entity data to the appropriate data structure.

    Parameters:
    entity_data (str): The string representation of entity data.

    Returns:
        dict: A dictionary containing mapped entity information.
    """
    
    datos = entity_data.split('\n')
    tipo_entidad = datos[0]

    if tipo_entidad == 'Factura electrónica':
        return map_factura(datos[1:-1])
    else:
        return map_informacion(datos[1:])
    

def get_pdf(driver):
    """Gets the URL of the graphical representation (PDF) of the invoice.

    Parameters:
    driver: WebDriver object.

    Returns:
    url_pdf (str): The URL of the PDF representation.
    """
    #Obtiene la url de la representación grafica

    enlace_pdf = driver.find_element(By.CSS_SELECTOR, "a.downloadPDFUrl")
       
    url_pdf = enlace_pdf.get_attribute("href")

    return url_pdf


def records_events(driver):
    """Records the events related to the invoice.

    Parameters:
    driver: WebDriver object.

    Returns:
    records_event (list): A list of dictionaries containing the recorded events.
    """

    logger.info('Obteniendo listado de eventos')

    events = driver.find_elements(By.XPATH, "//div[@id='container1']//tbody/tr")
    records_event = []

    for event in events:
        code = event.find_element(By.XPATH, ".//td[1]").text
        description = event.find_element(By.XPATH, ".//td[2]").text
        date = event.find_element(By.XPATH,".//td[3]").text
        nit_emisor = event.find_element(By.XPATH,".//td[4]").text
        emisor = event.find_element(By.XPATH,".//td[5]").text
        nit_receptor = event.find_element(By.XPATH,".//td[6]").text
        receptor = event.find_element(By.XPATH,".//td[7]").text

        if code and description:
            record = {
                'code' :code,
                'description': description,
                'date': date,
                'nit_emisor': nit_emisor,
                'name_emisor': emisor,
                'nit_receptor': nit_receptor,
                'name_receptor': receptor
            }

            records_event.append(record)
        
    return records_event