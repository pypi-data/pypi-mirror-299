from antbase._.server_drive.drive import Drive
from antbase._.server_drive.f import F

file_id    = F.track_sheet
file_name  = "Track"
folder_id  = "1xxzJJ9weM6k48q1VRlMLhI9VLD0I3j5u"

# Get file name
file_name = Drive.get_file_name(file_id)
print(f"File name: {file_name}")

# Get file list
files_list = Drive.get_file_list("track", folder_id, mime_type=Drive.SHEET)
for file in files_list:
    print(f" - File: {file['name']}, ID: {file['id']}, MimeType: {file['mimeType']}")

# Create an empty file
file_id = Drive.create_file_empty("testDrive.json", folder_id)
print(f"New file ID: {file_id}")

# Update file metadata
Drive.update_file_metadata(file_id, name="renamedTestDrive.json")

# Get file metadata
file_metadata = Drive.get_file_metadata(file_id)
print(f"File metadata: {file_metadata}")

# Delete a file
Drive.delete_file(file_id)

in_folderId   = F.p_ph
out_folderId  = F.orderPhoto
in_driveId    = F.GOOGLE_DRIVE
out_driveId   = F.ANT_DRIVE
fileName      = "p6638ph"
orderId       = "p6638"

files  = Drive.get_file_list(fileName, in_folderId, mime_type=Drive.IMAGE)
fileId = files[0].id