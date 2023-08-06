# Offline_banking_transaction
This project aims to provide a secure framework for conducting banking transactions via SMS, without the need for internet connectivity. The methodology for achieving this can be summarized as follows:
1) Database Setup
2) SMS Format: A specific SMS format is designed to ensure efficient parsing and interpretation by the application.
3) SMS API Integration: The project integrates two APIs to facilitate SMS communication. The Textlocal API is used to receive incoming SMS messages in the application's inbox. The Vonage API is utilized to send SMS notifications and responses to users.
4) SMS Processing
5) Transaction Execution

FLOWCHART ==>>
Start
|
|-----> Receive HTTP POST request to '/'
|
|-----> Retrieve latest SMS from Textlocal API
|       |
|       |-----> Extract message content
|       |
|       |-----> Split message into words
|
|-----> Check if first word is '#'
|       |
|       |-----> Extract sender's phone number and PIN
|       |
|       |-----> Connect to MySQL database
|       |
|       |-----> Retrieve account details based on phone number and PIN
|       |
|       |-----> If account details found,
|       |       |
|       |       |-----> Retrieve balance
|       |       |
|       |       |-----> Send balance as SMS using Vonage API
|       |
|       |-----> If account details not found,
|       |       |
|       |       |-----> Send error message to sender
|
|-----> Check if first word is '$'
|       |
|       |-----> Extract amount, sender's phone number, sender's PIN, and receiver's phone number
|       |
|       |-----> Connect to MySQL database
|       |
|       |-----> Retrieve account details of sender and receiver based on phone numbers
|       |
|       |-----> If sender's account details found,
|       |       |
|       |       |-----> Update debit and balance values in the database
|       |
|       |-----> If receiver's account details found,
|       |       |
|       |       |-----> Update credit and balance values in the database
|       |
|       |-----> Send success messages to sender and receiver with updated balances
|       |
|       |-----> If any account details not found,
|       |       |
|       |       |-----> Send error message to sender
|
|-----> Close database connection
|
|-----> Return HTTP response with status "OK"
|
End
