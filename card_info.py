import sqlite3
import random
import sys
# noinspection PyUnresolvedReferences
from icecream import ic

conn = sqlite3.connect("card.s3db")

cur = conn.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );""")

def card_num_generator():
    """Generates random card number."""
    base = 4000000000000000
    num = base + (random.randint(000000000, 999999999) * 10)

    luhn_list = [int(x) for x in str(num)]
    # Here is the luhn magic
    for i in range(0, 16, 2):
        luhn_list[i] = luhn_list[i] * 2
        if luhn_list[i] > 9:
            luhn_list[i] -= 9

    checksum = 10 - sum(luhn_list) % 10
    return num + checksum


def pin_generator():
    """Generates random PIN"""
    return random.randint(1000, 9999)


def add_customer(a, b):
    """Adds the card number and pin to the table."""
    cur.execute(f"""INSERT INTO card (number, pin)
VALUES ("{a}", "{b}")""")
    conn.commit()
    print(f"""Your card has been created
Your card number:
{a}
Your card PIN:
{b}""")


def check_entry(a, b):
    check = cur.execute(f"""SELECT EXISTS (
    SELECT *
    FROM
        card
    WHERE
        number = {a} AND pin = {b}
    );
""")
    for i, j in enumerate(check):
        val = j[0]
        if val == 0:
            return False
        else:
            return True


def show_bal(a):
    rows = cur.execute(f"""SELECT
    balance
FROM 
    card
WHERE
    number = {a}
;""")
    for i, j in enumerate(rows):
        print(f"Balance: {j[0]}")


def add_income(a, b):
    cur.execute(f"""UPDATE card
SET balance = balance + {a}
WHERE number = {b};""")
    conn.commit()
    print("Income was added!")


def luhn_check(a):
    base_list = list(str(a))
    for i in range(16):
        base_list[i] = int(base_list[i])

    for i in range(0, 15, 2):
        base_list[i] = 2 * base_list[i]
        for k in range(15):
            if base_list[k] > 9:
                base_list[k] -= 9

    if sum(base_list) % 10 == 0:
        return True
    else:
        return False


def card_num_check(a):
    check = cur.execute(f"""SELECT EXISTS( SELECT *
    FROM card
    WHERE number = {a});""")

    for i, j in enumerate(check):
        if j[0] == 1:
            return True
        else:
            return False


def balance_check(a, b):
    rows = cur.execute(f"""SELECT
    balance
FROM 
    card
WHERE
    number = {a}
;""")
    for i, j in enumerate(rows):
        if j[0] >= b:
            return True
        else:
            return False


def transfer_credit(a, b, c):
    cur.execute(f"""UPDATE card
SET balance = {a}
WHERE number = {b}""")  # Add money to designated card.
    cur.execute(f"""UPDATE card
SET balance = balance - {a}
WHERE number = {c}""")  # Remove money from user card.
    conn.commit()
    print("Success!")


def close_acc(a):
    cur.execute(f"""DELETE FROM card
WHERE number = {a}""")
    conn.commit()
    print("The account has been closed!")


while True:
    print("""1. Create an account
2. Log into account
0. Exit""")
    main_menu_opt = int(input())

    if main_menu_opt == 1:
        print()
        add_customer(card_num_generator(), pin_generator())
        print()
    elif main_menu_opt == 2:
        print()
        # Login info collection.
        card_num = int(input("Enter your card number:\n"))
        pin = int(input("Enter your PIN:\n"))
        print()
        if check_entry(card_num, pin) is False:
            print('Wrong card number or PIN!')
            print()
            continue
        else:
            print()
            print("You have successfully logged in!")
            print()
            while True:
                print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                login_menu_opt = int(input())

                if login_menu_opt == 1:
                    print()
                    show_bal(card_num)
                    print()
                elif login_menu_opt == 2:
                    print()
                    income = int(input('Enter income:\n'))
                    add_income(income, card_num)
                    print()
                elif login_menu_opt == 3:
                    print()

                    print("Transfer")
                    receiver_card_num = int(input('Enter card number:\n'))

                    if luhn_check(receiver_card_num) is True:
                        if card_num_check(receiver_card_num) is True:
                            amt_to_transfer = int(input('Enter how much money you want to transfer:\n'))
                            if balance_check(card_num, amt_to_transfer) is True:
                                transfer_credit(amt_to_transfer, receiver_card_num, card_num)
                            else:
                                print("Not enough money!")
                        else:
                            print("Such a card does not exist.")
                    else:
                        print("Probably you made a mistake in the card number. Please try again!")
                    print()
                elif login_menu_opt == 4:
                    print()
                    close_acc(card_num)
                    print()
                    break
                elif login_menu_opt == 5:
                    print()
                    print("You have successfully logged out!")
                    print()
                    break
                elif login_menu_opt == 0:
                    print()
                    print("Bye!")
                    print()
                    sys.exit()
    elif main_menu_opt == 0:
        print()
        print("Bye!")
        sys.exit()
    else:
        print()
        print("Enter a valid option.")
        print()
        continue
