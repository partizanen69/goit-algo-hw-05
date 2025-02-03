# Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа 
# на основі двох текстових файлів (стаття 1, стаття 2). 
# Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, 
# та іншого — вигаданого (вибір підрядків за вашим бажанням). На основі отриманих 
# даних визначте найшвидший алгоритм для кожного тексту окремо та в цілому.

import timeit


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def test_each_algorithm(article: str, substring: str) -> None:
  time_boyer_moore = timeit.timeit(
    lambda: boyer_moore_search(article, substring), 
    number=100
  )
  time_kmp = timeit.timeit(
    lambda: kmp_search(article, substring), 
    number=100
  )
  time_rabin_karp = timeit.timeit(
    lambda: rabin_karp_search(article, substring), 
    number=100
  )
  
  print(f"Time for substring: {substring}")
  print(f"Boyer-Moore search: {time_boyer_moore}")
  print(f"KMP search: {time_kmp}")
  print(f"Rabin-Karp search: {time_rabin_karp}")
  
  min_algorithm = min({
    "boyer_moore": time_boyer_moore,
    "kmp": time_kmp,
    "rabin_karp": time_rabin_karp
  }.items(), key=lambda x: x[1])
  print(f"Fastest algorithm: {min_algorithm[0]} with time {min_algorithm[1]}\n")
  

if __name__ == "__main__":
  with open("article1_utf8.txt", "r") as file:
    article1 = file.read()
  
  print('Testing article1')
  pattern_exists = "middle-1, забираючи другу частину"
  pattern_does_not_exist = "middle-1, забиEEEEEраючи другу частину"
  
  test_each_algorithm(article1, pattern_exists)
  test_each_algorithm(article1, pattern_does_not_exist)
  
  with open("article2.txt", "r") as file:
    article2 = file.read()
  
  print('\nTesting article2\n')
  pattern_exists = "кількість агентів 524288"
  pattern_does_not_exist = "кількість агEEEнтів 524288"
  
  test_each_algorithm(article2, pattern_exists)
  test_each_algorithm(article2, pattern_does_not_exist)
  