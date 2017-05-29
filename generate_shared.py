import sys
import random
import math

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

if __name__ == '__main__':
    p = 0x00ae0f0301f2ce3a97f40a5bded472bf9a168463aa1557b9888f502163d36f8f275816d971f3a40d3783dbe012077819d1081e5df45e978e26a03f2bc33aacf999998ca4673e551604d956c4b7641b534f74b7e96ffe27cc7f586e01c988d23e928abfc66125f97e73c6159622a6fa36551f0d40e8033a7245922ec797f6ebefac316e81641943527826a62dd62c83383f2b74e3e88b6210986c6dd54a9df092188f926294c87150550c862c2c74fd6bb7536c63ff121c7c82f6bfa5c466df8a2498de95f2ee65b62e1af7f1e2a441b50526c7d763bdb2e2da497bf6dde1b0552a39b91ca90e4f335465bf9483143c034e771b6245adc505c87e128f2054ecbce3
    g = 2

    # Bind input to raw_input for Python 2 support
    try:
        input = raw_input
    except NameError:
        pass

    # Check for input args
    if len(sys.argv) < 2:
        print ("Usage: python generate_shared.py <name>")
        sys.exit()
    name = sys.argv[1]

    # Avoid inputs that contain , as it is used as a delimiter
    if "," in name:
        print("Please enter a name that does not contain a comma.")
        sys.exit()

    # Pick random secret key
    a = random.randint(1, p - 1)

    # Fetch secrets database
    f = open("shared_secrets.txt", "r")
    secrets = [x.strip().split(",") for x in f.readlines()]
    f.close()

    # Check for existing entry
    row = -1
    for i, secret in enumerate(secrets):
        if name == secret[0]:
            row = i
            break
       
    # Loop only if the name exists
    while row is not -1:
        print("The provided name already exists. Overwrite?[y/n]")
        answer = input()
        if answer == "y":
            break
        elif answer == "n":
            sys.exit()

    # Save secret key with this particular partner   
    if row is -1:
        f = open("secrets.txt", "a") 
        f.write(name + "," + str(a) + "\n")
        f.close()
    else:
        replace_line("secrets.txt", row, name + "," + str(a) + "\n")
        print("Overwritten.")

    # Show g^a to the user
    g_to_a = pow(g, a, p)
    print("Send this to the other person:", g_to_a)

    # Recieve number from the partner
    print("Paste number recieved from other person:")
    g_b = int(input())

    # Compute shared secret
    g_b_a = pow(g_b, a, p)

    # Save shared secret with this particular partner
    if row is -1:
        f_out = open("shared_secrets.txt", "a")
        f_out.write(name + "," + str(g_b_a) + "\n")
        f_out.close()
    else:
        replace_line("shared_secrets.txt", row, name + "," + str(a) + "\n")
        print("Overwritten.")

    # Inform user of success
    print("Success")