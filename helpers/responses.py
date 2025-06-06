# responses.py

def success(data=None, message="Success", code=200):
    return {
        "meta" : {
            "status": "success",
            "message": message,
            "code": code
        },
        "data": data
    }

def error(message="Something went wrong", code=400, errors=None):
    return {
        "meta": {
            "status": "error",
            "message": message,
            "code": code
        },
        "errors": errors
    }
