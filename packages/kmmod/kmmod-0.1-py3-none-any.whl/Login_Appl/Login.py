def Loginerfunc(hold=0):
    """Code to Perform all the functions at once."""
    import login_holder
    import sys
    import time

    def login(Default_user="user",Default_password=0000):
        try:
            users=login_holder.user_list.keys()
            passc=login_holder.user_list.values()

            print("==================")
            print("Login".upper())
            userinput=str(input("Enter your username  ").lower())
            passinput=int(input("Enter your password "))
            if(userinput in users):
                if(passinput in passc):
                    print(f"👋 Welcome {userinput}!")
                    print("What would you like to do?")
                    print("1 : Sign up")
                    print("2 : See Profiles")
                    select=str(input(""))
                    if(select=="1"):
                        sign_up()
                    elif(select=="2"):
                        print("\n==================")
                        print(f"Profile Details : {login_holder.user_list}")
                        print("==================")
                        exit()
                    else:
                        print("\nwrong selection.")
                else:
                    print("\nInvalid password.")
            else:
                print("\nusername not found")
        except ValueError:
            print("\nLogin failed.\n(Default user and password :\n{user} {0000})\n")
            sys.exit()
    login()

    def sign_up():
        try:
            prompt=str(input("Who are you signing up for? "))
            much=int(input("How many people are you signing up? "))
            time.sleep(2)
            for signnum in range(0,much):
                print(f"Sign Up for {much} person.\n")
                print("=================")
                print("Sign Up\n")
                fname=str(input("Firstname ").lower())
                lname=str(input("Lastname ").lower())
                npass=input("Enter your New Password ")
                cpass=input("Confirm Password ")
                time.sleep(2)
                login_holder.user_list[fname]==cpass
                print("=================")
                print("\nAccount created successfully.".upper())
                print("Profile Details :")
                print(f"Firstname : {fname}")
                print(f"Lastname : {lname}")
                print(f"Your Username : {fname}")
                print(f"Password : {cpass}\n")
                print("=================")
        except ValueError:
            print("\nSign up failed.")
            sys.exit()

Loginerfunc()

