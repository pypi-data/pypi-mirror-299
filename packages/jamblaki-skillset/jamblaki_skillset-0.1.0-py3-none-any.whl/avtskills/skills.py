import asyncio,aiohttp,json,os
import datetime
from pytz import timezone
import openai
from openai import AzureOpenAI,AsyncAzureOpenAI
from ._sales_prompt import order_query_prompt,system_prompt
from ._skill_utils import aorder_status_body_call,abk_api_call


class sales_retrieval_skill():
    def __init__(self,req_url,req_body,apim_key):
        self.req_url = req_url,
        self.req_body = req_body,
        self.apim_key = apim_key

    async def sales_retrieval_tool_ins(self):
        pass

    async def sales_retrieval_tool(req_url:str,req_body:str,apim_key:str):
        pass




# security checking skill class - include instance method and statistic method
class security_checking_skill():
    def __init__(self,email_address:str):
        self.security_req_url = os.environ.get("SECURITY_REQ_URL")
        self._security_req_body_dict = {
             "ContactEmail": email_address
        }
        self.security_req_body = json.dumps(self._security_req_body_dict)
        self.security_apim_key = os.environ.get("SECURITY_APIM_KEY")
    
    async def security_checking_tool_ins(self):
        url = self.security_req_url
        body_data = self.security_req_body
        api_key = self.security_apim_key
        headers = {'Content-Type': 'application/json',
                    'Ocp-Apim-Subscription-Key': api_key,
                    'Accept': '*/*'
                    }       
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url,data=body_data,headers=headers) as resp:
                    customer_data = await resp.text()
            return customer_data
        except Exception as e:
            return e


    async def security_checking_tool(email_address:str):
        req_body_dict = {
        "ContactEmail": email_address
        }
        security_req_body = json.dumps(req_body_dict)
        
        url = os.environ.get("SECURITY_REQ_URL")
        body_data = security_req_body
        api_key = os.environ.get("SECURITY_APIM_KEY")
        headers = {'Content-Type': 'application/json',
                    'Ocp-Apim-Subscription-Key': api_key,
                    'Accept': '*/*'
                    }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url,data=body_data,headers=headers) as resp:
                    customer_data = await resp.text()
            return customer_data
        except Exception as e:
            return e



# security checking skill function , return result
async def security_checking_tool(email_address:str):
    security_req_url = os.environ.get("SECURITY_REQ_URL")
    security_apim_key = os.environ.get("SECURITY_APIM_KEY")
    req_body_dict = {
        "ContactEmail": email_address
    }
    security_req_body = json.dumps(req_body_dict)
    url = security_req_url
    body_data = security_req_body
    api_key = security_apim_key
    headers = {'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': api_key,
                'Accept': '*/*'
                }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url,data=body_data,headers=headers) as resp:
                customer_data = await resp.text()
        return customer_data
    except Exception as e:
        return e

# security checking skill package function , return function
def security_checking_call(email_address:str):
    async def asecurity_checking_tool(email_address:str):
        security_req_url = os.environ.get("SECURITY_REQ_URL")
        security_apim_key = os.environ.get("SECURITY_APIM_KEY")
        req_body_dict = {
            "ContactEmail": email_address
        }
        security_req_body = json.dumps(req_body_dict)
        url = security_req_url
        body_data = security_req_body
        api_key = security_apim_key
        headers = {'Content-Type': 'application/json',
                    'Ocp-Apim-Subscription-Key': api_key,
                    'Accept': '*/*'
                    }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url,data=body_data,headers=headers) as resp:
                    customer_data = await resp.text()
            return customer_data
        except Exception as e:
            return e
    return asecurity_checking_tool




