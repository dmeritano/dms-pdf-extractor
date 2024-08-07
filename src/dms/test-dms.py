import logging
from dms import api_dms


logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)-20s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("app")

def main():

    # v5 - Test
    # URL DRS = "http://16?.???.???.119/DmsV5"
    # URL AAD = "http://16?.???.???.119/AAV5"
    # USER = "USUARIO V5"
    # PASSWORD = "PASS V5"

    # v6 - Test
    # URL DRS = "http://16?.???.???.119/DmsV6"
    # URL AAD = "http://16?.???.???.119/AAV6"
    # USER     = "USUARIO V6"
    # PASSWORD = "PASSWORD V6"

    login_st = api_dms.login(URL, USER, PASSWORD, False)
    if login_st:
        print(f"User {USER} authenticated")
    else:
        logger.error(f"User {USER} could not be authenticated")
        return

    """
    documents = api_dms.get_documents_by_query("Recurso_Apelacion","$#TModificado",1,5,False)
    if documents:
        print(documents)
    """

    """
    document = api_dms.get_document_by_id("11790381012221953")
    if document:
        print(document)
    """

    """
    data_to_update = {
        "attributes":{
            "Numero_Boleto_8":"0"
        }
    }
    updated = api_dms.update_document("11790381012221953",data_to_update)
    """

    """
    doc_childrens = api_dms.get_document_childrens("11790381012221953")
    if doc_childrens:
        print(doc_childrens)
    """

    """
    api_dms.get_multimedia_item("11790381012221954","./doc.pdf")
    """
    """
    wf_queues = api_dms.get_workflow_queues("DTOP_RECURSO_DE_APELACION")
    print(wf_queues)
    """

    """
    doc_types = api_dms.get_document_types()
    if doc_types:
        print(doc_types)
    """

    """
    doc_definition = api_dms.get_document_definition("Recurso_Apelacion")
    if doc_definition:
        print(doc_definition)
    """

    """
    user = api_dms.get_user("CONFIGURACION_ATRIL")
    if user:
        print(user)
    """

    """
    users = api_dms.get_users()
    if users:
        print(users)
    """

    """
    
    ## Create documents - Then upload a multimedia item for "Side" document
    # ---------------------------------------------------------------------
    # Root
    #   Operations (34359738382)
    #       Area_DESA(32654636351490)
    #           Expediente_DESA     (documento a crear  - primera peticion)
    #               Caratula_DESA   (documento a crear  - segunda peticion)
    #                   Side        (documento a crear  - tercera peticion)
    #
    #PRIMERA PETICION
    doc_type = "Expediente_DESA"
    data = {
        "meta":{
            "type":doc_type,
            "item":"false"
        },
        "attributes":{
            "expediente_desa_date" : "20240617"
        }
    }    
    doc_created = api_dms.create_document("32654636351490",data)
    if doc_created:        
        id_expediente_desa = doc_created["attributes"]["#Id"]    
        print(f"Created document {doc_type} with Id {id_expediente_desa}")
        
        #SEGUNDA PETICION
        doc_type = "Caratula_DESA"
        data = {
            "meta":{
                "type":doc_type,
                "item":"false"
            },
            "attributes":{
                "caratula_desa_itemsize" : "18984"
            }
        }
        doc_created = api_dms.create_document(id_expediente_desa,data)
        if doc_created:            
            id_caratula_desa = doc_created["attributes"]["#Id"]
            print(f"Created document {doc_type} with Id {id_caratula_desa}")
            
            #TERCERA PETICION
            doc_type = "Side"
            data = {
                "meta":{
                    "type":"Side",
                    "item":"true"
                },
                "attributes":{
                    "view_origin" : "test"
                }
            }
            doc_created = api_dms.create_document(id_caratula_desa,data)
            if doc_created:
                id_item = doc_created["attributes"]["#Id"]
                print(f"Created document {doc_type} with Id {id_item}")

    
    #UPLOAD MULTIMEDIA ITEM 
    with open("./doc.pdf", "rb") as f:
        data = f.read()    
        
    result = api_dms.create_update_item(id_item,"application/pdf",data)
    if result:
        print(f"Multimedia item upload succesfully to document {id_item}")
    
    """

    api_dms.logout()
    print(f"User {USER} disconnected")


# Main
if __name__ == "__main__":
    main()
