class Config():



    #Process working modes
    # 0 => Get PDF files from DMS Item. Addiontally truncate pages of PDF to PARAM_PDF_MAX_PAGES, only if PARAM_TRUNCATE_PDF_PAGES is True
    #      Resultig PDF files are stored in PARAM_TARGET_FOLDER
    # 1 => Get PDF files from DMS Item and transform its pages either to JPEG images files or its base64 representation to TXT files.
    #      The PARAM_TRANSFORM_JPEG_TO_BASE64_TEXT_FILE parameter indicates whether to save the file as a JPEG (False) or as a TXT file (True). 
    #      In any case, the maximum number of pages of the PDF file to be taken into account is limited to that indicated in
    #      parameter PARAM_PDF_MAX_PAGES.
    #Working Modes
    MODE_GET_PDF = 0
    MODE_GET_IMAGES = 1

    # Json parameters - Used internally in this class
    PARAM_DMS_URI = "dmsUri"
    PARAM_DMS_USER = "dmsUser"
    PARAM_DMS_PASS = "dmsPass"
    PARAM_DMS_QUERY = "dmsQuery"
    PARAM_DMS_QUERY_PAGE_SIZE = "queryPageSize"
    PARAM_MAX_PAGES_TO_QUERY = "maxPagesToQuery"
    PARAM_WORKING_MODE = "workingMode"
    PARAM_PURGE_FILES = "purgeFiles"
    PARAM_TARGET_FOLDER = "targetFolder"
    PARAM_TEMP_FOLDER = "tempFolder"
    PARAM_TRANSFORM_JPEG_TO_BASE64_TEXT_FILE = "transformJpegToBase64TextFile"
    PARAM_POPPLER_BINARIES_PATH = "popplerBinariesPath"
    PARAM_TRUNCATE_PDF_PAGES = "truncatePdfPages"
    PARAM_PDF_MAX_PAGES = "pdfMaxPages"
    PARAM_JPEG_DPI = "jpegDpi"

    app_cfg = None

    def __init__(self, cfg):
        self.app_cfg = cfg

    # Json values - Return
    def get_dms_uri(self):
        return self.app_cfg[self.PARAM_DMS_URI]

    def get_dmsuser_name(self):
        return self.app_cfg[self.PARAM_DMS_USER]

    def get_dmsuser_pass(self):
        return self.app_cfg[self.PARAM_DMS_PASS]

    def get_query(self):
        return self.app_cfg[self.PARAM_DMS_QUERY]

    def get_query_pagesize(self):
        return self.app_cfg[self.PARAM_DMS_QUERY_PAGE_SIZE]

    def get_max_pages_to_query(self):
        return self.app_cfg[self.PARAM_MAX_PAGES_TO_QUERY]



    def get_working_mode(self):
        return self.app_cfg[self.PARAM_WORKING_MODE]

    def get_purge_files(self):
        return self.app_cfg[self.PARAM_PURGE_FILES]

    def get_target_folder(self):
        return self.app_cfg[self.PARAM_TARGET_FOLDER]

    def get_temp_folder(self):
        return self.app_cfg[self.PARAM_TEMP_FOLDER]


    def get_transform_to_base64(self):
        return self.app_cfg[self.PARAM_TRANSFORM_JPEG_TO_BASE64_TEXT_FILE]

    def get_poppler_binaries_path(self):
        return self.app_cfg[self.PARAM_POPPLER_BINARIES_PATH]

    def get_truncate_pdf_pages(self):
        return self.app_cfg[self.PARAM_TRUNCATE_PDF_PAGES]

    def get_pdf_max_pages(self):
        return self.app_cfg[self.PARAM_PDF_MAX_PAGES]

    def get_jpeg_dpi(self):
        return self.app_cfg[self.PARAM_JPEG_DPI]


