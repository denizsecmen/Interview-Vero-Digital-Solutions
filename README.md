# Python Request-Excel Convert Project
In this project, the client component reads CSV data located in the same directory. It then sends this data to the server using the HTTP protocol. Upon receiving a response from the server, the client extracts settings provided by the server. Utilizing these settings, the client converts the received data into an Excel file. This Excel conversion process is tailored based on the settings transmitted by the server, ensuring the final output adheres to the specified configurations.
# Used Classes Inside Project 
## Client
### Handle Request
- transmit_to_server(read file from selected path and send this data to server).
### Excel Conventer
- adding_rows_excel(add rows to excel file which will be created).
- convert_to_excel(convert to rows to excel file and save it to computer).
## Server
### HandleRequest
- recieve_request(recieve request from client,call functions to other operations and reponse back to client).
- run(run the server).
### SendToUrl
- auth_for_target(get auth creadentials for request with request to auth page).
- send_to_target(get data from distant URL.).
### Editor
- make_distict(Loops all elements from request and make them distinct).
- filter(Filter all elements based on conditions).
# Used Libraries
- fastapi
- requests
- json
- openpyxl
- csv
- uvicorn
