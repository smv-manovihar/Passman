import ast
from cryptography.fernet import Fernet
import random
import string
import os
import time
from rich import print as printc
from pwinput import pwinput
from rich.console import Console
import shutil

def pass_generator(p_len, numbers = True, special_charecters = True):
    letters = string.ascii_letters
    digits = string.digits
    special = '#@$&%'
    charecters = letters
    if numbers:
        charecters +=  digits
    if special_charecters:
        charecters +=  special      
    pwd=""
    condition = False
    has_number = False
    has_special = False
    while not condition or len(pwd) < p_len:
        new_cha = random.choice(charecters)
        pwd += new_cha
        if new_cha in digits:
            has_number = True
        elif new_cha in special:
            has_special = True
        condition = True
        if numbers:
            condition = has_number
        if special_charecters:
            condition = condition and has_special    
    return pwd

def sp_pass_generator(p):
    chars=['@', "#", "$", "&"]
    p=p.capitalize()
    p=p+random.choice(chars)+str(random.randint(10,10000))
    return p

def change_mpass(data,mpass,new_mpass):
    if new_mpass==mpass:
        return data
    data[new_mpass]=data[mpass]
    del data[mpass]
    return data

def genkey(profile):
    global file_path
    fpath=os.path.join(file_path,f'{profile}.key')
    key=Fernet.generate_key() #Generates a random key to encrypt and decrypt
    with open(fpath,"wb") as f:
        f.write(key)

def data_encryption(profile,data):
    global file_path
    fpath=os.path.join(file_path,f"{profile}.key")
    try:
        with open(fpath,"rb") as f: #Extracting Key from the file to encrypt
            key=f.read()
    except FileNotFoundError:
        genkey(profile)
        with open(fpath,"rb") as f:
            key=f.read()
    k=Fernet(key) #Assigning to a variable
    #Writing Encrpyted data into a pass(random extension made by me) file
    fpath=os.path.join(file_path,f'{profile}.pass')
    with open(fpath,"w") as f:
        f.write(data)
    with open(fpath,"rb") as og:
        og_data=og.read()
    en_data=k.encrypt(og_data)
    with open(fpath,"wb") as en:
        en.write(en_data)

def data_decryption(profile):
    global file_path
    fpath=os.path.join(file_path,f"{profile}.key")
    with open(fpath,"rb") as f: #Extracting Key from the file to decrypt
        key=f.read()
    k=Fernet(key)
    #Retrieving Data from the file and Decrypt
    fpath=os.path.join(file_path,f'{profile}.pass')
    with open(fpath,"rb") as en:
        en_data=en.read()
    de_data=k.decrypt(en_data)
    return de_data.decode('ascii') #Returning as a string (as it is binary)

def new_username(dic):
    platform=input("Enter the website: ")
    username=input("Enter the username or email: ")
    password=input("Enter the password: ")
    printc("[green]Your password has been saved![/]")
    for i in dic:
        if i==platform:
            dic[i].append({username:password})
            return dict(dic)
    dic.update({platform:[{username:password}]})
    return dict(dic)

def new_profile(user,mpass):
    genkey(user)
    data={mpass:{}}
    data_encryption(user,str(data))

def change_password(data,platform,username,new_pass):
    for i in data[platform]:
        for j in i:
            if j==username:
                i.update({username:new_pass})
                return data
    return data

def display_platforms(data):
    if data=={} or data==None:
        printc("[red]There is no saved data[/]")
        return 0,0
    else:    
        c=1
        d={}
        for i in data:
            printc(f"[yellow]{c}){i}[/]",end="  ")
            d[c]=i
            if c%3==0:
                print()
            c+=1
        printc(f"[red]{c})Back to Menu[/]\n")
        return d,c

def display_usernames(data,platform):
    if data=={} or data==None or data[platform]==[]:
        printc("[red]There is no saved data[/]")
        return 0,0
    else:    
        c=1
        d={}
        for i in data[platform]:
            for j in i:
                printc(f"[yellow]{c}){j}[/]",end="  ")
                d[c]=j
                if c%3==0:
                    print()
                c+=1
        printc(f"[red]{c})Back to Menu[/]\n")
        return d,c

def displayall(fdata,mp):
    if fdata[mp]=={} or fdata[mp]==None:
        printc("[red]There are no saved passwords[/]")
    else:
        for i in fdata[mp]:
            for j in fdata[mp][i]:
                printc(f'[yellow]{i}[/] :  ',end=" ")
                for k in j:
                    printc(f'Username --> [cyan]{k}[/]',f'|| Password--> [green]{j[k]}[/]')

