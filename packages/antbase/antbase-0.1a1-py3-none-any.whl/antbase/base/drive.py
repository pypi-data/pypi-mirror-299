import io, base64
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image
from typing import TypedDict, NotRequired
from datetime import datetime as Date

from antbase.base.log import Log, Auth

class ImageInfo(TypedDict):
    title:    str
    imageUrl: str
    altText:  str
    openLink: str

class ImageMeta(TypedDict):
    width:    int
    height:   int
    rotation: float

class FileMeta(TypedDict):
    '''Структура Метаданных Файла'''
    kind:                str # "drive#file"
    id:                  str
    name:                str
    mimeType:            str
    createdTime:         Date
    modifiedTime:        Date
    fileExtension:       str # "jpg"
    size:                int
    version:             str
    driveId:             str
    teamDriveId:         str
    starred:             bool
    trashed:             bool      
    imageMediaMetadata:  ImageMeta
    hasThumbnail:        bool
    thumbnailVersion:    int
    thumbnailLink:       str
    webViewLink:         str
    webContentLink:      str
    properties:          dict

class Drive:
    __service = Auth.get_drive_service()

    ANT_DRIVE            = "0AAOepvRO6ZQAUk9PVA"
    DB_DRIVE             = "0ACwszgPPnyU3Uk9PVA"
    CASTING_DRIVE        = "0AP6ujHcLcLS7Uk9PVA"

    GOOGLE_DRIVE         = "0AIi93Y2wZeObUk9PVA"
    WK_SAND_BOX_DRIVE    = "0AAxvgP-VidH6Uk9PVA"

    TEST_SHEET           = "1kHjoFh3xfLoit6UVksqn_xnKjkBSGettUB4Qt5vWrRY"

    # Фолдеры
    m_ph           = "1zdU2TT2Td0Z87-I2sbkeJVNWll58AMJr"  # Google Drive > JB_Orders > pms > m_ph
    p_sk           = "13ddCnDG2tf7xEVHQrcB_Mvaf7QroNaHc"  # Google Drive > JB_Orders > pms > p_sk
    p_ph           = "1z6zg8UZy9HlxejazBvSX_Fzw0JcfmZcn"  # Google Drive > JB_Orders > pms > p_ph
    i              = "1NNrJGGpIM-yTEX1bFMxBD8ePDKlRKBAR"  # Google Drive > JB_Orders > pms > i
    w              = "13ddCnDG2tf7xEVHQrcB_Mvaf7QroNaHc"  # Google Drive > JB_Orders > pms > w
    a              = "1vQRknCkm3OR1uEu_2-K3bcuzK6dCxYyy"  # Google Drive > JB_Orders > pms > a
    orderPhoto     = "1g-e0DjOaY5ogm0ODuwPBN_mFaE3Jan_D"  # ANT_DRIVE > orderPhoto

    # Шаблоны
    Template       = "1nTfPtlFM0AX8NUwyniqqDchwkFkhB306"

    # sdo
    Sdo            = "1lLUpv_Mymgy9pS8A_KKIRPxe5eRZoVD9"
    dictionary_db  = "1cUGc_4RXW30ibYn_KStvdupcndxlbARd"
    dictionary     = "1SL5rQrQ6y8q7GNgSV1MMqC-5BvZwnEDxCRz3xIcZne8"

    # sko person
    Persons_folder        = "1JWboTHx4dkKuTaQOlwpChwiIwvSSsckD"
    Person_im_folder      = "1hXLaU2ViwYKWwlWcvzlnvabSSQLsAYu6"
    person_template_sheet = "1KilE702v6lGH8QONxK1WrlZjOiP1SwJAbJCfGRtcq4Y"
    persons_sheet         = "1Ehw89CGrpB6mLIf7LKcPHoPWpNxc_Zc5eHOidoLX4Yk"
    persons_reg_sheet     = "10oboTYZs1cL8YwfmKxrLUe4AvvBNwvqy1bwcpId8ahU"
    wt_sheet              = "1BjfR1D9KCTVbmG2BwgCxhoSJ3s4XphdX_T8eLhWUhNw"

    # sko cjob
    Cjob_arch_folder      = "1Dr4HUALTd2TJj7ON31lTcazAG5DVla9y"
    Cjob_im_folder        = "1CAvnHU3Pf0Wx1_crsEBwhREyIQ8dkr67"
    Casting_sheeet        = "1Mpcmzr63W7p8ZdFWw2Oxd6IbGyu_gxc9"
    casting_sheet         = "1GjOnbt-WVVPH-j4aMHGWKocFYMeFdhzZdFGQjKDum44"
    cjob_template_sheet   = "1VeCon_vtRNhgwiaYU4Z_3OX5k53jYTx25g2-TqxzY1w"

    # sko order
    Order_db_folder       = "1PAiW2LPZs4QkVX_GGfjUTA0VrIEz1Kr_"
    Order_us_folder       = "1_1_o4mT-a6_w_8wwboY3HrGckBbCijTE"
    Order_im_folder       = "1eSKIHvMoUvQblk9INplOZewtzmmjSvLY"
    orders_sheet          = "12egN0DA2IajUrtOCbmJRdBW2YDcqBP_VIiB75DmZg0o"
    order_template_sheet  = "1gVrDUPpR1Yof1-hW91LvPnvwO5eJOn2nY_BVM8eJYrg"
    r500_sheet            = "115yVuthxDZ9ZCfty7QeQJi3LdDAzkamWGiVvJPJz5hI"

    # job
    Job_db         = "12-Uq8Hz4pY2vl-mg4q_-4ecxnCfdQwbt"
    Job_us         = "1G3ez1VqHtngo6V7z0-J9nSvMAxk4UpN2"
    Job_im         = "15QvW1_OpsRRRLT-0_YR_Bfk-7hr2ghu2"
    Job_arch       = "1-IYsakYJgJYjMq0coaTDBtTCHNiBZaZgC8Q0dP0BMVI"
    jobs           = "1Vk3wK8GRSjznnueCTVCJ9IUaNIo1Z3DFibcXKGSf2Ks"
    job_tp         = ""

    # track
    Track_old_folder     = "1_wl04CACAzYWsSrvAbK1IHfexof4HbEo"
    Track_folder         = "1xxzJJ9weM6k48q1VRlMLhI9VLD0I3j5u"
    track_sheet          = "1-IYsakYJgJYjMq0coaTDBtTCHNiBZaZgC8Q0dP0BMVI"
    track_diana_sheet    = "1OqAUil7oWUScexekhVDMBAxfZQ1cNDtxwYlceowTc00"

    # skoPjob
    P_cs           = "1z39e_e9nGqYkPMU_kRUOlq_8ZDDgYNgV"
    Pjob_us        = "1HxxRFN17WNaaPiK7yLuovppvQoL5ev8A"
    Pjob_db        = "1mwHcQwyT5n8RtQtyMaAd9TNjPGeOB1_m"
    r500           = "115yVuthxDZ9ZCfty7QeQJi3LdDAzkamWGiVvJPJz5hI"
    pjob_tp        = "1UZWVjsGk2nl-LsJ0I5tcI_EB8eRYLu8ncJzAs0YbJYw"

    # sheets
    balance_sheet  = "19JMMrnmyEYVr95gsOAdgkPQIi28AsI-_zciX_njNBgk"
    finance_sheet  = "1pj0FxuJlUCB7BUgiNNfDdK8OB2IKbAAK6CTRCoqysbo"

    URL = {
        "persons_arch": "https://docs.google.com/spreadsheets/d/10oboTYZs1cL8YwfmKxrLUe4AvvBNwvqy1bwcpId8ahU/edit?usp=sharing",
        "persons":      "https://docs.google.com/spreadsheets/d/1Ehw89CGrpB6mLIf7LKcPHoPWpNxc_Zc5eHOidoLX4Yk/edit?usp=sharing",
        "orders":       "https://docs.google.com/spreadsheets/d/12egN0DA2IajUrtOCbmJRdBW2YDcqBP_VIiB75DmZg0o/edit?usp=sharing",
        "casting":      "https://docs.google.com/spreadsheets/d/1GjOnbt-WVVPH-j4aMHGWKocFYMeFdhzZdFGQjKDum44/edit?usp=sharing",
        "production":   "https://docs.google.com/spreadsheets/d/115yVuthxDZ9ZCfty7QeQJi3LdDAzkamWGiVvJPJz5hI/edit?usp=sharing",
        "dictionary":   "https://docs.google.com/spreadsheets/d/1SL5rQrQ6y8q7GNgSV1MMqC-5BvZwnEDxCRz3xIcZne8/edit?usp=sharing"
    }

    IMAGE        = "image/"
    JPEG         = "image/jpeg"
    SHEET        = "application/vnd.google-apps.spreadsheet"
    JSON         = "application/json"
    PDF          = "application/pdf"
    EXCEL_LEGACY = "application/vnd.ms-excel"
    EXCEL        = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    @staticmethod
    def get_file_name(file_id: str) -> str:
        try:
            file_metadata = Drive.__service.files().get(fileId=file_id, supportsAllDrives=True).execute()
            return file_metadata.get('name')
        except Exception as e:
            Log.error(f"Error getting file name: {e}")
        
    @staticmethod
    def get_file_blob(file_id: str) -> bytes:
        try:
            file_metadata = Drive.__service.files().get(fileId=file_id, alt='media', supportsAllDrives=True).execute()
            return file_metadata
        except Exception as e:
            Log.error(f"Error getting file blob: {e}")
        
    @staticmethod
    def get_file_url(file_id: str) -> str:
        try:
            file_metadata = Drive.__service.files().get(fileId=file_id, supportsAllDrives=True).execute()
            return file_metadata.get('webContentLink')
        except Exception as e:
            Log.error(f"Error getting file URL: {e}")

    @staticmethod
    def set_name(file_id: str, name: str) -> None:
        try:
            file_metadata = {'name': name}
            Drive.__service.files().update(fileId=file_id, body=file_metadata, fields='id', supportsAllDrives=True).execute()
            Log.info(f"File {file_id} renamed to {name}")
        except Exception as e:
            Log.error(f"Error renaming file: {e}")

    @staticmethod
    def move_file(file_id: str, to_folder_id: str):
        try:
            file_metadata = {'parents': [to_folder_id]}
            Drive.__service.files().update( fileId=file_id, body=file_metadata, fields='id', supportsAllDrives=True).execute()
            Log.info(f"File {file_id} moved to folder {to_folder_id}")
        except Exception as e:
            Log.error(f"Error moving file: {e}")

    @staticmethod
    def create_file_empty(file_name: str, folder_id: str, mime_type: str=None):
        mime_type = mime_type or Drive.JSON
        try:
            file_metadata = {'name': file_name, 'parents': [folder_id], 'mimeType': mime_type }
            file = Drive.__service.files().create( body=file_metadata, fields='id', supportsAllDrives=True ).execute()
            Log.info(f"File {file_name} created with ID: {file.get('id')}")
            return file.get('id')
        except Exception as e:
            Log.error(f"Error creating empty file: {e}")
        
    @staticmethod
    def update_file_metadata(file_id: str, name: str=None, description: str=None, mime_type: str=None):
        mime_type = mime_type or Drive.JSON
        try:
            file_metadata = {}
            if name:        file_metadata['name'] = name
            if description: file_metadata['description'] = description
            if mime_type:   file_metadata['mimeType'] = mime_type
            Drive.__service.files().update( fileId=file_id, body=file_metadata, fields='id', supportsAllDrives=True ).execute()
            Log.info(f"File {file_id} metadata updated.")
        except Exception as e:
            Log.error(f"Error updating file metadata: {e}")

    @staticmethod
    def update_file_props(file_id: str, props: dict):
        try:
            file_metadata = {'properties': props}
            Drive.__service.files().update( fileId=file_id, body=file_metadata, fields='id', supportsAllDrives=True ).execute()
            Log.info(f"File {file_id} properties updated.")
        except Exception as e:
            Log.error(f"Error updating file properties: {e}")

    @staticmethod
    def update_file_media(file_id: str, file_object: io.BytesIO, mime_type: str = None):
        mime_type = mime_type or Drive.JSON
        try:
            # Используем MediaIoBaseUpload для загрузки данных из BytesIO
            media = MediaIoBaseUpload(file_object, mimetype=mime_type, resumable=True)
            
            # Обновляем файл на Google Drive
            Drive.__service.files().update(
                fileId=file_id, 
                media_body=media, 
                fields='id', 
                supportsAllDrives=True
            ).execute()

            Log.info(f"File {file_id} content updated.")
        except Exception as e:
            Log.error(f"Error updating file content: {e}")
        

    @staticmethod
    def get_file_media(file_id: str):
        try:
            request = Drive.__service.files().get_media(fileId=file_id, supportsAllDrives=True)
            file_data = io.BytesIO()  # Создаем буфер для записи данных
            downloader = MediaIoBaseDownload(file_data, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")
            
            file_data.seek(0)  # Возвращаемся к началу данных
            return file_data  # Возвращаем бинарные данные в виде BytesIO объекта
        except Exception as e:
            Log.error(f"Error downloading file: {e}")

    @staticmethod
    def get_jpeg_blob(jpeg_url:str) -> bytes:
        try:
            return MediaFileUpload( jpeg_url, mimetype='image/jpeg', resumable=True )
        except Exception as e:
            Log.error(f"Error getting JPEG blob: {e}")

    @staticmethod
    def get_file_metadata(file_id: str) -> FileMeta:
        try:
            return Drive.__service.files().get( fileId=file_id, fields='*', supportsAllDrives=True ).execute()
        except Exception as e:
            Log.error(f"Error getting file metadata: {e}")

    @staticmethod
    def get_file_props(file_id: str) -> dict:
        try:
            file_metadata = Drive.__service.files().get( fileId=file_id, fields='properties', supportsAllDrives=True ).execute()
            return file_metadata.get('properties')
        except Exception as e:
            Log.error(f"Error getting file properties: {e}")

    @staticmethod
    def get_file_list(file_name:str, folder_id:str, drive_id: str=None, mime_type: str=None) -> list:
        mime_type = mime_type or Drive.JSON
        try:
            query = f"name contains '{file_name}' and parents in '{folder_id}' and trashed=false"
            if drive_id: query += f" and '{drive_id}' in parents"
            files_list = []
            page_token = None
            while True:
                response = Drive.__service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size)',
                    pageToken=page_token,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True
                ).execute()
                files_list.extend(response.get('files', []))
                page_token = response.get('nextPageToken')
                if not page_token: break
            return files_list
        except Exception as e:
            Log.error(f"Error getting file list: {e}")

    @staticmethod
    def delete_file(file_id: str):
        try:
            Drive.__service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
            Log.info(f"File {file_id} deleted.")
        except Exception as e:
            Log.error(f"Error deleting file: {e}")

    @staticmethod
    def get_revisions_list(file_id: str, mime_type: str=None) -> list:
        mime_type = mime_type or Drive.JSON
        try:
            revisions_list = []
            page_token = None
            while True:
                response = Drive.__service.revisions().list(
                    fileId=file_id, 
                    fields='nextPageToken, revisions(id, mimeType, modifiedTime)',
                    pageToken=page_token,
                    supportsAllDrives=True
                ).execute()
                revisions_list.extend(response.get('revisions', []))
                page_token = response.get('nextPageToken')
                if not page_token: break
            return revisions_list
        except Exception as e:
            Log.error(f"Error getting revisions list: {e}")
        
    @staticmethod
    def get_revision(revision_id: str, file_id: str, mime_type: str=None) -> FileMeta:
        mime_type = mime_type or Drive.JSON
        try:
            file_metadata = Drive.__service.files().get( fileId=file_id, revisionId=revision_id, alt='media', supportsAllDrives=True ).execute()
            return file_metadata
        except Exception as e:
            Log.error(f"Error getting file revision: {e}")
    
#--------------------------------- Image ---------------------------------#

    @staticmethod
    def get_image_blob(file_id: str) -> bytes:
        '''Получить Blob изображения по URL'''
        blob = Drive.__service.files().get_media(fileId=file_id).execute()
        return blob

    @staticmethod
    def jpeg_uri(image_data: str) -> str:
        '''Преобразовать изображение в URI'''
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_image}"

    @staticmethod
    def jpeg_size(image_data: str) -> tuple:  
        '''Получить метаданные изображения (размер и т.п.)'''
        image = Image.open(io.BytesIO(image_data))
        return (image.width, image.height)

    @staticmethod
    def card_image(image_uri: str, title: str, url: str) -> ImageInfo:
        '''Вставить изображение в карточку (в веб-интерфейсе, например)'''
        return {
            'title': title,
            'imageUrl': image_uri,
            'altText': title,
            'openLink': url
        }