async def asales_retrieval_tool(email_subject:str,email_body:str,email_history:str):

        # 1. sales order query filter selection and body generation
        order_status_body = await aorder_status_body_call(email_subject,email_body,email_history)
        print("-----order_status_body------")
        print(order_status_body)
        print("-----end  ------")
        
        # 2. calling sales API in concurrently
        try:
            tasks = []
            order_status_dict = json.loads(order_status_body)
            for key,value in order_status_dict.items():
                print("-----value- -----")
                print(value)
                value_json_str = json.dumps(value)
                print("----------------")
                print(value_json_str)
                print("-----end ------")
                tasks.append(abk_api_call(value_json_str))
            abk_api_ls = await asyncio.gather(*tasks)
            print("-----sales data ------")
            print(abk_api_ls)
            print("-----end ------")
        except Exception as e:
            print("error is : ", e)
            abk_api_ls = "there is no such data"+e

        return abk_api_ls

# retrieval skill function - return function
def asales_retrieval_call(email_subject:str,email_body:str,email_history:str):
    async def sales_retrieval_tool(email_subject:str,email_body:str,email_history:str):

        # 1. sales order query filter selection and body generation
        order_status_body = await aorder_status_body_call(email_subject,email_body,email_history)
        # 2. calling sales API in concurrently
        try:
            resp_dict = dict()
            n = 1
            tasks = []
            order_status_dict = json.loads(order_status_body)
            for key,value in order_status_dict.items():
                value_json_str = json.dumps(value)
                tasks.append(abk_api_call(value_json_str))
            abk_api_ls = await asyncio.gather(*tasks)
                
            for resp in range(len(abk_api_ls)):
                resp_json = json.loads(abk_api_ls[resp])
                for index in range(len(resp_json["data"])):
                    orderNumber = resp_json["data"][index]["orderNumber"]
                    item_number = resp_json["data"][index]["itemNo"]
                    try:      
                        endCustomer = resp_json["data"][index]["endCustomer"]["no"]
                    except Exception as e:
                        endCustomer = ""
                    try:
                        soldTo = resp_json["data"][index]["soldTo"]["no"]
                    except Exception as e:
                        soldTo = ""
                    soldToName = resp_json["data"][index]["soldTo"]["name"]
                    customerPartNumber = resp_json["data"][index]["customerPartNumber"]
                    poNumber = resp_json["data"][index]["poNumber"]
                    webOrderNumber = resp_json["data"][index]["webOrderNumber"]
                    quantity = resp_json["data"][index]["quantity"]
                    totalShippedQty = resp_json["data"][index]["totalShippedQty"]
                    totalRemainingQty = resp_json["data"][index]["totalRemainingQty"]
                    totalConfirmQty = resp_json["data"][index]["totalConfirmQty"]
                    totalDeliveredQty = resp_json["data"][index]["totalDeliveredQty"]
                    totalRequirementQty = resp_json["data"][index]["totalRequirementQty"]
                    shippedDate = resp_json["data"][index]["shippedDate"]
                    deliveryDate = resp_json["data"][index]["deliveryDate"]
                    scheduleDate = resp_json["data"][index]["scheduleDate"]
                    orderStatus = resp_json["data"][index]["orderStatus"]
                    resp_dict[str(n)] = {
                        "orderNumber" : orderNumber,
                        "item_number" : item_number,
                        "endCustomer" : endCustomer,
                        "soldTo" : soldTo,
                        "soldToName": soldToName,
                        "customerPartNumber" : customerPartNumber,
                        "poNumber" : poNumber,
                        "webOrderNumber" : webOrderNumber,
                        "quantity" : quantity,
                        "totalShippedQty" : totalShippedQty,
                        "totalRemainingQty" : totalRemainingQty,
                        "totalConfirmQty" : totalConfirmQty,
                        "totalDeliveredQty" : totalDeliveredQty,
                        "totalRequirementQty" : totalRequirementQty,
                        "shippedDate" : shippedDate,
                        "deliveryDate" : deliveryDate,
                        "scheduleDate" : scheduleDate,
                        "orderStatus" : orderStatus                
                    }
                    print(resp_dict)
                    n = n+1
            return resp_dict
        except Exception as e:
            print("xx error is : ", e)
            resp_dict = "there is no such data"+e
            return resp_dict

    return sales_retrieval_tool


