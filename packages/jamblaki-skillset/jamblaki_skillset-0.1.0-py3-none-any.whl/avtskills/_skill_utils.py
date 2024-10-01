import asyncio,aiohttp,json,os
import datetime
from pytz import timezone
import openai
from openai import AzureOpenAI,AsyncAzureOpenAI
from ._sales_prompt import order_query_prompt,system_prompt



async def ageneral_call(human_msg):
    deployment = os.environ["AZURE_OPENAI_MODEL_NAME"]

    client = AsyncAzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version = os.environ["AZURE_OPENAI_API_VERSION"],
    timeout=120,
    max_retries=1)

    sys_meg = system_prompt
    human_msg = human_msg
    try:
        resp = await client.chat.completions.create(
            model=deployment,
            temperature=0.0,
            max_tokens=4000,
            messages=[{"role":"system","content":sys_meg},{"role": "user", "content": human_msg}]
        )
        gen_resp = resp.choices[0].message.content

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
        print("-----general_resp is ----------")
        print(gen_resp)
        print("----------------------------")
        gen_resp = gen_resp.replace("```json","")
        gen_resp = gen_resp.replace("```","")
        # gen_resp_json = json.loads(gen_resp)
        # gen_resp_json_str = json.dumps(gen_resp_json)
    except Exception as e:
        print("error when parsing topic resp to json ,",e)
        gen_resp = ''
    return gen_resp



async def aorder_status_body_call(email_subject:str,email_body:str,email_history:str)-> str:

    today_tm = datetime.datetime.now(timezone('America/Phoenix')).strftime('%Y-%m-%d %H:%M:%S')
    human_msg = order_query_prompt.format(today = today_tm,email_subject=email_subject,email_body = email_body,chat_history=email_history)
    query_resp = await ageneral_call(human_msg)
    return query_resp


async def post_backlog_po(email_body):
    sales_url = os.environ["SALES_URL"]
    json_data = email_body
    APIM_key = os.environ["SALES_APIM_KEY"]
    headers = {'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': APIM_key,
                'Accept': '*/*'
                }
    print("----------------RAG API REQUEST BODY------")
    print(json_data)
    print("----------end---------------")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(sales_url,data = json_data,headers=headers) as resp:
                sales_summary_resp = await resp.text()
        print("---------Sales api return---------")
        print(sales_summary_resp)
        print("-----------------------")
        return sales_summary_resp
    except Exception as e:
        print("sales_summary_call has error, error is ", e)
        return e

async def abk_api_call(email_body):
    try:
        summary_resp = await post_backlog_po(email_body)   
    except Exception as e:
        print(e)
        summary_resp = "Oh dear, it seems I've run into a language riddle.Can you help me out by rephrasing your question in a less puzzling way?"
    return summary_resp