def remove_username(data,platform,all=False,username=None):
    if all==True:
        try:
            del data[platform]
            return data
        except KeyError:
            printc("[red]!Entered Platform is not found![/]")
            time.sleep(1)
            return data
    else:
        try:
            for i in data[platform]:
                for j in i:
                    if j==username:
                        data[platform].remove(i)
                        return data
        except KeyError or IndexError or ValueError:
            printc("[red]!Entered Username is not found![/]")
            return data

def sp_platform(data,mp,platform):
    try:
        printc(f"[yellow]{platform} :[/]\n")
        for i in data[mp][platform]:
            for j in i:
                printc(f'Username --> [cyan]{j}[/]',f'|| Password-->,[green]{i[j]}[/]')
    except KeyError or IndexError:
        printc("[red]There is no saved data[/]")

#--------------------------VERIFICATION PROCESS----------------------#
def ver_encryption(profile,data):
    global file_path
    fpath=os.path.join(file_path,f"{profile}.key")
    with open(fpath,"rb") as f: 
        key=f.read()
    k=Fernet(key) #Assigning to a variable
    fpath=os.path.join(file_path,f"{profile}.ver")
    #Writing Encrpyted data into a pass(random extension made by me) file
    with open(fpath,"w") as f:
        f.write(data)
    with open(fpath,"rb") as og:
        og_data=og.read()
    en_data=k.encrypt(og_data)
    with open(fpath,"wb") as en:
        en.write(en_data)

def ver_decryption(profile):
    global file_path
    fpath=os.path.join(file_path,f"{profile}.key")
    with open(fpath,"rb") as f: #Extracting Key from the file to decrypt
        key=f.read()
    k=Fernet(key)
    #Retrieving Data from the file and Decrypt
    fpath=os.path.join(file_path,f"{profile}.ver")
    with open(fpath,"rb") as en:
        en_data=en.read()
    de_data=k.decrypt(en_data)
    return de_data.decode('ascii')

def verification(profile):
    global file_path
    while True:
        console.print("~~ SECURITY QUESTION ~~ \n",style="bold underline red")
        printc("[cyan]Select any one of the question:[/]")
        printc("[yellow]1.What was your first job designation?\n2.What was the first concert you attended?\n3.What is the name of your best childhood friend?\n4.What is your favorite book/series/movie/band?\n5.What is the name of your favorite teacher?[/]")
        printc("[yellow]6.Create your own custom question\n7.Exit this menu[/]")
        vch=int(input("Enter your choice: "))
        if vch==1:
            ans=input("Your answer or back: ")
            if str.lower(ans) not in ['back','b','exit','e']:
                data={"What was your first job designation?":ans}
                ver_encryption(profile,str(data))
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
        if vch==2:
            ans=input("Your answer or back: ")
            if str.lower(ans) not in ['back','b','exit','e']:
                data={"What was the first concert you attended?":ans}
                ver_encryption(profile,str(data))
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
        if vch==3:
            ans=input("Your answer or back: ")
            if str.lower(ans) not in ['back','b','exit','e']:
                data={"What is the name of your best childhood friend?":ans}
                ver_encryption(profile,str(data))
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
        if vch==4:
            ans=input("Your answer or back: ")
            if str.lower(ans) not in ['back','b','exit','e']:
                data={"What is your favorite book/series/movie/band?":ans}
                ver_encryption(profile,str(data))
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
        if vch==5:
            ans=input("Your answer or back: ")
            if str.lower(ans) not in ['back','b','exit','e']:
                data={"What is the name of your favorite teacher?":ans}
                ver_encryption(profile,str(data))
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
        if vch==6:
            que=input("Your Question or back: ")
            if str.lower(que) in ['back','b','exit','e']:
                os.system('cls' if os.name == 'nt' else 'clear')
            else:    
                ans=input("Your answer or back: ")
                if str.lower(ans) in ['back','b','exit','e']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    if que[-1]!='?': que=que+'?'
                    data={que.capitalize():ans}
                    ver_encryption(profile,str(data))
                    break
        if vch==7:
            os.system('cls' if os.name == 'nt' else 'clear')
            return False

