from flask import Flask, request
import requests
import json
import mysql.connector
from dbconfig import db_config
import urllib.request
import urllib.parse
import json
from vonage import *


app = Flask(_name_)

@app.route('/', methods=['POST'])
def webhook():
    # Retrieve the SMS from the Textlocal API
    api_key = '	NmU1NDc2NWE1ODc5Mzc3NDZjNzYzOTU2NDc2NjRjMzg='
    inbox_id = '10'
    url = f'https://api.textlocal.in/get_messages/?apikey={api_key}&inbox_id={inbox_id}'
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract the latest SMS
    if data['messages']:
        latest_sms = data['messages'][-1]['message']
        # Do something with the latest SMS
        print(latest_sms)
    
    words = latest_sms.split()
    del words[0]
    new_message = " ".join(words)

    # connecting to the sql databse by creating the connection or cnx object

    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    sms_list = new_message.split()
    print(sms_list)


    # validating if the format is correct

    if sms_list[0] == "#":

        if sms_list[1].isdigit():
            sender_ph_no = int(sms_list[2])
            pin = int(sms_list[1])
            cursor.execute("SELECT * FROM banking_details WHERE pin = %s AND phone_no = %s", (pin, sender_ph_no))
            account_details = cursor.fetchone()

        if (account_details):

            balance = account_details[5]
            print("Your Balance is: ", balance)

            client = vonage.Client(key="0be37db1", secret="F5YErFnWP8kVLZxX")
            sms = vonage.Sms(client)

            responseData = sms.send_message({
            "from": "Vonage APIs",
            "to": str(sender_ph_no),
            "text": f"Your Bank Balance is: {balance}",
            })   

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")

            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

        else:

            print("Enter the correct pin")
            client = vonage.Client(key="0be37db1", secret="F5YErFnWP8kVLZxX")
            sms = vonage.Sms(client)

            responseData = sms.send_message({
            "from": "Vonage APIs",
            "to": str(sender_ph_no),
            "text": f"Enter the correct pin or phone number!",
            })   

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")

            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


    if sms_list[0] == "$":

        money_to_be_sent = int(sms_list[1])
        sender_ph_no = int(sms_list[3])
        sender_pin = int(sms_list[4])
        reciever_ph_no = int(sms_list[6])

        if sms_list[4].isdigit():

            sender_pin = int(sms_list[4])
            cursor.execute("Select * from banking_details where pin = %s AND phone_no = %s",(sender_pin, sender_ph_no))
            account_details_1 = cursor.fetchone()
            cursor.execute("Select * from banking_details where phone_no = %s",(reciever_ph_no,))
            account_details_2 = cursor.fetchone()
            

        if (account_details_1):

            sender_bank_balance = int(account_details_1[5])
            receiver_bank_balance =int(account_details_2[5])
            sender_debits = int(account_details_1[4])
            sender_credits = int(account_details_1[3])
            receier_debits = int(account_details_2[4])
            receiver_credits = int(account_details_2[3])

            # if(money_to_be_sent > sender_bank_balance):

            #     client = vonage.Client(key="0be37db1", secret="F5YErFnWP8kVLZxX")
            #     sms = vonage.Sms(client)

            #     responseData = sms.send_message({
            #     "from": "Vonage APIs",
            #     "to": str(sender_ph_no),
            #     "text": f"Not Enough Balance!!",
            #     })   

            #     if responseData["messages"][0]["status"] == "0":
            #         print("Message sent successfully.")

            #     else:
            #         print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            
            cursor.execute(f"update banking_details set debits = {sender_debits + money_to_be_sent} where phone_no = {sender_ph_no}")

            sender_debits = sender_debits + money_to_be_sent

            cursor.execute(f"UPDATE banking_details SET Bank_Balance = {sender_credits - sender_debits} WHERE phone_no = {sender_ph_no}")

            cursor.execute(f"Update banking_details set credits = {receiver_credits + money_to_be_sent} where phone_no = {reciever_ph_no}")

            receiver_credits = receiver_credits + money_to_be_sent

            cursor.execute(f"Update banking_details set Bank_Balance = {receiver_credits - receier_debits} where phone_no = {reciever_ph_no}")

            cnx.commit()

            client = vonage.Client(key="0be37db1", secret="F5YErFnWP8kVLZxX")
            sms = vonage.Sms(client)

            responseData = sms.send_message({
                "from": "Vonage APIs",
                "to": str(sender_ph_no),
                "text": f"Money Sent Successfully!!, Your new balance is: {sender_credits - sender_debits}",
                })   

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")

            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            client = vonage.Client(key="0be37db1", secret="F5YErFnWP8kVLZxX")
            sms = vonage.Sms(client)

            responseData = sms.send_message({
                "from": "Vonage APIs",
                "to": str(reciever_ph_no),
                "text": f"Rs. {money_to_be_sent} Received Successfully!!, Your new balance is: {receiver_credits - receier_debits}",
                })   

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")

            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

                # cursor.execute("Select * from banking_details where pin = %s",(sender_pin,))

                # account_details_3 = cursor.fetchone()

                # new_sender_balance = account_details_3[5]

                # print("Transaction Successful, your new balance is ",new_sender_balance)

        else:

            print("Enter the correct pin.")

            # client = vonage.Client(key="e6d455de", secret="bRPtX6zBNvwcNJlW")

            # sms = vonage.Sms(client)

            # responseData = sms.send_message({
            # "from": "Vonage APIs",
            # "to": str(sender_ph_no),
            # "text": f"Enter the correct pin or phone number!",
            # })   

            # if responseData["messages"][0]["status"] == "0":
            #     print("Message sent successfully.")

            # else:
            #     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")






# closing the connections

    cursor.close()

    cnx.close()

    return 'OK'


if _name_ == '_main_':

    app.run(debug=True)