def sales_writer_call(retrieval_respnse:str,security_checking_response:str,customer_email_subject:str,customer_email_body:str,customer_email_history:str,email_receiver:str):
    async def sales_writer_tool(retrieval_respnse:str,security_checking_response:str,email_subject:str,email_body:str,email_history:str,email_receiver:str):
        deployment = os.environ["AZURE_OPENAI_MODEL_NAME"]
        sys_meg = "You are a customer service agent in Avnet and your job is to write emails to customers. You must understand the sentiment of the customer and provide a helpful response. You should reply with a friendly and professional tone. You must start the email with the greeting and end with thanking them. You must always reply to the customerr in the same language they used in their email."
        human_msg = """Using sales transaction data and customer master data, draft an email to respond to [email_receiver]'s question in their email (including the subject, body, and email history).
        Notice:
        1. if customer's email body is start with 'Dear', then your generated response email must also start with 'Dear' and soldToName, otherwise use 'Hello' and soldToName;
        2. if the external sales partner name and contact name does not match in customer master dataset, you MUST add a new line of notice after ISR name , at the end of the response to inform ISR about the mismatch!
        3. if the soldto customer number and end customer number are both not equal to customer number in customer master data dataset, you MUST add a new line of notice after ISR name , at the end of the response to inform ISR!
        -----------------------------------------
        this is the field mapping from sales data to email fields:
        1. item : itemNo
        2. Customer PO#: poNumber
        3. Customer PN: customerPartNumber
        4. Item Qty:quantity
        5. Shipped Qty: totalShippedQty
        6. Estimated Ship Date : shippedDate or scheduleDate if shippedDate is null
        7. Status: orderStatus
        8. receiver: first name from email_receiver email address
        -----------------------------------------
        Here is the sammple email format. The email generated must be in HTML format and follow similar style as below:

        <body>Dear/Hello receiver /first name of {email_receiver}, 

        <p>The current status of your order: <order number> / depends on which kind of number customer is asking, can be Customer PO, Web Order, Sales order.. </p>
        / the below must be in a <table> 
        item  |Customer PO#  |  Customer PN   |  Item Qty|  Shipped Qty   |   Estimated Ship Date |   Status  
        0001  |1233455  |ABDDDD|21|21|20251201|shipped
        0002  |dldjhfd  |abiixx|200|100|20251011|Order In Process
        </table>

        <p>If you have any further questions or require assistance, please do not hesitate to contact me.</p>
        
        <p>Sincerely,</p>

        <p>ISR/CSR Name / in blue color</p>
        ----------------------------------------
        this is email receiver:{email_receiver}.
        this is email subject:{email_subject}.
        this is email body:{email_body}.
        this is email chat history:{email_history}.
        this is salse transaction data:{retrieval_respnse}.
        this is customer data:{security_checking_response}.
        your response should be only the generated email and nothing else!!!!""".format(email_receiver=email_receiver,email_subject=email_subject,email_body=email_body,email_history=email_history,retrieval_respnse=retrieval_respnse,security_checking_response=security_checking_response)
        client = AsyncAzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version = os.environ["AZURE_OPENAI_API_VERSION"],
            timeout=120,
            max_retries=1)
        try:
            resp = await client.chat.completions.create(
                model=deployment,
                temperature=0.0,
                max_tokens=4000,
                messages=[{"role":"system","content":sys_meg},{"role": "user", "content": human_msg}]
            )
            topic_resp = resp.choices[0].message.content

        except openai.BadRequestError as e:
            print("a Bad request error is happened")
        except openai.AuthenticationError as e:
            print("the authentication is having error")
        except openai.APIConnectionError as e:
            print("the server could not be reached")
            print(e.__cause__)
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit")
            print(e.status_code)
        except openai.APIStatusError as e:
            print("Anotehr non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except Exception as e:
            print("one of the 5 agents is having error, error message is: ", e)
        try:
            topic_resp = topic_resp.replace("```json","")
            topic_resp = topic_resp.replace("```","")
            topic_json = json.loads(topic_resp)
            topic_json_str = json.dumps(topic_json)
        except Exception as e:
            print("error when parsing topic resp to json ,",e)
            # try:
            #     print(f"response is : {topic_resp}")
            # except Exception as e:
            #     print("response is not a string")
            topic_json_str = ''
        return topic_resp
    
    return sales_writer_tool


def dir_sales_writer_tool(retrieval_respnse:str,security_checking_response:str,email_subject:str,email_body:str,email_history:str):
        deployment = os.environ["AZURE_OPENAI_MODEL_NAME"]
        sys_meg = "you are a helpful assistant"
        human_msg = """by using salse transactiondata and customer master data, try to write an email to answer customer's question in customer' email(email subject, email body, email history).
        Notice:
        1. if customer's email body is start with 'Dear', then your generated response email must also start with 'Dear' and soldToName, otherwise use 'Hello' and soldToName;
        2. if the soldto customer number and end custoemr number are both not equal to customer number in customer master data dataset, you MUST add a line of notice to inform it!
        -----------------------------------------
        this is the field mapping from sales data to email fields:
        1. item : itemNo
        2. Customer PO#: poNumber
        3. Customer PN: customerPartNumber
        4. Item Qty:quantity
        5. Shipped Qty: totalShippedQty
        6. Estimated Ship Date : shippedDate or scheduleDate if shippedDate is null
        7. Status: orderStatus
        8. soldToName: soldToName
        -----------------------------------------
        the email format you generated must be follow this format:

        Dear/Hello soldToName ,

        The current status of your order: <order number> / depends on which kind of number customer is asking, can be Customer PO, Web Order, Sales order..
        item  |Customer PO#  |  Customer PN   |  Item Qty|  Shipped Qty   |   Estimated Ship Date |   Status  
        0001  |1233455  |ABDDDD|21|21|20251201|shipped
        0002  |dldjhfd  |abiixx|200|100|20251011|Order In Process


        If you have any further questions or require assistance, please do not hesitate to contact me.
        
        Sincerely,

        ISR/CSR Name
        ----------------------------------------
        this is email subject:{email_subject}.
        this is email body:{email_body}.
        this is email chat history:{email_history}.
        this is salse transaction data:{retrieval_respnse}.
        this is customer data:{security_checking_response}.
        your response should be only the generated email and nothing else!!!!""".format(email_subject=email_subject,email_body=email_body,email_history=email_history,retrieval_respnse=retrieval_respnse,security_checking_response=security_checking_response)
        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version = os.environ["AZURE_OPENAI_API_VERSION"],
            timeout=120,
            max_retries=1)
        try:
            resp =  client.chat.completions.create(
                model=deployment,
                temperature=0.0,
                max_tokens=4000,
                messages=[{"role":"system","content":sys_meg},{"role": "user", "content": human_msg}])
            topic_resp = resp.choices[0].message.content

        except openai.BadRequestError as e:
            print("a Bad request error is happened")
        except openai.AuthenticationError as e:
            print("the authentication is having error")
        except openai.APIConnectionError as e:
            print("the server could not be reached")
            print(e.__cause__)
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit")
            print(e.status_code)
        except openai.APIStatusError as e:
            print("Anotehr non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except Exception as e:
            print("one of the 5 agents is having error, error message is: ", e)
        try:
            topic_resp = topic_resp.replace("```json","")
            topic_resp = topic_resp.replace("```","")
            topic_json = json.loads(topic_resp)
            topic_json_str = json.dumps(topic_json)
        except Exception as e:
            print("error when parsing topic resp to json ,",e)
            # try:
            #     print(f"response is : {topic_resp}")
            # except Exception as e:
            #     print("response is not a string")
            topic_json_str = ''
        return topic_resp
