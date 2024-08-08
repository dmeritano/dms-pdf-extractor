import logging
import os
import io
import os.path
import shutil
import math
import base64
from time import sleep
from pypdf import PdfWriter, PdfReader
from pdf2image import convert_from_bytes


# import Config
from config import Config
from dms import api_dms

# App Config
cfg = None

app_config = Config({})

# Logging system
logger = logging.getLogger(__name__)

def start(config):
    global app_config
    app_config = config
    st_login = None
    
    logger.info("Main process started")
    
    #Check access to process configured folders
    if not check_folders():
        logger.warn("Process cannot continue")    
        return        

    # DMS - Login
    st_login = api_dms.login(app_config.get_dms_uri(), 
                    app_config.get_dmsuser_name() , 
                    app_config.get_dmsuser_pass(), False)
    if not st_login:
        logger.warn("Process cannot continue")    
        return

    # Get list of documents from specified query
    documents = get_documents_list()
    if len(documents) > 0:                
        # Deberiamos borrar las imagenes
        if app_config.get_purge_files():
            purge_files(documents)

        if app_config.get_working_mode() == Config.MODE_GET_PDF:
            get_pdfs(documents)
        elif app_config.get_working_mode() == Config.MODE_GET_IMAGES:
            extract_images_from_pdfs(documents)            
    
    # Disconnect from DMS
    if st_login:
        api_dms.logout()

    #Empty temp folder ??
    empty_temp(app_config.get_temp_folder())

    logger.info("Main process finished")
    

def extract_images_from_pdfs(documents):
    
    num_docs = len(documents)

    try:

        print("Extract images/base64 data from PDF files started ...")

        for idx, idDms in enumerate(documents):
            sleep(1)
            msg = f"Processing ID {idDms} - {str(idx + 1).zfill(5)} of {str(num_docs).zfill(5)}"
            logger.info(msg)                               
            item_bytes = api_dms.get_multimedia_item_bytes(idDms)
            if len(item_bytes) > 0:
                pdf_pages = convert_from_bytes(item_bytes, poppler_path=app_config.get_poppler_binaries_path(), dpi=app_config.get_jpeg_dpi())
                for idx, image in enumerate(pdf_pages):               
                    file_name = None
                    if app_config.get_transform_to_base64():                    
                        file_name = get_output_file_name_with_path(idDms,idx+1,".txt")
                        test = io.BytesIO()
                        image.save(test,"jpeg")                
                        #Save as 
                        test.seek(0)
                        base64_encoded = base64.b64encode(test.read())

                        with open(file_name, "w") as f_target:
                            f_target.write(str(base64_encoded,"utf-8"))
                    
                    else:   #Save images JPEG                        
                        file_name = get_output_file_name_with_path(idDms,idx+1,".jpg")
                        image.save(file_name,"jpeg")                
                    
                    #Check for process cancell by configuration
                    if (idx + 1) == app_config.get_pdf_max_pages():
                        break

            else:
                msg = f"Could not get PDF bytes for ID {idDms}"
                logger.error(msg)

    except Exception as error:
        msg = f"Error extracting images: {error.args}"
        logger.error(msg)   

    print("Extract images/base64 data from PDF files finished") 

def get_pdfs(documents):

    print("Getting and processing PDFs files")

    num_docs = len(documents)
    temp_dir = app_config.get_temp_folder()
    try:
        for idx, idDms in enumerate(documents):
            sleep(1)
            msg = f"Processing ID {idDms} - {str(idx + 1).zfill(5)} of {str(num_docs).zfill(5)}"
            logger.info(msg)
            temp_file = f"{temp_dir}/{idDms}.pdf"
            final_file = get_output_file_name_with_path(idDms,None,".pdf")            

            response = None
            if app_config.get_truncate_pdf_pages():
                response = api_dms.get_multimedia_item(idDms,temp_file,8192)
                if response:
                    control_pdf_pages(idDms, temp_file, final_file)    
            else:
                response = api_dms.get_multimedia_item(idDms,final_file,8192)
            
            if not response:
                logger.error(f"Error getting multimedia item for idDms {idDms}")

    except Exception as error:
        msg = f"Error running job: {error.args}"
        logger.error(msg)

    print("Finished PDF files")

