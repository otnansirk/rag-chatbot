import json

def check_stock(query: str) -> str:
    query_lower = query.lower()
    # Request to external API
    # EXAMPLE :
    # Response: {
    #     "status": "success",
    #     "data": {
    #         "sepatu": 12,
    #         "tas": 5
    #     }
    # }
    # Request in python:
    # respones = requests.get("https://api.example.com/stock", params={"query": query_lower})
    # data = response.json()
    # Json to String
    # knowlages = json.dumps(data)

    if "sepatu" in query_lower:
         response = {
            "status": "success",
            "data": {
                "sepatu": 12
            }
        }
    elif "tas" in query_lower:
        response = {
            "status": "success",
            "data": {
                "tas": 5
            }
        }
    else:
        response = {
            "status": "success",
            "message": "Maaf, stok produk tersebut tidak ditemukan dalam sistem."
        }

    return json.dumps(response)