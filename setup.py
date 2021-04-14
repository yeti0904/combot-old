print("Setting up ComBot..")
try:
    os.system("mkdir economies/accounts")
except:
    print("Failed to set up.")
    exit()
print("ComBot Economies set up.\nNow setting up admins and banned users.")
os.system("touch admins.txt && touch banned.txt")
print("Set up ComBot admin now?")
if input("(Y/N)").lower() == "y":
    id = str("What is your Discord account ID? (Turn on Developer mode and right click your icon, then click Copy ID) ")
    try:
        f = open("admins.txt","w")
        f.write(id)
        f.close()
    except:
        print("Error setting up admins")
print("ComBot setup finished!")
