import random
password = ""
# Paso 1
caracteres = [
    '+', '-', '/', '*', '!', '&', '$', '#', '?', '=', '@',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
]

#Paso 2
cantidad = int(input("¿Cuántos caracteres quieres que tenga tu contraseña?"))

#Paso 3
for i in range(cantidad):
    car_r = random.randint(1, 73)
    password += caracteres[car_r]
    

print(password)