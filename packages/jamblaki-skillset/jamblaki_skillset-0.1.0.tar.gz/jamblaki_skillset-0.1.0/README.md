# Skillset Defined
skill set  

#Notice:  
1. set these entries in env. configuration (local: in .env file; server: in server env. setting)     
    for security checking endpoint:  
        security_req_url = os.environ.get("SECURITY_REQ_URL")    
        security_apim_key = os.environ.get("SECURITY_APIM_KEY")    
    for RAG endpoint:  
        sales_url = os.environ["SALES_URL"]  
        APIM_key = os.environ["SALES_APIM_KEY"]  