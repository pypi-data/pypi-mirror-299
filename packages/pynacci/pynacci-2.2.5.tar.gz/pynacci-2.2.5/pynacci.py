import math

__version__ = "2.2.5"  

def fibonacci(iter=10):
    """Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci, comenzando con 1."""
    try:
        if iter < 0:
            raise ValueError("El número de iteraciones no puede ser negativo.")
        sequence = []
        a, b = 1, 1  
        for _ in range(iter):
            sequence.append(a)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("El argumento 'iter' debe ser un entero.")

def fibonacci_generator():
    """Generador que produce los números de la serie de Fibonacci de manera indefinida, comenzando con 1."""
    a, b = 1, 1 
    while True:
        yield a
        a, b = b, a + b

def is_perfect_square(x, include_negative=False, include_zero=False):
    """Verifica si un número es un cuadrado perfecto."""
    try:
        if x < 0 and include_negative == False:
            return False
        if include_negative:
            x = abs(x)
        if x == 0 and include_zero == False:
            return False
        elif x == 0 and include_zero:
            return True
        s = int(math.sqrt(x))
        return s * s == x
    except TypeError:
        raise TypeError("El argumento 'x' debe ser un número.")

def is_fibonacci(n):
    """Devuelve True si el número 'n' es un número de Fibonacci, False en caso contrario."""
    if n < 0:
        return False
    try:
        return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_n(n):
    """Devuelve el n-ésimo número de Fibonacci, comenzando con 1."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        a, b = 1, 1  
        for _ in range(n):
            a, b = b, a + b
        return a
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_sum(n):
    """Devuelve la suma de los primeros 'n' números de Fibonacci, comenzando con 1."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        a, b = 1, 1  
        total = 0
        for _ in range(n):
            total += a
            a, b = b, a + b
        return total
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_less_than(n):
    """Devuelve una lista con todos los números de Fibonacci menores que 'n', comenzando con 1."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        result = []
        a, b = 1, 1  
        while a < n:
            result.append(a)
            a, b = b, a + b
        return result
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número.")

def golden_ratio(n, diff=False):
    """Calcula la aproximación de la razón dorada usando los dos últimos 'n' términos de Fibonacci, comenzando con 1."""
    try:
        phi = (1 + math.sqrt(5)) / 2
        if n <= 0:
            raise ValueError("El número debe ser mayor que cero.")
        a, b = 1, 1  
        for _ in range(n):
            a, b = b, a + b
        if diff == False:
            return b / a if a != 0 else None
        else:
            return phi - (b / a) if a != 0 else None
    
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_remainder(n, m):
    """Devuelve una lista con los primeros 'n' números de Fibonacci resto 'm', comenzando con 1."""
    try:
        if n < 0 or m <= 0:
            raise ValueError("'n' no puede ser negativo y 'm' debe ser mayor que cero.")
        sequence = []
        a, b = 1, 1  
        for _ in range(n):
            sequence.append(a % m)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("Los argumentos 'n' y 'm' deben ser números enteros.")

def is_divisible_by_fibonacci(n, return_divisors=False):
    """
    Devuelve True si 'n' es divisible por algún número de Fibonacci mayor que 1.
    Si 'return_divisors' es True, devuelve la lista de los números de Fibonacci que dividen a 'n'.
    """
    try:
        if n <= 0:
            raise ValueError("El número debe ser mayor que cero.")
        a, b = 1, 1  
        divisors = [] 
        
        while a <= n:
            if a > 1 and n % a == 0:
                if return_divisors:
                    divisors.append(a)  
                else:
                    return True  # Si no se necesita la lista, devuelve True inmediatamente
            a, b = b, a + b
        
        # Si se solicita la lista de divisores
        if return_divisors:
            return divisors
        else:
            return False
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def custom_fibonacci(n, first=1, second=1):
    """Genera los primeros 'n' números de una secuencia de Fibonacci personalizada, comenzando con los valores indicados."""
    try:
        if n < 0:
            raise ValueError("El número 'n' no puede ser negativo.")
        sequence = []
        a, b = first, second
        for _ in range(n):
            sequence.append(a)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("Los argumentos 'n', 'first' y 'second' deben ser números enteros.")
    
def fibonacci_list(start=0, stop=5, step=1):
    """Devuelve una lista de números de Fibonacci desde 'start' hasta 'stop', con saltos 'step', comenzando con 1."""
    if step == 0:
        raise ValueError("El argumento 'step' no puede ser 0, ya que causaría un bucle infinito.")
    elif start == stop:
        return []
    elif start > stop:
        raise ValueError("El argumento 'start' no puede ser mayor que 'stop'.")
    
    sequence = fibonacci(stop)
    if step < 0:
        return sequence[stop:start:step]
    else:
        return sequence[start:stop:step]


def show_help():
    """Muestra una lista de las funciones disponibles en la librería `pynacci` junto con una breve descripción y ejemplos de uso."""
    print("""
    === Funciones disponibles en la librería `pynacci` ===
    
    1. fibonacci(iter=10):
       - Descripción: Devuelve una lista con los primeros `iter` números de la secuencia de Fibonacci.
       - Parámetros: 
         - iter (int): Número de elementos de Fibonacci que se quieren generar. El valor por defecto es 10.
       - Ejemplo:
         fibonacci(5)  # Devuelve [1, 1, 2, 3, 5]
    
    2. fibonacci_generator():
       - Descripción: Generador que produce números de Fibonacci indefinidamente.
       - Ejemplo:
         gen = fibonacci_generator()
         next(gen)  # Devuelve 1
         next(gen)  # Devuelve 1
    
    3. is_perfect_square(x):
       - Descripción: Verifica si un número `x` es un cuadrado perfecto.
       - Parámetros:
         - x (int): El número a verificar.
       - Ejemplo:
         is_perfect_square(16)  # Devuelve True
         is_perfect_square(15)  # Devuelve False
    
    4. is_fibonacci(n):
       - Descripción: Determina si el número `n` es parte de la secuencia de Fibonacci.
       - Parámetros:
         - n (int): El número a verificar.
       - Ejemplo:
         is_fibonacci(21)  # Devuelve True
         is_fibonacci(22)  # Devuelve False
    
    5. fibonacci_n(n):
       - Descripción: Devuelve el `n`-ésimo número de la secuencia de Fibonacci.
       - Parámetros:
         - n (int): El índice del número de Fibonacci que se quiere obtener.
       - Ejemplo:
         fibonacci_n(7)  # Devuelve 13
    
    6. fibonacci_sum(n):
       - Descripción: Devuelve la suma de los primeros `n` números de Fibonacci.
       - Parámetros:
         - n (int): Cantidad de números de Fibonacci a sumar.
       - Ejemplo:
         fibonacci_sum(5)  # Devuelve 7 (1 + 1 + 2 + 3)
    
    7. fibonacci_less_than(n):
       - Descripción: Devuelve una lista con todos los números de Fibonacci menores que `n`.
       - Parámetros:
         - n (int): El límite superior para los números de Fibonacci.
       - Ejemplo:
         fibonacci_less_than(50)  # Devuelve [1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    8. golden_ratio(n):
       - Descripción: Calcula la aproximación del número áureo usando los dos últimos `n` términos de Fibonacci.
       - Parámetros:
         - n (int): Cantidad de términos de Fibonacci a considerar.
       - Ejemplo:
         golden_ratio(10)  # Devuelve aproximadamente 1.618
    
    9. fibonacci_remainder(n, m):
       - Descripción: Devuelve una lista con los primeros `n` números de Fibonacci, calculados módulo `m`.
       - Parámetros:
         - n (int): Número de elementos de Fibonacci que se quieren generar.
         - m (int): Módulo para la operación de resto.
       - Ejemplo:
         fibonacci_remainder(5, 3)  # Devuelve [1, 1, 2, 0, 2]
    
    10. is_divisible_by_fibonacci(n, return_divisors=False):
        - Descripción: Verifica si `n` es divisible por algún número de Fibonacci mayor que 1. 
        - Parámetros:
          - n (int): El número a verificar.
          - return_divisors (bool): Si es `True`, devuelve la lista de divisores de Fibonacci. El valor por defecto es `False`.
        - Ejemplo:
          is_divisible_by_fibonacci(21)  # Devuelve True
          is_divisible_by_fibonacci(21, return_divisors=True)  # Devuelve [3, 21]
    
    11. custom_fibonacci(n, first=1, second=1):
        - Descripción: Genera una secuencia personalizada de Fibonacci comenzando con los valores `first` y `second`.
        - Parámetros:
          - n (int): Cantidad de elementos a generar.
          - first (int): El primer valor de la secuencia.
          - second (int): El segundo valor de la secuencia.
        - Ejemplo:
          custom_fibonacci(5, first=2, second=3)  # Devuelve [2, 3, 5, 8, 13]
    
    12. fibonacci_list(start, stop, step):
        - Descripción: Devuelve una lista de números de Fibonacci desde `start` hasta `stop` con el paso `step`.
        - Parámetros:
          - start (int): El índice de inicio de la secuencia.
          - stop (int): El índice final de la secuencia.
          - step (int): El salto entre los números de Fibonacci. Soporta pasos negativos.
        - Ejemplo:
          fibonacci_list(0, 10, 2)  # Devuelve [1, 2, 5, 13, 34]
          fibonacci_list(10, 0, -1)  # Devuelve [55, 34, 21, 13, 8, 5, 3, 2, 1, 1]
    """)

__all__ = ['fibonacci', 'fibonacci_generator', 'is_perfect_square', 'is_fibonacci', 'fibonacci_n', 'fibonacci_sum',
           'fibonacci_less_than', 'golden_ratio', 'fibonacci_remainder', 'is_divisible_by_fibonacci', 'custom_fibonacci', 'fibonacci_list', 'show_help']