#----------------------------USER INPUT-----------------------------#
console=Console()
console.print("\n~~ PASSMAN SIGN UP ~~\n",style="bold underline blue")
userchoice=input("New To PASSMAN?(y/n): ")
flag=0
while True:
    if str.lower(userchoice) not in ["yes",'y','true']:
        while True:
            os.system('cls' if os.name=='nt' else 'clear')
            console.print("\n~~ PASSMAN LOGIN ~~\n",style='bold underline blue')
            user_profile=input("Enter your Profile username: ")
            mpass=pwinput("\nEnter your Master password\n(enter 'back' to change username): ")
            os.system('cls' if os.name == 'nt' else 'clear')
            if str.lower(mpass) not in ['back','b','exit']:
                break
        while True:
            try:
                path=os.getcwd()
                file_path=os.path.join(path,f'PASSMAN/Users/{user_profile}')
                fdata=data_decryption(user_profile)
                dicdata=ast.literal_eval(fdata)
                mp=list(dicdata.keys())
                if mpass==mp[0]:
                    if flag==0:
                        printc("[green]WELCOME![/]")
                        printc("[blue]Loading...[/]")
                        flag=1
                        time.sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                    printc('\n[bold cyan]~ MAINMENU ~[/]\n')
                    printc("\n[yellow]1)Create a new username\n2)Change a username's password\n3)Change your Master Password\n4)Show all passwords\n5)Show particular website passwords\n6)Remove a Username\n7)Remove a Platform[/]")
                    printc('[yellow]8)Generate a Password for you\n9)Change Security Question\n10)Delete your User Account\n11)Log out[/]')
                    choice=input("\nEnter your Option Number: ")
                    try:
                        if int(choice)==1:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("ADDING A USERNAME: \n",style="bold underline blue")
                            dicdata[mpass]=new_username(dicdata[mpass])
                            data_encryption(user_profile,str(dicdata))
                            time.sleep(2)
                            os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==2:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("CHANGING PASSWORD: \n",style="bold underline red")
                            pd,pc=display_platforms(dicdata[mpass])
                            if pd!=0 and pc!=0:
                                pch=int(input("Enter your choice: "))
                                if pch==pc:
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                else:
                                    while True:
                                        if pch<pc:
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                            printc(f"[cyan]{pd[pch]}:\n[/]")
                                            ud,uc=display_usernames(dicdata[mpass],pd[pch])
                                            if uc!=0 and ud!=0:
                                                uch=int(input("Enter your choice: "))
                                                while True:
                                                    if uch<uc:
                                                        os.system('cls' if os.name == 'nt' else 'clear')
                                                        new_pass=input(f"Enter your new password for {ud[uch]}: ")
                                                        dicdata[mpass]=change_password(dicdata[mpass],pd[pch],ud[uch],new_pass)
                                                        data_encryption(user_profile,str(dicdata))
                                                        os.system('cls' if os.name == 'nt' else 'clear')
                                                        printc("[green]Your changes have been saved![/]")
                                                        break
                                                    elif uch==uc:
                                                        os.system('cls' if os.name == 'nt' else 'clear')
                                                        break
                                                    else:
                                                        printc("[red]Invalid Choice.[/]")
                                                        uch=input("Re-enter your choice or Back: ")
                                                        if str.lower(uch) in ['exit','e','back','b']: 
                                                            os.system('cls' if os.name == 'nt' else 'clear')
                                                            break
                                                        else: uch=int(uch)
                                            else:
                                                temp=input("Press enter to continue.")
                                                os.system('cls' if os.name == 'nt' else 'clear')
                                            break
                                        else:
                                            printc("[red]Invalid choice.[/]")
                                            pch=input("Re-enter your choice or Back: ")
                                            if str.lower(pch) in ['exit','e','b','back']:
                                                os.system('cls' if os.name == 'nt' else 'clear')
                                                break
                                            else: pch=int(pch)
                            else:
                                temp=input("Press enter to continue.")
                                os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==3:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("CHANGING MASTER PASSWORD: \n",style="bold underline red")
                            new_mpass=pwinput("Enter your new Master password\n(type 'back' to return menu): ")
                            if str.lower(new_mpass) not in ['back','b','exit','e']:
                                dicdata=change_mpass(dicdata,mpass,new_mpass)
                                data_encryption(user_profile,str(dicdata))
                                os.system('cls' if os.name == 'nt' else 'clear')
                                printc("[green]Your Master password has been changed![/]")
                                time.sleep(2)
                                while True:
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    printc("[red]!You have been logged out Please Re-login![/]\n")
                                    console.print("\n~~ PASSMAN LOGIN ~~\n",style='bold underline blue')
                                    user_profile=input("Enter your Profile username: ")
                                    mpass=pwinput("\nEnter your Master password\n(enter 'back' to change username): ")
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    if str.lower(mpass) not in ['back','b','exit']:
                                        break
                                flag=0
                            else:
                                os.system('cls' if os.name == 'nt' else 'clear')                               
                        elif int(choice)==4:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("PASSWORDS: \n",style="bold underline green")
                            displayall(dicdata,mpass)
                            jch=input("\nPress enter to continue.")
                            os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==5:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("PASSWORDS: \n",style="bold underline green")
                            pd,pc=display_platforms(dicdata[mpass])
                            if pd!=0 and pd!=0:
                                while True:
                                    pch=input("\nEnter your choice number: ")
                                    if str.lower(pch) in ['exit','e','back','b']: 
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    if int(pch)==pc:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    elif int(pch)<pc:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        sp_platform(dicdata,mpass,pd[int(pch)])
                                        jch=input("\nPress enter to continue.")
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    else:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        console.print("PASSWORDS: \n",style="bold underline green")
                                        display_platforms(dicdata[mpass])
                                        printc("\n[red]Invalid Choice.[/]\n[cyan]Re-enter your choice or Back[/]")
                            else:
                                temp=input("Press enter to continue.")
                                os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==6:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("REMOVING A USERNAME: \n",style="bold underline red")
                            pd,pc=display_platforms(dicdata[mpass])
                            if pd!=0 and pc!=0:
                                while True:
                                    pch=input("Enter your choice: ")
                                    if str.lower(pch) in ['exit','e','b','back']:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    if int(pch)==pc:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break 
                                    if int(pch)<pc:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        printc(f"[cyan]{pd[int(pch)]}:\n[/]")
                                        ud,uc=display_usernames(dicdata[mpass],pd[int(pch)])
                                        if uc!=0 and ud!=0:
                                            while True:
                                                uch=input("Enter your choice: ")
                                                if str.lower(uch) in ['exit','e','back','b']: 
                                                    os.system('cls' if os.name == 'nt' else 'clear')
                                                    break
                                                if int(uch)==uc:
                                                    os.system('cls' if os.name == 'nt' else 'clear')
                                                    break
                                                elif int(uch)<uc:
                                                    dicdata[mpass]=remove_username(dicdata[mpass],pd[int(pch)],False,ud[int(uch)])
                                                    data_encryption(user_profile,str(dicdata))
                                                    os.system('cls' if os.name == 'nt' else 'clear')
                                                    printc("[green]Your changes have been saved![/]")
                                                    break
                                                else:
                                                    os.system('cls' if os.name == 'nt' else 'clear')
                                                    console.print("PASSWORDS: \n",style="bold underline green")
                                                    display_usernames(dicdata[mpass],pd[int(pch)])
                                                    printc("\n[red]Invalid Choice.[/]\n[cyan]Re-enter your choice or Back[/]")
                                        else:
                                            temp=input("Press enter to continue.")
                                            os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    else:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        console.print("PASSWORDS: \n",style="bold underline green")
                                        display_platforms(dicdata[mpass])
                                        printc("\n[red]Invalid Choice.[/]\n[cyan]Re-enter your choice or Back[/]")
                            else:
                                temp=input("Press enter to continue.")
                                os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==7:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("REMOVING A PLATFORM: \n",style="bold underline red")
                            d,c=display_platforms(dicdata[mpass])
                            if d!=0 and c!=0:
                                while True:
                                    ch=input("Enter your choice: ")
                                    if str.lower(ch) in ['exit','e','back','b']:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        break
                                    if int(ch)==c:
                                        os.system('cls' if os.name == 'nt' else 'clear') 
                                        break   
                                    elif int(ch)<c:
                                        dicdata[mpass]=remove_username(dicdata[mpass],d[int(ch)],True)
                                        data_encryption(user_profile,str(dicdata))
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        printc("[green]Your changes have been saved![/]")
                                        break
                                    else:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        console.print("PASSWORDS: \n",style="bold underline green")
                                        display_platforms(dicdata[mpass])
                                        printc("\n[red]Invalid Choice.[/]\n[cyan]Re-enter your choice or Back[/]")
                            else:
                                temp=input("Press enter to continue.")
                                os.system('cls' if os.name == 'nt' else 'clear')
                        elif int(choice)==8:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            console.print("PASSWORD GENERATOR: \n",style="bold underline blue")
                            promptpass=input("Enter your key password to suggest a new password or press enter: ")
                            if promptpass==None or promptpass=='':    
                                while True:
                                    try:
                                        plen=int(input("Number of Characters: "))
                                        num=input("Do you want numbers included?(y/n): ")
                                        spc=input("Do you want Special charcters included?(y/n): ")
                                        while True:
                                            if num not in ['yes','y'] and spc not in ['yes','y']:
                                                printc(f"[bold cyan]Suggested Password --> [/][bold green]{pass_generator(plen,False,False)}[/]")
                                            elif num not in ['yes','y'] and spc in ['yes','y']:
                                                printc(f"[bold cyan]Suggested Password --> [/][bold green]{pass_generator(plen,False,True)}[/]")
                                            elif num in ['yes','y'] and spc not in ['yes','y']:
                                                printc(f"[bold cyan]Suggested Password --> [/][bold green]{pass_generator(plen,True,False)}[/]")
                                            else : printc(f"[bold cyan]Suggested Password --> [/][bold green]{pass_generator(plen,True,True)}[/]")
                                            gc=input("\nGenerate another?(y/n): ")
                                            os.system('cls' if os.name=='nt' else 'clear')
                                            if str.lower(gc) not in ['yes','y']:
                                                break
                                        break
                                    except ValueError:
                                        os.system('cls' if os.name=='nt' else 'clear')
                                        console.print("PASSWORD GENERATOR: \n",style="bold underline blue")
                                        printc("\n[red]Enter a Number![/]\n")
                            else:
                                while True:
                                    printc(f"[bold cyan]Suggested Password --> [/][bold green]{sp_pass_generator(promptpass)}[/]")
                                    t1=input("\nGenerate another?(y/n): ")
                                    os.system('cls' if os.name=='nt' else 'clear')
                                    if str.lower(t1) not in ['yes','y']:
                                        break
                        elif int(choice)==9:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            verification(user_profile)
                            printc("[green]Your Changes have been saved![/]")
                            time.sleep(2)
                            os.system('cls' if os.name=='nt' else 'clear')
                        elif int(choice)==10:
                            printc("[red]!After this you won't be able to RECOVER your DATA anymore![/]\n")
                            printc("[blue]Do you really want to delete your account?(y/n)[/]")
                            rch=input()
                            if rch in ['yes','y','true']:
                                shutil.rmtree(file_path)
                                os.system('cls' if os.name=='nt'else 'clear')
                                printc("[red]!USER ACCOUNT DELETED![/]")
                                temp=input("Do you want create a new User account(enter 'y')\nOr Login into existing User account(enter 'n')\nOr Exit(press Enter): ")
                                if str.lower(temp) in ['y','yes','new']:
                                    userchoice='y'
                                    break
                                elif str.lower(temp) in ['no','n','old','existing']:
                                    os.system('cls' if os.name=='nt'else 'clear')
                                    console.print("\n~~ PASSMAN LOGIN ~~\n",style='bold underline blue')
                                    user_profile=input("Enter your Profile username: ")
                                    mpass=pwinput("Enter your Master password: ")
                            else:
                                printc('[green]No Changes were made.[/]')
                                time.sleep(2)
                                os.system('cls' if os.name=='nt'else 'clear')
                        elif int(choice)==11 or str.lower(choice) in ['exit','e','logout','log out']:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            printc("[bold cyan]Logged Out![/]")
                            time.sleep(1)
                            break
                        elif int(choice)>11 or int(choice)<1:
                            printc("[red]Invalid Choice.[/]")
                            time.sleep(1)
                            os.system('cls' if os.name == 'nt' else 'clear')
                    except ValueError:
                        printc("[red]Invalid Choice.[/]")
                        time.sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                else: 
                    printc("[red]Wrong Password![/]\n")
                    mch=input("Forgot your password?(y/n): ")
                    os.system('cls' if os.name=='nt' else 'clear')
                    if str.lower(mch) in ['yes','y','forgot','true']:
                        printc("[cyan]Answer the following question to verify your identity.[/]")
                        ver_data=ast.literal_eval(ver_decryption(user_profile))
                        que=list(ver_data.keys())
                        ans=ver_data[que[0]]
                        uans=input(f"{que[0]}: ")
                        while True:
                            if str.lower(uans)==str.lower(ans):
                                fdata=data_decryption(user_profile)
                                dicdata=ast.literal_eval(fdata)
                                mp=list(dicdata.keys())
                                printc("[green]Verification Success![/]\n")
                                time.sleep(1)
                                os.system('cls' if os.name == 'nt' else 'clear')
                                mpass=mp[0]
                                new_mpass=pwinput("Enter your new Master password: ")
                                dicdata=change_mpass(dicdata,mp[0],new_mpass)
                                data_encryption(user_profile,str(dicdata))
                                printc("[green]Changes have been saved![/]")
                                time.sleep(2)
                                os.system('cls' if os.name=='nt' else 'clear')
                                break
                            else:
                                os.system('cls' if os.name=='nt' else 'clear')
                                printc("[red]Wrong answer! Retry.(type 'exit' to Exit)[/]")
                                time.sleep(1)
                                uans=input(f"{que[0]}: ")
                                if str.lower(uans) in ['exit','e','back','b']:
                                    os.system('cls' if os.name=='nt' else 'clear')
                                    break
                        printc("[cyan]Re-login to access your account[/]")
                        console.print("\n~PASSMAN LOGIN~\n",style='bold underline blue')
                        user_profile=input("Enter your Profile username: ")
                        mpass=pwinput("Enter your Master password: ",'*')
                        os.system('cls' if os.name=='nt' else 'clear') 
                    else:
                        printc("[cyan]Re-enter your Master password [/](or) [red]Type 'exit' to Quit.[/]")
                        f=0
                        while True:
                            console.print("\n~~ PASSMAN LOGIN ~~\n",style='bold underline blue')
                            if f==0:
                                print(f"Enter your Profile username: {user_profile}")
                                f=1
                            else: user_profile=input("Enter your Profile username: ")
                            mpass=pwinput("\nEnter your Master password\n(enter 'back' to change username): ")
                            os.system('cls' if os.name == 'nt' else 'clear')
                            if str.lower(mpass) not in ['back','b']:
                                break
                        if str.lower(mpass)=="exit" or str.lower(mpass)=='e': 
                            printc("[bold cyan]Closing the Program![/]")
                            time.sleep(1)
                            break
            except FileNotFoundError: 
                os.system('cls' if os.name == 'nt' else 'clear')
                printc("[red]Entered User Account is not found.[/]\n")
                printc("[green]Re-Enter Details? (press enter) (or)[/]")
                printc("[blue]Create a new User Profile? (type 'back' or 'b')[/] (or)")
                printc("[yellow]Exit?(type 'exit')[/]")
                c=input('Your choice?: ')
                if str.lower(c) in ['exit','e']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                if str.lower(c) in ['b','back']:
                    userchoice='y'
                    break
                else:
                    while True:
                        os.system('cls' if os.name=='nt' else 'clear')
                        console.print("\n~~ PASSMAN LOGIN ~~\n",style='bold underline blue')
                        user_profile=input("Enter your Account Username: ")
                        mpass=pwinput("\nEnter your Master password\n(enter 'back' to change username): ")
                        os.system('cls' if os.name == 'nt' else 'clear')
                        if str.lower(mpass) not in ['back','b','exit']:
                            break
        if userchoice!='y':
            break
    else :
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            console.print("\n~~ PASSMAN SIGN UP ~~\n",style="bold underline blue")
            console.print("\nEnter your New profile details\n",style="bold cyan underline")
            user_profile=input("Enter your Profile username: ")
            mpass=pwinput("\nEnter your Master password\n(enter 'back' to change username): ")
            if str.lower(mpass) not in ['back','b','exit']:
                break
        try:
            path=os.getcwd()
            file_path=os.path.join(path,f'PASSMAN/Users/{user_profile}')
            os.system('cls' if os.name == 'nt' else 'clear')
            os.makedirs(file_path)
            new_profile(user_profile,mpass)
            v=verification(user_profile)
            if v!=False: 
                printc("[green]User Account has been created![/]")
                time.sleep(2)
                userchoice='n'
                os.system('cls' if os.name== 'nt' else 'clear')
                printc("[green]Please Re-Login to access your account.[/]\n")
            else:
                shutil.rmtree(file_path)
                printc("[red]!User Account Sign up Failed![/]")
                t=input("Return to Sign Up page?(y/n): ")
                if str.lower(t) not in ['y','yes','true']:
                    os.system('cls' if os.name== 'nt' else 'clear')
                    printc("[bold cyan]Logged Out![/]")
                    time.sleep(1)
                    break
        except FileExistsError:
            printc("[red]User Account already exists.[/]")
            t=input("Return to Sign Up page?(y/n): ")
            if str.lower(t) not in ['y','yes','true']:
                os.system('cls' if os.name== 'nt' else 'clear')
                printc("[bold cyan]Logged Out![/]")
                time.sleep(1)
                break