def control_pdf_pages(idDms, temp_file, final_file):

    max_pages = app_config.get_pdf_max_pages()
    output = PdfWriter()

    try:        
        msg = f"Final file for PDF corresponding to Id {idDms} -> {final_file}"
        logger.info(msg)

        move_nochanges = False
        with open(temp_file, "rb") as f_source:
            input_pdf = PdfReader(f_source)
            total_pages = len(input_pdf.pages)

            if total_pages > max_pages:
                for x in range(max_pages):
                    output.add_page(input_pdf.get_page(x))        

                with open(final_file, "wb") as f_target:
                    output.write(f_target)
                            
                msg = f"Pages of PDF corresponding to IdDms {idDms} were truncated from {total_pages} to {max_pages} pages"
                logger.info(msg)
            else:
                move_nochanges = True
                        
        if move_nochanges:
            shutil.move(temp_file,final_file)

        if os.path.exists(temp_file):
            os.remove(temp_file)

    except Exception as e:
        logger.error(f"Error: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as ex:
                logger.error(f"Error: {ex}")



def get_output_file_name_with_path(idDms,page,extension):
    try:        
        subfolder = idDms[-2:]
        complete_path = f"{app_config.get_target_folder()}/{subfolder}"
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)

        if (page == None): #PDF Files
            return f"{complete_path}/{idDms}{extension}"
        else:              #JPEG or TXT Files
            return f"{complete_path}/{idDms}-{str(page).zfill(3)}{extension}"
        
    except OSError as e:
        logger.error(f"Error creating folder: {e}")
        
    return None


def get_documents_list():

    page_size = app_config.get_query_pagesize()
    all_documents = []
    max_query_pages = app_config.get_max_pages_to_query()

    try:

        print("Getting documents from DMS ...")

        if max_query_pages == 0:
            return all_documents
        msg = f"Getting document list, page size {page_size}"
        logger.info(msg)

        #Get Total of documents
        query = app_config.get_query()
        response = api_dms.get_documents_by_query(query, "$#TModificado", None, None, True)
        total = int(response["meta"]["total"])
        if total == 0:
            return all_documents
        
        total_pages = math.ceil(total / page_size)
        for currentPage in range(total_pages):
            response = api_dms.get_documents_by_query(query, "$#Id", currentPage + 1, page_size, False) #pages start from 1 (not zero)
            docs = response["docs"]
            if len(docs) > 0:                
                for item in range(len(docs)):
                    all_documents.append(docs[item]["#Id"])                    
            
            #Check for process cancell
            if (max_query_pages != -1):
                if (currentPage + 1) == max_query_pages:
                    break
                          
        all_documents.sort()

        print(f"Documents retrieved from DMS: {len(all_documents)}")

        return all_documents
    
    except Exception as error:
        msg = f"Error running job: {error.args}"
        logger.error(msg)
    
    return all_documents

def purge_files(documents):
    
    print("File purge function started ...")

    purged = 0    
    files_found = find_files(app_config.get_target_folder())        
    msg = f"Files found in {app_config.get_target_folder()}: {len(files_found)}"
    logger.info(msg)
    
    if files_found:        
        for f in files_found:
            fname = os.path.basename(f)[:-8]
            if fname not in documents:
                #Delete
                os.remove(f)
                purged = purged + 1

    msg = f"Purge process finished with {purged} files deleted" 
    logger.info(msg)
    print(msg)


def find_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            #if file.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(root, file))
    
    return pdf_files

def check_folders():

    response = False

    try:
        #Target
        folder = app_config.get_target_folder()
        if os.path.isdir(folder):
            if os.access(folder, os.R_OK):
                response = True
        
        if not response:
            msg = f"Folder {folder} does not exist or is not writable"
            logger.error(msg)

        if response and ((app_config.get_working_mode() == Config.MODE_GET_PDF) and app_config.get_truncate_pdf_pages()):
            folder = app_config.get_temp_folder()
            if not os.path.isdir(folder):
                response = False
            else:
                if not os.access(folder, os.R_OK):
                    response = False
            
            if not response:
                msg = f"Folder {folder} does not exist or is not writable"
                logger.error(msg)


    except Exception as e:
        logger.error(e)

    return response


def empty_temp(folder_path):

    if not os.path.isdir(folder_path):
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the subfolder
        except Exception as e:
            logger.error(f'Failed to delete {file_path}. Reason: {e}')    