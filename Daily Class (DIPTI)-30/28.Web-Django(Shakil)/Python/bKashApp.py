while True:
    print("     Send Instraction")
    print("bkash")
    print("1 Send Money")
    print("2 Send Money to Non-Bkash")
    print("3 Mobile Research")
    print("4 Payment")
    print("5 Cash Out")
    print("6 Pay Bill")
    print("7 Microfinance")
    print("8 Download bKash App")
    print("9 My bKash")
    print("10 Reset PIN")

    value = int(input())

    if value == 1:
        print("     Send Instraction")
        print("Enter Reciver Bkash Account No:")
        bkashNumber = input()
        
        if bkashNumber:
            print("     Send Instraction")
            print("Enter Amount: ")
            Amount= int(input())
            
            if Amount:
                print("     Send Instraction")
                print("Send Money")
                print(f"To: {bkashNumber}")
                print(f"Amount: {Amount}")
                print("Enter Your PIN: ")
                PinNum= int(input())
                
                if PinNum:
                    print(f"Successfully send {Amount} BDT to {bkashNumber} this Number")
    elif value == 2:
        print("     Send Instraction")
        print("Enter Reciver Bkash Account No:")
        bkashNumber = input()
        
        if bkashNumber:
            print("     Send Instraction")
            print("Enter Amount: ")
            Amount= int(input())
            
            if Amount:
                print("     Send Instraction")
                print("Send Money to Non-Bkash")
                print(f"To: {bkashNumber}")
                print(f"Amount: {Amount}")
                print("Enter Your PIN: ")
                PinNum= int(input())
                
                if PinNum:
                    print(f"Successfully send {Amount} BDT to {bkashNumber} this Number")

    elif value == 3:
        print("     Send Instraction")
        print("1 Robi")
        print("2 Airtel")
        print("3 Banglalink")
        print("4 Grameenphone")
        print("5 Teletalk")
        print("6 Get instant cashback on bKash Recharge")
        print("0 Main Menu")
        choice= int(input())
        if choice == 1:
            print("     Send Instraction")
            print("Enter Robi Mobile No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Mobile Recharge")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        elif choice == 2:
            print("     Send Instraction")
            print("Enter Airtel Mobile No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Mobile Recharge")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        elif choice == 3:
            print("     Send Instraction")
            print("Enter Banglalink Mobile No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Mobile Recharge")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        elif choice == 4:
            print("     Send Instraction")
            print("Enter Grameenphone Mobile No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Mobile Recharge")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        elif choice == 5:
            print("     Send Instraction")
            print("Enter Teletalk Mobile No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Mobile Recharge")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        elif choice == 6:
            print("     Send Instraction")
            print("Recharge from bKash and get instant cashback on selected packs!")          
        elif choice == 0:
            continue
    elif value == 4:
        print("     Send Instraction")
        print("Enter Merchant bKash Account No:")
        mobileNo = input()
        
        if mobileNo:
            print("     Send Instraction")
            print("Enter Amount: ")
            Amount= int(input())
            
            if Amount:
                print("     Send Instraction")
                print("Payment")
                print(f"To: {mobileNo}")
                print(f"Amount: {Amount}")
                print("Enter Your PIN: ")
                PinNum= int(input())
                
                if PinNum:
                    print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
      
    elif value == 5:
        print("     Send Instraction")
        print("1 From Agent")
        print("2 Priyo Agent")
        print("3 Set up to 2 Priyo Agent Number ")
        print("0 Main Menu")
        choice= int(input())
        if choice == 1:
            print("     Send Instraction")
            print("Enter Agent No")
            mobileNo = input()
            
            if mobileNo:
                print("     Send Instraction")
                print("Enter Amount: ")
                Amount= int(input())
                
                if Amount:
                    print("     Send Instraction")
                    print("Cash Out")
                    print(f"To: {mobileNo}")
                    print(f"Amount: {Amount}")
                    print("Enter Your PIN: ")
                    PinNum= int(input())
                    
                    if PinNum:
                        print(f"Successfully send {Amount} BDT to {mobileNo} this Number")
        
        elif choice == 0:
            continue  
    elif value == 6:
        print("     Send Instraction")
        print("1 Electricity (Prepaid)")
        print("2 Electricity (Postpaid)")
        print("3 Gas")
        print("4 Water")
        print("5 Internet and Phone")
        print("6 TV")
        print("7 City Services")
        print("7 Education")
        print("8 Financial Services")
        print("0 Main Menu")
        
        choice= int(input())
        if choice == 1:
            print("     Electricity (Prepaid")
            print("1 Palli Bidyut")
            print("2 DESCO")
            print("3 DPDC")
            print("4 BPDB")
            print("5 Sylhet BPDB")
            print("6 WestZone")
            print("7 NESCO")
            print("0 Main Menu")
            
            choice2 = int(input())
            
            if choice2 == 1:
                while True:
                    print("     Palli Bidyut (Prepaid)")
                    print("1 Bill Breakdown")
                    print("2 Make Payment")
                    print("0 Main Menu")
                    
                    choice3 = int(input())
                    if choice3 == 1:
                        print("     Palli Bidyut Prepaid")
                        print("1 Input Meter")
                        print("2 Make Payment")
                        print("0 Main Menu")
                        
                        choice4 = int(input())
                        if choice4 == 1:
                            print("Enter Meter Number")
                            meterno = input()
                    
                            if meterno:
                                print("     Send Instraction")
                                print("Enter Amount: ")
                                Amount= int(input())
                                
                                if Amount:
                                    print("     Send Instraction")
                                    print("Pay Bill")
                                    print(f"To: {meterno}")
                                    print(f"Amount: {Amount}")
                                    print("Enter Your PIN: ")
                                    PinNum= int(input())
                                    
                                    if PinNum:
                                        print(f"Successfully pay {Amount} BDT to {meterno} this Meter Number")
                        
                        elif choice == 0:
                            break
            elif choice2 == 2:
                print("     DESCO (Prepaid)")
                print("1 Bill Breakdown")
                print("2 Make Payment")
                print("0 Main Menu")
                
                choice3 = int(input())
                if choice3 == 1:
                    print("     DESCO Prepaid")
                    print("1 Input Meter")
                    print("2 Make Payment")
                    print("0 Main Menu")
                    
                    choice4 = int(input())
                    if choice4 == 1:
                        print("Enter Meter Number")
                        meterno = input()
                
                        if meterno:
                            print("     Send Instraction")
                            print("Enter Amount: ")
                            Amount= int(input())
                            
                            if Amount:
                                print("     Send Instraction")
                                print("Pay Bill")
                                print(f"To: {meterno}")
                                print(f"Amount: {Amount}")
                                print("Enter Your PIN: ")
                                PinNum= int(input())
                                
                                if PinNum:
                                    print(f"Successfully pay {Amount} BDT to {meterno} this Meter Number")
            elif choice2 == 3:
                print("     DPDC (Prepaid)")
                print("1 Bill Breakdown")
                print("2 Make Payment")
                print("0 Main Menu")
                
                choice3 = int(input())
                if choice3 == 1:
                    print("     DPDC Prepaid")
                    print("1 Input Customer Number")
                    print("2 Saved Accounts")
                    print("0 Main Menu")
                    
                    choice4 = int(input())
                    if choice4 == 1:
                        print("Enter Meter Number")
                        meterno = input()
                
                        if meterno:
                            print("     Send Instraction")
                            print("Enter Amount: ")
                            Amount= int(input())
                            
                            if Amount:
                                print("     Send Instraction")
                                print("Pay Bill")
                                print(f"To: {meterno}")
                                print(f"Amount: {Amount}")
                                print("Enter Your PIN: ")
                                PinNum= int(input())
                                
                                if PinNum:
                                    print(f"Successfully pay {Amount} BDT to {meterno} this Meter Number")
            elif choice2 == 0:
                continue
        elif choice == 0:
            continue    