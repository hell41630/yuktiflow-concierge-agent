from googleapiclient.discovery import build
from google.oauth2 import service_account

class DriveTool:
    """
    Real Google Drive tool using a service account.
    Reads only files shared with the service account.
    """
    def __init__(self, creds_path="secrets/service_account.json"):
        scopes = ["https://www.googleapis.com/auth/drive.readonly"]
        self.creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=scopes
        )
        self.service = build("drive", "v3", credentials=self.creds, cache_discovery=False)

    def list_docs(self, folder_id=None):
        q = None
        if folder_id:
            q = f"'{folder_id}' in parents"
        result = self.service.files().list(
            q=q,
            fields="files(id, name, mimeType)"
        ).execute()
        return result.get("files", [])

    def download_text(self, file_id):
        file = self.service.files().get(fileId=file_id).execute()
        mime = file.get("mimeType")

        if mime == "application/vnd.google-apps.document":
            resp = self.service.files().export(
                fileId=file_id,
                mimeType="text/plain"
            ).execute()
            return resp.decode("utf-8")

        from googleapiclient.http import MediaIoBaseDownload
        import io

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        return fh.getvalue().decode("utf-8")
