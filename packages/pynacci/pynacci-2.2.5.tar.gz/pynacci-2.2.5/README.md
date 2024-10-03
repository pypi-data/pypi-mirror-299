
# pynacci

`pynacci` es una librería de Python que te permite trabajar con la secuencia de Fibonacci de múltiples formas, ofreciendo varias funciones útiles para generar, manipular, y analizar números de Fibonacci.

## Instalación

La librería no tiene dependencias externas. Simplemente descárgala y colócala en tu proyecto.

## Uso

A continuación, se detallan las funciones disponibles en la librería.

### 1. `fibonacci(iter=10)`

Devuelve una lista con los primeros `iter` números de la serie de Fibonacci.

**Ejemplo:**
```python
fibonacci(5)  # [1, 1, 2, 3, 5]
```

### 2. `fibonacci_generator()`

Generador que produce los números de la serie de Fibonacci de manera indefinida.

**Ejemplo:**
```python
gen = fibonacci_generator()
[next(gen) for _ in range(5)]  # [1, 1, 2, 3, 5]
```

### 3. `is_perfect_square(x)`

Verifica si un número es un cuadrado perfecto.

**Ejemplo:**
```python
is_perfect_square(16)  # True
```

### 4. `is_fibonacci(n)`

Devuelve `True` si el número `n` es un número de Fibonacci, `False` en caso contrario.

**Ejemplo:**
```python
is_fibonacci(21)  # True
is_fibonacci(22)  # False
```

### 5. `fibonacci_n(n)`

Devuelve el `n`-ésimo número de Fibonacci.

**Ejemplo:**
```python
fibonacci_n(7)  # 13
```

### 6. `fibonacci_sum(n)`

Devuelve la suma de los primeros `n` números de Fibonacci.

**Ejemplo:**
```python
fibonacci_sum(5)  # 7 (0 + 1 + 1 + 2 + 3)
```

### 7. `fibonacci_less_than(n)`

Devuelve una lista con todos los números de Fibonacci menores que `n`.

**Ejemplo:**
```python
fibonacci_less_than(50)  # [1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### 8. `golden_ratio(n)`

Calcula la aproximación de la razón dorada usando los dos últimos `n` términos de Fibonacci.

**Ejemplo:**
```python
golden_ratio(10)  # Aproximadamente 1.618
```

### 9. `fibonacci_remainder(n, m)`

Devuelve una lista con los primeros `n` números de Fibonacci, pero con el resto de su división entre `m`.

**Ejemplo:**
```python
fibonacci_remainder(5, 3)  # [1, 1, 2, 0, 2]
```

### 10. `is_divisible_by_fibonacci(n, return_divisors=False)`

Devuelve `True` si `n` es divisible por algún número de Fibonacci mayor que 1.
Si `return_divisors=True`, devuelve la lista de los números de Fibonacci que dividen a `n`.

**Ejemplo:**
```python
is_divisible_by_fibonacci(21)  # True
is_divisible_by_fibonacci(22)  # False
is_divisible_by_fibonacci(21, return_divisors=True)  # [3, 21]
```

### 11. `custom_fibonacci(n, first=1, second=1)`

Genera los primeros `n` números de una secuencia de Fibonacci personalizada con los dos primeros valores dados.

**Ejemplo:**
```python
custom_fibonacci(5, first=2, second=3)  # [2, 3, 5, 8, 13]
```

### 12. `fibonacci_list(start, stop, step)`

Devuelve una lista de números de Fibonacci desde `start` hasta `stop`, con saltos `step`. Soporta pasos positivos y negativos.

**Ejemplo:**
```python
fibonacci_list(0, 10, 2)  # [1, 2, 5, 13, 34]
fibonacci_list(10, 0, -1)  # [55, 34, 21, 13, 8, 5, 3, 2, 1, 1]
```

### 13. `show_help()`

Muestra la lista de funciones disponibles y sus descripciones.

**Ejemplo:**
```python
show_help()
```
