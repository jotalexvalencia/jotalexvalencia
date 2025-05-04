"""
Este script descarga los últimos artículos de Hashnode, Medium y Dev.to,
y actualiza el README.md con un bloque de "Latest Articles".
"""

import requests
from bs4 import BeautifulSoup
# import time # Ya no es necesario el sleep manual aquí

def get_hashnode_articles():
    """
    Obtiene los últimos artículos desde el RSS de Hashnode usando requests + BeautifulSoup.
    """
    url = "https://jorgealexandervalencia.hashnode.dev/rss.xml"
    print(f"Intentando obtener artículos de Hashnode desde: {url}")
    try:
        # User-Agent más descriptivo y timeout
        headers = {"User-Agent": "Mozilla/5.0 (compatible; PythonReadmeVUpdater/1.0; +https://github.com/jotalexvalencia/jotalexvalencia)"}
        # time.sleep(5) # Eliminado - El error 429 debe manejarse o evitarse con menos frecuencia de ejecución
        response = requests.get(url, headers=headers, timeout=15) # Timeout de 15 segundos
        response.raise_for_status()

        # Usar parser XML para RSS feed
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:3] # Obtener los 3 más recientes

        articles = []
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            guid_tag = item.find('guid') # A veces usado como URL alternativa

            title = title_tag.text if title_tag else "Sin título"
            # Usar link si existe, si no, intentar con guid
            url = link_tag.text if link_tag and link_tag.text else guid_tag.text if guid_tag else '#'
            articles.append({"title": title, "url": url})
        return articles
    except requests.exceptions.HTTPError as http_err:
        status_code = getattr(http_err.response, 'status_code', None)
        if status_code == 429:
            print(f"Error 429: Demasiadas solicitudes a Hashnode ({url}). Intenta ejecutar el script más tarde o con menos frecuencia.")
        else:
            print(f"Error HTTP {status_code} obteniendo artículos de Hashnode ({url}): {http_err}")
        return []
    except requests.exceptions.Timeout:
        print(f"Error: Timeout al intentar conectar con Hashnode ({url}).")
        return []
    except requests.exceptions.RequestException as req_err:
         print(f"Error de conexión/solicitud obteniendo artículos de Hashnode ({url}): {req_err}")
         return []
    except Exception as e:
        # Captura cualquier otro error durante el parsing o procesamiento
        print(f"Error inesperado procesando artículos de Hashnode ({url}): {e}")
        return []

def get_devto_articles():
    """
    Obtiene los últimos artículos desde la API pública de Dev.to.
    """
    url = "https://dev.to/api/articles?username=aljutupapa"
    print(f"Intentando obtener artículos de Dev.to desde: {url}")
    try:
        # Añadir timeout
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        # Devuelve solo los campos necesarios y limita a 3 artículos
        articles_data = response.json()[:3]
        return [{"title": article.get('title', 'Sin título'), "url": article.get('url', '#')} for article in articles_data]
    except requests.exceptions.HTTPError as http_err:
        status_code = getattr(http_err.response, 'status_code', None)
        print(f"Error HTTP {status_code} en la solicitud a Dev.to ({url}): {http_err}")
        return []
    except requests.exceptions.Timeout:
        print(f"Error: Timeout al intentar conectar con Dev.to ({url}).")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a Dev.to ({url}): {e}")
        return []
    except Exception as e:
        # Captura errores de parsing JSON u otros
        print(f"Error inesperado procesando artículos de Dev.to ({url}): {e}")
        return []


