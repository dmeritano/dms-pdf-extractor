## DMS PDF EXTRACTOR
* * *

**Current versión**: 1.0

Last release: `07-08-2024`

### Description
This application is designed to extract PDFs from multimedia items contained within DMS documents. The idea is to program a applicationquery` to obtain these documents - for example `(Hoja_Recurso_Apelacion & $#NumeroCola=10)` and then proceed to process them according to the configured processing mode ( `workingMode` ).

If `workingMode=0`, the program will extract the PDF from each item and store it in the configured folder ( `targetFolder` ). These PDFs can also be truncated to only `N` pages by configuring the parameters `truncatePdfPages` and `pdfMaxPages` respectively. For example, if `truncatePdfPages=true` and `pdfMaxPages=2`, all PDFs with more than 2 pages will be truncated, leaving only 2 of the pages they contained. If `truncatePdfPages=false`, the PDFs remain as they were downloaded from the DMS repository. In this operating mode, the resulting files generated in the 'targetFolder' are named with the `DMS-ID + ".pdf"`.

If `workingMode=1`, the program will convert the pages of the PDFs either into JPEG files ( `transformJpegToBase64TextFile=false` ) or into text files containing a representation of the JPEG files encoded in Base64 ( `transformJpegToBase64TextFile=true` ). In this operating mode, the parameter `pdfMaxPages` will also be used to determine how many pages to extract at most from the PDF files. The resulting files in this operating mode (also in the folder specified in `targetFolder` ) are named with the `DMS-ID + PPP + EXTENSION`, where `PPP` refers to the page number in 3-digit format, for example, page 1 would be 001. The values for `EXTENSION` will be either `.jpg` or `.txt` when `transformJpegToBase64TextFile=true`.

To avoid having too many files in the root folder `targetFolder`, up to 10 subfolders will be created within it, with the name of these corresponding to the last digit of the `DMS-ID` of the item obtained from the repository.



**Configuration File:** ```appconfig.json```

**Sample:**
```json
{
    "dmsUri": "[URL API DMS]",
    "dmsUser": "[USER DMS]",
    "dmsPass": "[PASS DMS]",
    "dmsQuery": "[QUERY DMS]",
    "queryPageSize": 5,
    "maxPagesToQuery": 1,
    "workingMode": 1,
    "purgeFiles": true,
    "targetFolder": "[TARGET FOLDER]",
    "tempFolder": "[TEMP FOLDER]",
    "transformJpegToBase64TextFile": true,
    "popplerBinariesPath": "[LOCAL POPPLER BINARIES PATH]",
    "truncatePdfPages": false,
    "pdfMaxPages": 2,
    "jpegDpi": 100,
}
```

### DISTRIBUTION

Use the script `build.bat` located in project root folder to generate executable (EXE) in the DIST folder of the project. Batch script also copies the configuration file to "DIST"  folder and some BIN files needed for packages like Pdf2Image.