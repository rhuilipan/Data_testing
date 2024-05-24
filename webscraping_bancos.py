import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
import pandas as pd
from pathlib import Path
import os
home = Path.home()
carpeta_descargas = Path.home()/"Downloads"
carpeta_destino = Path.home()/r"Documents\falabella_files"

print(f"RUT: {os.getenv('BANK_RUT_FALABELLA')}")
print(f"Password: {os.getenv('BANK_PASSWORD_FALABELLA')}")

rut = os.getenv('BANK_RUT_FALABELLA')
password_falabella = os.getenv('BANK_PASSWORD_FALABELLA')
password_bnco_chile = os.getenv('BANK_PASSWORD_B_CHILE')


def tiempo_aleatorio(a, b):
    return random.uniform(a, b)

def ingreso_user(banco):
    driver = webdriver.Chrome()
    driver.maximize_window() # For maximizing window
    if banco == 'falabella':
        driver.get("https://www.bancofalabella.cl/")
        #Ingreso:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-button"]'))).click()
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user"]'))).send_keys(rut)
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(password_falabella)
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-buttons"]/div/app-login-form/form/button'))).click()
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="dy-lb-close"]'))).click()
        except:
            pass
    elif banco == 'banco de chile':
        driver.get("https://portales.bancochile.cl/personas")
        #Ingreso:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ppp_header-link-banco_en_linea"]'))).click()
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="iduserName"]'))).send_keys(rut)
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(password_bnco_chile)
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idIngresar"]'))).click()
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-dialog-0"]/fenix-modal-zona-emergente/div/div/div/button'))).click()
        time.sleep(tiempo_aleatorio(6,12))
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn default btn pull-right"]'))).click()
        except:
            print("popup no encontrado")
            pass
    return driver