def get_medium_articles():
    """
    Obtiene los últimos artículos desde el feed RSS de Medium usando requests + BeautifulSoup.
    """
    url = "https://medium.com/@jorgealexandervalencia/feed"
    print(f"Intentando obtener artículos de Medium desde: {url}")
    try:
        # User-Agent más descriptivo y timeout
        headers = {"User-Agent": "Mozilla/5.0 (compatible; PythonReadmeVUpdater/1.0; +https://github.com/jotalexvalencia/jotalexvalencia)"}
        response = requests.get(url, headers=headers, timeout=15) # Timeout de 15 segundos
        response.raise_for_status()

        # Usar parser XML para RSS feed
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:3] # Obtener los 3 más recientes

        articles = []
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            guid_tag = item.find('guid') # Medium a veces usa guid como permalink

            title = title_tag.text if title_tag else "Sin título"
            # Priorizar link si existe, si no, intentar con guid
            url = link_tag.text if link_tag and link_tag.text else guid_tag.text if guid_tag else '#'
            articles.append({"title": title, "url": url})
        return articles
    except requests.exceptions.HTTPError as http_err:
        status_code = getattr(http_err.response, 'status_code', None)
        print(f"Error HTTP {status_code} obteniendo artículos de Medium ({url}): {http_err}")
        return []
    except requests.exceptions.Timeout:
        print(f"Error: Timeout al intentar conectar con Medium ({url}).")
        return []
    except requests.exceptions.RequestException as req_err:
         print(f"Error de conexión/solicitud obteniendo artículos de Medium ({url}): {req_err}")
         return []
    except Exception as e:
        # Captura cualquier otro error durante el parsing o procesamiento
        print(f"Error inesperado procesando artículos de Medium ({url}): {e}")
        return []

def update_readme(articles):
    """
    Lee el archivo README.md, busca la sección '## 📝 Latest Articles',
    la reemplaza con la lista actualizada de artículos y guarda los cambios.
    """
    readme_path = "README.md"
    start_marker = "## 📝 Latest Articles"
    end_marker = "<!-- LATEST_ARTICLES_END -->"

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        if start_index == -1 or end_index == -1:
            print(f"Error: No se encontraron los marcadores '{start_marker}' o '{end_marker}' en {readme_path}")
            print("Asegúrate de que tu README.md contenga una sección como esta:")
            print(f"{start_marker}")
            print("... (contenido antiguo aquí) ...")
            print(f"{end_marker}")
            return

        # Asegurarse de que el marcador de inicio esté antes del de fin
        if start_index >= end_index:
             print(f"Error: El marcador '{start_marker}' aparece después o en la misma posición que '{end_marker}' en {readme_path}")
             return

        articles_section = start_marker + "\n\n" # Añade un salto de línea extra para formato
        if articles:
            for article in articles:
                # Usar .get() con valores por defecto por seguridad
                title = article.get('title', 'Artículo sin título').strip()
                url = article.get('url', '#')
                articles_section += f"- [{title}]({url})\n"
        else:
            articles_section += "No hay artículos recientes para mostrar.\n" # Mensaje si no se obtienen artículos

        articles_section += "\n" + end_marker # Añade un salto de línea antes del marcador final

        # Construir el nuevo contenido
        # Parte antes del marcador + nueva sección + parte después del marcador
        new_content = content[:start_index] + articles_section + content[end_index + len(end_marker):]

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Archivo {readme_path} actualizado exitosamente!")
    except FileNotFoundError:
        print(f"Error: El archivo {readme_path} no fue encontrado en el directorio actual.")
    except Exception as e:
        print(f"Error inesperado actualizando {readme_path}: {e}")

if __name__ == "__main__":
    print("Iniciando la actualización de artículos...")

    hashnode_articles = get_hashnode_articles()
    print(f"Obtenidos {len(hashnode_articles)} artículos de Hashnode.")

    devto_articles = get_devto_articles()
    print(f"Obtenidos {len(devto_articles)} artículos de Dev.to.")

    medium_articles = get_medium_articles()
    print(f"Obtenidos {len(medium_articles)} artículos de Medium.")

    # Combinar todas las listas de artículos
    all_articles = hashnode_articles + devto_articles + medium_articles

    # Opcional: Ordenar por fecha si estuviera disponible, o simplemente mantener el orden de obtención
    # all_articles.sort(key=lambda x: x.get('published_at', ''), reverse=True) # Ejemplo si tuvieras fecha

    # Limitar al total deseado si es necesario (ej. los 5 más recientes en total)
    # MAX_ARTICLES = 5
    # all_articles = all_articles[:MAX_ARTICLES]

    if all_articles:
        print(f"Actualizando README.md con {len(all_articles)} artículos...")
        update_readme(all_articles)
    else:
        print("No se obtuvieron artículos de ninguna fuente para actualizar el README.md.")
        # Opcional: podrías querer actualizar el README con un mensaje "No hay artículos"
        # update_readme([]) # Descomentar si quieres que se actualice aunque no haya artículos

    print("Proceso finalizado.")
