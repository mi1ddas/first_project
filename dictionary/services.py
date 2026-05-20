# dictionary/services.py
# Здесь описана логика работы с внешними сервисами.

import requests
class ExternalDictionaryService:

    @staticmethod
    def get_hint_from_wikipedia(word: str) -> dict | None:
        search_url = "https://ru.wikipedia.org/w/api.php"
        search_params = {
            "action": "opensearch",
            "search": word,
            "limit": 1,
            "format": "json"
        }
        headers = {
         
            'User-Agent': 'MyITDictionaryBot/2.0 (contact: student@example.com)'
        }

        try:
           
            search_response = requests.get(
                search_url,
                params=search_params,
                headers=headers,
                timeout=5  
            )
            search_data = search_response.json()
            if not search_data[1]:
                return None

            article_title = search_data[1][0]  
            article_url = search_data[3][0]   
            extract_params = {
                "action": "query",
                "prop": "extracts",       
                "exintro": True,          
                "explaintext": True,      
                "exsentences": 3,        
                "titles": article_title,
                "format": "json"
            }

            extract_response = requests.get(
                search_url,
                params=extract_params,
                headers=headers,
                timeout=5
            )
            extract_data = extract_response.json()
            pages = extract_data.get("query", {}).get("pages", {})
            page = next(iter(pages.values())) 
            extract = page.get("extract", "").strip()

            if len(extract) > 400:
                extract = extract[:400].rstrip() + "..."

            return {
                "title": article_title,
                "extract": extract if extract else None,
                "url": article_url
            }

        except requests.exceptions.Timeout:
  
            print("Wikipedia API: timeout")
            return None

        except requests.exceptions.ConnectionError:
     
            print("Wikipedia API: connection error")
            return None

        except Exception as e:
           
            print(f"Wikipedia API: unexpected error — {e}")
            return None