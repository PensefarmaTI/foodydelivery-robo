from datetime import *

def log(func):
    def wrapper(*args, **kwargs):
        data = datetime.now().strftime("%d/%m/%Y")
        # Registrar informações antes da chamada de função
        function_name = func.__name__
        arguments = ', '.join([repr(args) for args in args])
        kwargs_str = ', '.join([f'{key}={value}' for key, value in kwargs.items()])
        all_args = ', '.join(filter(None, [arguments, kwargs_str]))

        result  = func(*args, **kwargs)
        result += f'{data}'
        
        data = data.replace('/','-')

        # print(result)
        with open(f'log/{data}.txt', 'a+') as f:
            f.write(result)

    return wrapper