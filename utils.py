#decorator

def log(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        
    return wrapper