import random
import time
from collections import deque

# Asignar valores a las cartas, A es el más alto
valores = {str(n): n for n in range(2, 11)}
valores.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14})
palos = ['♠', '♥', '♦', '♣']
mazo = [f'{carta}{palo}' for carta in valores for palo in palos]

# Mezclar y repartir
random.shuffle(mazo)
jugador1 = deque(mazo[:26])
jugador2 = deque(mazo[26:])

# Función para obtener valor numérico de la carta
def valor(carta):
    return valores[carta[:-1]]

# Juego principal
ronda = 1
while jugador1 and jugador2:
    print(f"\n🌀 Ronda {ronda}")
    print(f"Cartas restantes -> Jugador 1: {len(jugador1)} | Jugador 2: {len(jugador2)}")
    
    mesa1 = [jugador1.popleft()]
    mesa2 = [jugador2.popleft()]
    
    while True:
        print(f"Jugador 1 juega: {mesa1[-1]}  |  Jugador 2 juega: {mesa2[-1]}")
        v1 = valor(mesa1[-1])
        v2 = valor(mesa2[-1])
        
        if v1 > v2:
            print("➡️ Jugador 1 gana la ronda.")
            jugador1.extend(mesa1 + mesa2)
            break
        elif v2 > v1:
            print("➡️ Jugador 2 gana la ronda.")
            jugador2.extend(mesa1 + mesa2)
            break
        else:
            print("⚔️ ¡Guerra!")
            if len(jugador1) < 4:
                print("Jugador 1 no tiene suficientes cartas para la guerra.")
                jugador2.extend(jugador1 + mesa1 + mesa2 + list(jugador2))
                jugador1.clear()
                break
            elif len(jugador2) < 4:
                print("Jugador 2 no tiene suficientes cartas para la guerra.")
                jugador1.extend(jugador2 + mesa1 + mesa2 + list(jugador1))
                jugador2.clear()
                break
            for _ in range(3):
                mesa1.append(jugador1.popleft())
                mesa2.append(jugador2.popleft())
            mesa1.append(jugador1.popleft())
            mesa2.append(jugador2.popleft())
    
    print("====================")
    time.sleep(2)
    ronda += 1

# Resultado final
print("\n🎉 Resultado final:")
if jugador1:
    print("🏆 ¡Jugador 1 gana el juego con todas las cartas!")
else:
    print("🏆 ¡Jugador 2 gana el juego con todas las cartas!")