def descarga_hist(driver,banco,tipo=None,anio = None): #TODO: Clickear descarga excel
    if banco == 'falabella' and tipo =='cuenta_corriente':
        # Ir a cuenta corriente
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="darker bold product-name"][text()=" Cuenta Corriente "]'))).click()
        #Listado de Movimientos
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//p[@class="autoAdjustText"][text()="Listado de Movimientos"]'))).click()
        # Seleccionar lista desplegable:
        time.sleep(tiempo_aleatorio(5,8))
        select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@class="select-field_medium_label-medium"][@id="selectField_movimientos"]')))
        # Hacer clic en la lista desplegable
        time.sleep(tiempo_aleatorio(5,8))
        select_element.click()
        # Crear un objeto Select con la lista desplegable
        time.sleep(tiempo_aleatorio(5,8))
        select = Select(select_element)
        # Obtener todas las opciones visibles
        time.sleep(tiempo_aleatorio(5,8))
        options = select.options
        # Iterar sobre la selección
        for option in options:
            print(option.text)
            if option.text in ('Últimos movimientos','Mes en curso'):
                print(f"No se selecciona, opción {option.text}")
                pass
            else:
                print(f"Se seleccionó la fecha {option.text}")
                option.click()
                time.sleep(tiempo_aleatorio(5,8))
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//img[@class="collection-footer_export"]'))).click()
                time.sleep(tiempo_aleatorio(6,10))
                select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@class="select-field_medium_label-medium"][@id="selectField_movimientos"]')))
                # Crear un objeto Select con la lista desplegable
                time.sleep(tiempo_aleatorio(5,8))
                select_element.click()
    elif banco == 'falabella' and tipo == 'credito_elite':
        # Ir a CMR Mastercard Elite
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="darker bold product-name"][text()=" CMR Mastercard Elite "]'))).click()
        # Movimientos Facturados:
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"Movimientos Facturados")]'))).click()
        time.sleep(tiempo_aleatorio(5,8))
        # Seleccionar lista desplegable:
        try: 
            select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@class="form-control pointer select-movements"]')))
        except:
            select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@caption="Elige el mes"]')))
            pass
        # Hacer clic en la lista desplegable
        time.sleep(tiempo_aleatorio(5,8))
        select_element.click()
        # Crear un objeto Select con la lista desplegable
        time.sleep(tiempo_aleatorio(5,6))
        select = Select(select_element)
        # Obtener todas las opciones visibles
        options = select.options
        # Iterar sobre la selección
        for option in options:
            print(f"Se seleccionó la fecha {option.text}")
            option.click()
            time.sleep(tiempo_aleatorio(5,8))
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Exportar a Excel")]'))).click()
            time.sleep(tiempo_aleatorio(6,10))
            select_element.click()
    elif banco == 'banco de chile' and tipo =='cuenta_corriente': #Débito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Cuentas "]'))).click()##Cuentas
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Cartolas Históricas "]'))).click()##Cartola histórica
        ##Selección Filtro desde
        time.sleep(5)
        elemento_celda = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-0"]')))
        elemento_celda.send_keys(Keys.CONTROL + 'a')  # Seleccionar todo el texto
        elemento_celda.send_keys(f"01/{anio}")  # Reemplazar el texto
        del elemento_celda
        ##Selección Filtro hasta
        elemento_celda = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-input-1"]')))
        elemento_celda.clear()  # Elimina el texto existente en la celda
        elemento_celda.send_keys(Keys.CONTROL + 'a')  # Seleccionar todo el texto
        elemento_celda.send_keys(f"12/{anio}")  # Ingresa el nuevo texto

        #Selecionar largo filas
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-select-value-5"]'))).click() #Lista
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-option-6"]/span'))).click() #20

        # Encontrar los elementos de descarga
        # Encontrar todos los elementos que contienen el texto "Descargar"
        elementos_descarga = driver.find_elements(By.XPATH, '//span[@class="btn-text"][text()="Descargar"]')
        for elemento in elementos_descarga:
            elemento.click()
            time.sleep(tiempo_aleatorio(2, 6))
            opcion_excel = driver.find_element(By.XPATH, '//button[@role="menuitem"][contains(text(), " Descargar Excel ")]')
            print("¡Opción Excel encontrada!")    
            opcion_excel.click()
            time.sleep(tiempo_aleatorio(2, 6))  # Esperar unos segundos para que el archivo se descargue completamente
        print(f"Descarga {anio} exitoso!")
    elif banco == 'banco de chile' and tipo =='credito': #Crédito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Tarjeta de Crédito "]'))).click()##Tarjeta
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Movimientos Facturados "]'))).click()##Cartola histórica

        # Seleccionar lista desplegable:
        select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="mat-select-value"]')))
        # Hacer clic en la lista desplegable
        select_element.click()
        # Crear un objeto Select con la lista desplegable
        options = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//mat-option')))
        # Iterar sobre la selección
        for option in options:
            print(f"Se seleccionó la fecha {option.text}")
            option.click()
            time.sleep(tiempo_aleatorio(4,6))
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@class="mat-button btn btn-link mb-0 ng-star-inserted"]'))).click()
            time.sleep(tiempo_aleatorio(14,18))
            select_element.click()

