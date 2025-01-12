import random
import math

# Promptar fråga om ett heltal och kontrollerar att det är ett heltal inom givet intervall
def input_valid_int(prompt, min_val, max_val):
    while True:
        try_input = input(prompt)

        if str.isdigit(try_input) and min_val <= int(try_input) <= max_val:
            return int(try_input)

        print(f'Talet måste vara ett positivt heltal')

# Promptar angedd fråga, kontrollerar om svaret finns i possible_answers
def input_valid_str(prompt, error_message, possible_answers):
    answer = input(prompt)

    while answer not in possible_answers:
        answer = input(f'{error_message}\n{prompt}')

    return answer

# Kontrollerar svaret på specifika ja/nej - frågor för att returnera ett booleskt värde
def check_yes_no(yes_or_no):
    if yes_or_no == 'y':
        return True
    else:
        return False

# Kontrollerar räknesättet (calc_method) för att bestämma vilket intervall som ska skickas till int_valid_input
def pick_number(calc_method):
    if calc_method == "*":
        number = input_valid_int("Välj en tabell (2-12): ", 2, 12)
        return number
    elif calc_method == "//" or calc_method == "%":
        number = input_valid_int("Välj divisior (2-5): ", 2, 5)

    return number #  Returnerar valt heltal

# Låter användaren välja dörr. Sparar både dörren och ett booleskt värde (False = zombies : True = no zombies) till dictionary "door_pick"
def pick_door(settings, current_question, door_pick):
    gen_zombie_door = random.randint(current_question, settings[0])
    picked_door = input_valid_int(f'\nVälj en dörr mellan {current_question} och {settings[0]} ', current_question, settings[0])

    door_pick["zombie_door"] = gen_zombie_door

    if picked_door == gen_zombie_door:
        door_pick["success"] = False
    else:
        door_pick["success"] = True

    return door_pick

# Avgör hur många förekomster som får ske av genererade heltal
def get_occurences_max(settings):
    occurences_max = 0

    if settings[0] < 14:
        occurences_max = 1
    if settings[0] >= 14 and settings[0] <= 26:
        occurences_max = 2
    if settings[0] >= 27 and settings[0] <= 39:
        occurences_max = 3

    return occurences_max

# Genererar nya slumpade heltal om max förekomster av det genererade talet nåtts 
def gen_rand_number(settings, generated_numbers):
    occurences_max = get_occurences_max(settings)
    
    while True:
        occurences = 0
        rand_int = random.randint(0, 12)

        for numbers in generated_numbers["numbers"]:  # Itererar över tidigare genererade heltal
            if numbers == rand_int:
                occurences += 1
        
        if occurences != occurences_max:  # Avbryt loopen om max förekomster inte nåtts
            break

    generated_numbers["numbers"].append(rand_int)  # Lägger till det genererade heltalet i "numbers" arrayen i dictionary "generated_numbers"
    return rand_int  # Returnerar det genererade heltalet

# Jämför användarens svar med det korrekta svaret beroende på valt räknesätt
def prompt_question(settings, generated_numbers):
    rand_int = gen_rand_number(settings, generated_numbers)

    if settings[1] == "*":
        correct = rand_int * settings[2]
        answer = input_valid_int(f'Vad blir {rand_int} {settings[1]} {settings[2]}? ', 0, math.inf)
    elif settings[1] == "//":
        correct = rand_int // settings[2]
        answer = input_valid_int(f'Vad blir {rand_int} {settings[1]} {settings[2]}? ', 0, math.inf)
    elif settings[1] == "%":
        correct = rand_int % settings[2]
        answer = input_valid_int(f'Vad blir {rand_int} {settings[1]} {settings[2]}? ', 0, math.inf)

    if answer == correct:
        generated_numbers["success"] = True
    else:
        generated_numbers["success"] = False

# Kallas i början av varje nytt spel för att användaren ska få ange antalet frågor, räknesätt och tillhörande faktor/divisor
def init_game():
    print(f'Lös lite matte, och välj rätt dörr, så slipper du bli uppäten av zombies.')
    num_questions = input_valid_int("Välj antal frågor (12-39st): ", 12, 39)
    calc_method = input_valid_str("Välj räknesätt (* , // , %): ", "Svaret måste vara en av (*, //, %)", ('*', '//', '%'))
    number = pick_number(calc_method)

    settings = (num_questions, calc_method, number)

    return settings  # Returnerar "settings" som en tuple

# Startpunkt i spelet. Styr flödeslogiken.
def playing_game(settings):
    while True:
        generated_numbers = {"numbers": [], "success": False}  # Dictionary {list, bool} för att lagra genererade slumptal och om svar var rätt eller inte
        door_pick = {"zombie_door": int, "success": bool}  # Dictionary {int, bool} för att lagra den slumpade zombie-dörren och om den valdes eller inte
        current_question = 0
        play_again_prompt = "Vill spela igen med samma inställningar? (y/n) "

        for current_question in range(1, settings[0] + 1):  # Loop intervall : 1 - antal angivna frågor
            print(f'\nFråga {current_question} av {settings[0]}')
            prompt_question(settings, generated_numbers)  # Ställer matematisk fråga
            if not generated_numbers["success"]:  # Kontrollerar om svaret var rätt eller fel
                print(f'\nÅhnej, fel svar! Du blir uppäten av zombies!')
                return check_yes_no(input_valid_str(play_again_prompt, "Du måste svara y/n", ('y', 'n')))  # Fråga om användaren vill spela igen

            print(f'Du svarade rätt på fråga {current_question} av {settings[0]}!')

            if current_question < settings[0]:
                pick_door(settings, current_question, door_pick)  # Ber användaren välja dörr
                if not door_pick["success"]:  # Kontrollerar om svaret var rätt eller fel
                    print(f'\nÅhnej, zombies bakom dörr {door_pick["zombie_door"]}!')
                    return check_yes_no(input_valid_str(play_again_prompt, "Du måste svara y/n", ('y', 'n')))  # Fråga om användaren vill spela igen
                else:
                    print(f'Zombies var bakom dörr {door_pick["zombie_door"]}')  # Skriver ut vilken dörr som hade zombies om användaren valde en dörr utan

        print(f'\nDu slipper bli uppäten! Bra jobbat!')  # Skrivs ut om användaren klarar alla frågor (for-loopen löpt hela vägen)

        return check_yes_no(input_valid_str(play_again_prompt, "Du måste svara y/n", ('y', 'n')))  # Fråga igen om användaren vann

# Startpunkt för programmet
def main():
    new_game_prompt = "Vill du starta ett nytt spel? (y/n) "

    while True:
        settings = init_game()

        play_again = True
        while play_again:
            play_again = playing_game(settings)  # Om return: True : startar om med samma inställningar
            if play_again:
                print(f'Startar om...\n')

        if not check_yes_no(input_valid_str(new_game_prompt, "Du måste svara y/n", ('y', 'n'))):
            print(f'Avslutar...')
            return

# Kallar main() första gången
main()