with open("mails.txt", "r") as f:
    mails = f.read().splitlines()

for mail in mails:
    print(mail.split("|")[0])