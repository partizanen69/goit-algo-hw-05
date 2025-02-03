# Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами.
# Написана функція для двійкового пошуку повинна повертати кортеж, де першим елементом є
# кількість ітерацій, потрібних для знаходження елемента. Другим елементом має бути
# "верхня межа" — це найменший елемент, який є більшим або рівним заданому значенню.
# Якщо елемент не знайдено, то верхня межа — це найближчий елемент, який є більшим за задане значення.

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return iterations, arr[mid]
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
            
        if left == right:
            return iterations, arr[left]
            
    if right < 0:
        return iterations, arr[0]
    if left >= len(arr):
        return iterations, arr[-1]
        
    return iterations, arr[left]

if __name__ == "__main__":
    arr = [1.5, 2.3, 3.7, 4.2, 5.9]
    target = 5.8
    iterations, upper_bound = binary_search(arr, target)
    print(f"Кількість ітерацій: {iterations}")
    print(f"Верхня межа: {upper_bound}")
