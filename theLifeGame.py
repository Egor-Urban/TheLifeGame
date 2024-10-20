'''
The Life game
Developer: Urban Egor
Version: 2.7.234 r
'''

import numpy as np
import time
import os
import keyboard

ON = 255
OFF = 0
N = 30
updateInterval = 0.1
grid = np.random.choice([ON, OFF], N*N, p=[0.2, 0.8]).reshape(N, N)
rules = {"birth": [3], "survival": [2, 3]}  # стандартные правила игры

def update(grid, N, rules):
    newGrid = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) / 255)

            if grid[i, j] == ON:
                if total in rules["survival"]: 
                    newGrid[i, j] = ON
                else:
                    newGrid[i, j] = OFF
            else:
                if total in rules["birth"]: 
                    newGrid[i, j] = ON
    return newGrid

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def resize(grid, N):
    new_size_x = int(input("Введите новый размер поля по горизонтали (x): "))
    new_size_y = int(input("Введите новый размер поля по вертикали (y): "))
    new_grid = np.zeros((new_size_x, new_size_y), dtype=int)
    for i in range(min(len(grid), new_size_x)):
        for j in range(min(len(grid[0]), new_size_y)):
            new_grid[i][j] = grid[i][j]
    return new_grid, max(new_size_x, new_size_y)

def regenerate(grid):
    new_grid = np.random.choice([ON, OFF], len(grid)*len(grid[0]), p=[0.2, 0.8]).reshape(len(grid), len(grid[0]))
    return new_grid

def display_info(N, updateInterval):
    clear()
    print("Информация:")
    print("Разработчик: Urban Egor")
    print("Версия: 2.7.234 r")
    print(f"Размер поля: {N}x{N}")
    print(f"Скорость обновления: {updateInterval} сек")
    print("\n\n")

def load_grid_from_file(filename):
    try:
        with open("makets/"+filename, 'r') as file:
            lines = file.readlines()
            grid = []
            max_length = 0
            for line in lines:
                row = [int(cell) * ON for cell in line.strip()]
                grid.append(row)
                max_length = max(max_length, len(row))

            for i in range(len(grid)):
                while len(grid[i]) < max_length:
                    grid[i].append(OFF)

            while len(grid) < max_length:
                grid.append([OFF] * max_length)
            return np.array(grid)
    except FileNotFoundError:
        print("Файл не найден.")
        return None
    except ValueError as e:
        print(f"Ошибка при загрузке макета поля клетки: {e}")
        return None

def set_rules():
    try:
        birth_rule = input("Введите список соседей для рождения клетки: ").split(',')
        survival_rule = input("Введите список соседей для выживания клетки: ").split(',')
        rules["birth"] = [int(x) for x in birth_rule]
        rules["survival"] = [int(x) for x in survival_rule]
        print(f"Новые правила установлены: рождение {rules['birth']}, выживание {rules['survival']}")
    except ValueError:
        print("Ошибка ввода правил, попробуйте снова.")
        set_rules()

paused = False
mode = input("1 - Стандартная конфигурация / 2 - настройка")
if mode == "1":
    pass
elif mode == "2":
    updateInterval = float(input("Скорость (стандарт. 0.1, больше значение - медленнее симуляция) >> "))
    grid, N = resize(grid, N)
    set_rules()
else:
    pass

while True:
    if not paused:
        display_info(N, updateInterval)
        for row in grid:
            print(''.join('██' if cell == ON else '  ' for cell in row))
        print("\n" * 2)
        time.sleep(updateInterval)
        grid = update(grid, N, rules)

    if keyboard.is_pressed('p'):
        paused = not paused
        time.sleep(0.2)

    if paused:
        print("/help - список команд. 'p' - продолжить")
        command = input(">>> ").strip().lower()
        if command == 'p':
            paused = False
        elif command == "/help":
            print("/quit - выход")
            print("/speed - изменение скорости симуляции")
            print("/resize - изменение размера поля")
            print("/regenerate - перезапуск симуляции")
            print("/load - загрузить перфокарту")
            print("/rule - задать правила")
        elif command == '/quit':
            break
        elif command == "/speed":
            speed = float(input("Введите скорость симуляции (больше значение - меньше скорость, по умолчанию 0.1) >> "))
            updateInterval = speed
        elif command == "/resize":
            grid, N = resize(grid, N)
        elif command == "/regenerate":
            grid = regenerate(grid)
        elif command == "/load":
            filename = input("Введите имя файла с макетом поля клетки: ")
            loaded_grid = load_grid_from_file(filename)
            if loaded_grid is not None:
                N = len(loaded_grid)
                grid = loaded_grid
                print("Макет поля клетки успешно загружен.")
                time.sleep(1)
        elif command == "/rule":
            set_rules()
