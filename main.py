import pygame
import time
import random

def citeste_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0  # Dacă fișierul nu există, high score-ul e 0

def salveaza_highscore(scor):
    with open("highscore.txt", "w") as f:
        f.write(str(scor))

# 1. Inițializare Pygame și setări fereastră
pygame.init()
latime, inaltime = 600, 400
ecran = pygame.display.set_mode((latime, inaltime))
pygame.display.set_caption('Snake Game - Proiectul meu')

# 2. Culori și constante
NEGRU = (0, 0, 0)
ALB = (255, 255, 255)
ROSU = (213, 50, 80)
VERDE = (0, 255, 0)
ALBASTRU = (50, 153, 213)

dimensiune_bloc = 10
viteza = 15
ceas = pygame.time.Clock()

pygame.font.init() 
font_stil = pygame.font.SysFont("bahnschrift", 25)
scor_font = pygame.font.SysFont("comicsansms", 35)

# 3. Funcția pentru desenarea șarpelui
def deseneaza_sarpe(bloc, lista_sarpe):
    for x in lista_sarpe:
        pygame.draw.rect(ecran, VERDE, [x[0], x[1], bloc, bloc])

def joc():
    game_over = False
    game_close = False
    high_score = citeste_highscore()

    # Poziția inițială
    x1, y1 = latime / 2, inaltime / 2
    x1_schimbare, y1_schimbare = 0, 0

    lista_sarpe = []
    lungime_sarpe = 1

    # Generare mâncare
    mancare_x = round(random.randrange(0, latime - dimensiune_bloc) / 10.0) * 10.0
    mancare_y = round(random.randrange(0, inaltime - dimensiune_bloc) / 10.0) * 10.0

    while not game_over:

        # Așteaptă decizia de restart sau quit după pierdere
        while game_close == True:
            ecran.fill(ALBASTRU)

            scor_final = lungime_sarpe - 1
            if scor_final > high_score:
                high_score = scor_final
                salveaza_highscore(high_score)

            mesaj_scor = font_stil.render(f"Scor curent: {scor_final}", True, ALB)
            mesaj_high = font_stil.render(f"High Score: {high_score}", True, VERDE)

            ecran.blit(mesaj_scor, [latime / 4, inaltime / 2.5])
            ecran.blit(mesaj_high, [latime / 4, inaltime / 2])

            mesaj_info = font_stil.render("Q - iesire, C - continuare", True, ALB )

            ecran.blit(mesaj_info, [latime / 4, inaltime / 40])

            # Aici poți adăuga un mesaj de "Ai pierdut! Apasă Q sau C"
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        joc()

        # 4. Controlul tastelor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_schimbare = -dimensiune_bloc
                    y1_schimbare = 0
                elif event.key == pygame.K_RIGHT:
                    x1_schimbare = dimensiune_bloc
                    y1_schimbare = 0
                elif event.key == pygame.K_UP:
                    y1_schimbare = -dimensiune_bloc
                    x1_schimbare = 0
                elif event.key == pygame.K_DOWN:
                    y1_schimbare = dimensiune_bloc
                    x1_schimbare = 0

        # 5. Verificare coliziune cu pereții
        if x1 >= latime or x1 < 0 or y1 >= inaltime or y1 < 0:
            game_close = True

        x1 += x1_schimbare
        y1 += y1_schimbare
        ecran.fill(NEGRU)
        
        # Desenare mâncare
        pygame.draw.rect(ecran, ROSU, [mancare_x, mancare_y, dimensiune_bloc, dimensiune_bloc])
        
        # Logica de creștere a șarpelui
        cap_sarpe = []
        cap_sarpe.append(x1)
        cap_sarpe.append(y1)
        lista_sarpe.append(cap_sarpe)
        
        if len(lista_sarpe) > lungime_sarpe:
            del lista_sarpe[0]

        # Verificare coliziune cu propriul corp
        for x in lista_sarpe[:-1]:
            if x == cap_sarpe:
                game_close = True

        deseneaza_sarpe(dimensiune_bloc, lista_sarpe)
        pygame.display.update()

        # 6. Verificare dacă a mâncat mâncarea
        if x1 == mancare_x and y1 == mancare_y:
            mancare_x = round(random.randrange(0, latime - dimensiune_bloc) / 10.0) * 10.0
            mancare_y = round(random.randrange(0, inaltime - dimensiune_bloc) / 10.0) * 10.0
            lungime_sarpe += 1

        ceas.tick(viteza)

    pygame.quit()
    quit()

joc()