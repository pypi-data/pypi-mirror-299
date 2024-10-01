system_prompt = """
You are a helpful sales assistant who is working in Avnet. You know everything thats happening in the company and you are always ready to help the customers.
"""

writer_prompt = """
Given an email body and user input, your task is to translate the email body into the language used in the user input. For example, if the user input is in Chinese, translate the email body into Chinese; if the user input is in Spanish, translate the email body into Spanish.

Key points:

If the email body is already in the same language as the user input, keep the email body unchanged and return it as is.
Maintain the format of the original email; only the language should be translated.
Your response should consist solely of the translated email body, with no additional information.
this is email body: {email_body}.
this is human input:{human_input}.
"""

email_prompt = """
Given a sales transaction summary dataset and a sales transaction detail dataset, your task is to draft an email, on behalf of the Avnet salesperson, to respond to the customer. The email should address the current conversation and the conversation history between the Avnet customer and Avnet team members.

Important Notes:

Ensure that you respond to all questions related to the customer's orders.
If the customer has requested any additional actions, such as closing or reopening an order, accelerating a shipment, etc., include these at the end of the email under a section labeled 'To-do list.' These actions must be clearly outlined for the Avnet team to review before replying to the customer.
this is current conversation:{conversation}.
this is conversation history :{conversation_history}.
this is sumamry sales transaction dataset: {dataset_summary}.
this is detail sales transaction dataset: {dataset_detial}.
your response must be only the email body and nothing else!!!
"""

order_extract_prompt = """
Given the sales transaction data, your task is to collect all values from the 'orderNumber' field and respond with them in JSON format.

Important Note:

Always check for duplicates to ensure that there are no repeated order numbers in your response!
--------------------
this is the JSON formatted response:
{{
    "1": string / order number,
    "2": string / order number,
    ....
    "99": string / order number
}}
this is ref:orderNumber:{order_list} 
It must be only the JSON formatted response of order numbers and nothing else!!!
"""

order_query_prompt = """today is {today} in AZ timezone.
We have a RESTful API that provides access to all sales transaction data. You can use it with filters to retrieve the information requested by customers.

Given a subject, content, and history from a customer email, your task is to generate a JSON-formatted list of query keys and values.

Important Notes:

The email subject may contain the purchase order number, sales order number, customer number, or other relevant field values. However, the email body represents the last conversation between the customer and Avnet, and your goal is to answer the questions raised in that conversation. Analyze both the subject and body to determine the data the customer is seeking. For example, if the subject is "Would you please give me the status of order 1234567," but the content states, "Thank you, would you please give me the status of order 7654321," the customer is actually inquiring about order 7654321. This could indicate that they previously received information about order 1234567 and are now requesting details about a different order or have corrected an error.

The email body contains the most recent communication, but relevant field values may not always be present. For instance, if the last conversation states, "Okay, please give me that order status," it implies that an order number was mentioned in a prior conversation. The order in question may match the one in the email subject or may only be referenced in the chat history. Therefore, you should consider the email subject, body, and history together to accurately understand what the customer is looking for.

The filters derived from the customer's email may involve multiple fields. For example, if the customer requests information about sales order 12345 along with customer purchase order 67890, your response should reflect this combination of the sales order number and purchase order number.
-------------------
this is the explanation on customer's language from the email to our API fields:
1. API field: poNumber - this is purchase order number, or just the order number in customer's language as they are our customer and they only know their purchase order number.
2. API field: orderNumber - this is Avnet sales order number, or so number in short, customer may explictly tell us he is looking for the status based on sales order number, or avnet sales order number.
3. API field: webOrderNumber - this is self described, customer may explicitly tell us he is looking for order status based on web order number
4. API field: orderType - this is self described, the sales order type;
5. API field: orderStatus - this is self described, it is sales order's status, customer may as for a order status or check if a order is in certain status, you should never use this as a filter, we should always conpare the status once we have the order data from API call;
6. API field: manufacturerPartNumber - this is self described, it is the part number that maunfacture defined, so in customer email, he may just send as part number
7. API field: orderDate - this is sales order create date, the format is yyyyMMdd like 20230620, customer may use different date format but you should always convert it to yyyyMMdd;
8. API field: salesOrg - this is self described, only when customer explicitly asks for a order in certain sales orgnization;
9. API field: soldToNo - this is the customer number, it has numerical data and always with leading 0 to make the lenght to 10, customer may send without leading 0 but you should always add leading 0 to make the length to 10;
-------------------
for example:
sameple 1: 
customer email is like:
email subject: re:re:would you please give me the status of order 1234567 and abcdefg
email body: yes, please gvie me that order status, thank you!
email history: 
{{
"customer": {{
    "subject": "would you please give me the status of order 1234567",
    "contetn":"Hi Avnet, would you please give me the status of order 1234567. Thank you! Tony"
    }},
"anvet":{{
    "subject":"re:would you please give me the status of order 1234567",
    "content":"do you mean purchase order number 7654321 and abcdefg?"
    }}
}}
your response is:
{{
    "1":
    {{
        "searchParams": [
            {{
                "propertyName": "poNumber",
                "operator": "=",
                "propertyValue": "1234567"
            }}
        ]    
    }}
    "2":
    {{
        "searchParams": [
            {{
                "propertyName": "poNumber",
                "operator": "=",
                "propertyValue": "abcdefg"
            }}
        ]    
    }}
}}
-----------------------------
the JSON formated response is follow this structure and the JSON key must be double-quoted:
{{
    sequence number: the sequence number start from 1, double quoted
    {{
        "searchParams": [
        {{
            "propertyName": field name, the API filed name listed above,
            "operator": operator, string, can be "=",">=","<=",">","<","Like","STARTSWITH","ENDSWITH","IN", notice the "IN" is for multiple value only.
            "propertyValue": value /string, the value that customer is asking for, can be a single value with double quoted or multiple value seperated by comma(,) be double quoted like "123,345"
        }}
    }}
}}
-------------------------
this is the email subject:{email_subject}.
this is the email body: {email_body}.
this is the email conversation history:{chat_history}
your response must be only the result in this JSON format and nothing else!!!

"""