import requests
from bs4 import BeautifulSoup
import pandas as pd

# Definir la URL base
base_url = 'https://caufy.com.ar/catalogo-de-productos-dropshipping/?product-page={}'

# Lista para almacenar los DataFrames de cada página
dfs = []

# Iterar sobre las páginas del 1 al 10
for page in range(1, 11):
    # Construir la URL para la página actual
    url = base_url.format(page)
    
    # Realizar la solicitud GET al sitio web
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el contenido HTML de la página
        html_content = response.text
        
        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Encontrar la lista de productos con la clase 'astra-shop-summary-wrap'
        products_list = soup.find_all('div', class_='astra-shop-summary-wrap')
        
        # Verificar si se encontraron productos
        if products_list:
            # Listas para almacenar nombres y precios de los productos
            product_names = []
            product_prices = []
            
            # Iterar sobre cada elemento de la lista de productos
            for product in products_list:
                # Extraer el nombre del producto (suponiendo que esté dentro de una etiqueta <h2>)
                product_name_tag = product.find('h2', class_='woocommerce-loop-product__title')
                if product_name_tag:
                    product_name = product_name_tag.text.strip()
                else:
                    product_name = 'Nombre no disponible'
                product_names.append(product_name)
                
                # Extraer el precio del producto (suponiendo que esté dentro de una etiqueta <span> con la clase 'woocommerce-Price-amount')
                product_price_tag = product.find('span', class_='woocommerce-Price-amount')
                if product_price_tag:
                    product_price = product_price_tag.text.strip()
                else:
                    product_price = 'Precio no disponible'
                product_prices.append(product_price)
            
            # Crear un DataFrame de Pandas con los nombres y precios de los productos de esta página
            df = pd.DataFrame({'Nombre del Producto': product_names, 'Precio': product_prices})
            
            # Agregar el DataFrame de esta página a la lista de DataFrames
            dfs.append(df)
        
        else:
            print("No se encontraron productos en la página {}.".format(page))
    
    else:
        print("No se pudo realizar la solicitud a la página {}.".format(page))

# Concatenar todos los DataFrames en uno solo
final_df = pd.concat(dfs)

final_df.to_csv("df_caufy")

# Imprimir el DataFrame final
print(final_df)