def descarga_mes_act(driver,banco,tipo=None): #TODO: Clickear descarga excel
    if banco == 'falabella' and tipo =='cuenta_corriente':
        # Ir a cuenta corriente
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="darker bold product-name"][text()=" Cuenta Corriente "]'))).click()
        #Listado de Movimientos
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//p[@class="autoAdjustText"][text()="Listado de Movimientos"]'))).click()
        # Seleccionar lista desplegable:
        time.sleep(tiempo_aleatorio(5,8))
        select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@class="select-field_medium_label-medium"][@id="selectField_movimientos"]')))
        # Hacer clic en la lista desplegable
        time.sleep(tiempo_aleatorio(5,8))
        select_element.click()
        # Crear un objeto Select con la lista desplegable
        time.sleep(tiempo_aleatorio(5,8))
        select = Select(select_element)
        # Obtener todas las opciones visibles
        time.sleep(tiempo_aleatorio(5,8))
        options = select.options
        filtered_options = [option for option in options if option.text in ('Últimos movimientos', 'Mes en curso')]
        # Iterar sobre la selección
        for option in filtered_options:
            print(f"Se selecciona opción {option.text}")
            option.click()
            time.sleep(tiempo_aleatorio(5,8))
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//img[@class="collection-footer_export"]'))).click()
            time.sleep(tiempo_aleatorio(6,10))
            select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@class="select-field_medium_label-medium"][@id="selectField_movimientos"]')))
            time.sleep(tiempo_aleatorio(5,8))
            select_element.click()
    elif banco == 'falabella' and tipo == 'credito_elite':
        # Ir a CMR Mastercard Elite
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="darker bold product-name"][text()=" CMR Mastercard Elite "]'))).click()
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//img[@title="Exportar a Excel"]'))).click()
    elif banco == 'banco de chile' and tipo =='cuenta_corriente': #Débito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Cuentas "]'))).click()##Cuentas
        time.sleep(tiempo_aleatorio(3,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Saldos y Movimientos "]'))).click()##Cartola histórica
        
        # Encontrar los elementos de descarga
        # Encontrar todos los elementos que contienen el texto "Descargar"
        elementos_descarga = driver.find_elements(By.XPATH, '//span[@class="btn-text"][text()="Descargar"]')
        elementos_descarga[0].click()
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel = driver.find_element(By.XPATH, '//button[@role="menuitem"][contains(text(), " Descargar Excel ")]')
        print("¡Opción Excel encontrada!")
        opcion_excel.click()
        time.sleep(tiempo_aleatorio(2, 6))  # Esperar unos segundos para que el archivo se descargue completamente
    elif banco == 'banco de chile' and tipo =='credito': #Crédito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Tarjeta de Crédito "]'))).click()##Tarjeta
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Saldos y Movimientos No Facturados "]'))).click()##Saldos y Movimientos No Facturados
        time.sleep(tiempo_aleatorio(2, 6))
        #Seleccionar primer botón disponible de Descarga:
        elementos_descarga = driver.find_elements(By.XPATH, '//span[@class="btn-text"][text()="Descargar"]')
        elementos_descarga[0].click()
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel = driver.find_element(By.XPATH, '//button[@role="menuitem"][contains(text(), " Descargar Excel ")]')
        print("¡Opción Excel encontrada!")
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel.click()

def limpieza_mes_act(banco,tipo=None): #TODO: Clickear descarga excel.... In Progresss
    if banco == 'falabella' and tipo =='cuenta_corriente':
        ##archivos descargados se llaman "reportCollection (num)"
    elif banco == 'falabella' and tipo == 'credito_elite':
        ##archivos descargados no tienen formato logico
        # Ir a CMR Mastercard Elite


    elif banco == 'banco de chile' and tipo =='cuenta_corriente': #Débito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(tiempo_aleatorio(5,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Cuentas "]'))).click()##Cuentas
        time.sleep(tiempo_aleatorio(3,8))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Saldos y Movimientos "]'))).click()##Cartola histórica
        
        # Encontrar los elementos de descarga
        # Encontrar todos los elementos que contienen el texto "Descargar"
        elementos_descarga = driver.find_elements(By.XPATH, '//span[@class="btn-text"][text()="Descargar"]')
        elementos_descarga[0].click()
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel = driver.find_element(By.XPATH, '//button[@role="menuitem"][contains(text(), " Descargar Excel ")]')
        print("¡Opción Excel encontrada!")
        opcion_excel.click()
        time.sleep(tiempo_aleatorio(2, 6))  # Esperar unos segundos para que el archivo se descargue completamente
    elif banco == 'banco de chile' and tipo =='credito': #Crédito
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Mis Productos "]'))).click() #Mis productos
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()=" Tarjeta de Crédito "]'))).click()##Tarjeta
        time.sleep(tiempo_aleatorio(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()=" Saldos y Movimientos No Facturados "]'))).click()##Saldos y Movimientos No Facturados
        time.sleep(tiempo_aleatorio(2, 6))
        #Seleccionar primer botón disponible de Descarga:
        elementos_descarga = driver.find_elements(By.XPATH, '//span[@class="btn-text"][text()="Descargar"]')
        elementos_descarga[0].click()
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel = driver.find_element(By.XPATH, '//button[@role="menuitem"][contains(text(), " Descargar Excel ")]')
        print("¡Opción Excel encontrada!")
        time.sleep(tiempo_aleatorio(2, 6))
        opcion_excel.click()


### banco= ['falabella','banco de chile']
#banco = 'falabella'
banco = 'falabella'
driver = ingreso_user(banco)
#Falabella, cuenta corriente, 2023
#descarga_hist(driver,banco,"cuenta_corriente","2023")
descarga_hist(driver,banco,"credito_elite","2023")
descarga_mes_act(driver,banco,"cuenta_corriente")

