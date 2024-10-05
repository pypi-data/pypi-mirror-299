# Base templates for Synology log analysis

process_start_or_stop = (
    "{time} {server_name} System: System successfully {result} [{process}]."
)

backup_task = (
    "{time} {server_name} Backup SYSTEM:#011[{type}][{task_name}] Backup task {state}."
)

multi_backup_task = "{time} {server_name} Backup SYSTEM:#011[{type}][{task_name}] Backup task {state}. [{files_scanned} files scanned] [{new_files} new files] [{files_modified} files modified] [{files_unchanged} files unchanged]"
version_rotation = (
    "{time} {server_name} Backup SYSTEM:#011[{task_name}] Trigger version rotation."
)

integrity_check = "{time} {server_name} Backup SYSTEM:#011[{type}][{task_name}] Backup integrity {result}."

scrubbing = "{time} {server_name} System SYSTEM:#011System {state} {type} scrubbing on [{location}]."

login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged in successfully via [{method}]."
failed_login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to log in via [{method}] due to authorization failure."

logout = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged out the server via [{method}] with totally [{data_uploaded}] uploaded and [{data_downloaded}] downloaded."

sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] signed in to [{service}] successfully via [{auth_method}]."
failed_sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to sign in to [{service}] via [{auth_method}] due to authorization failure."

folder_access = "{time} {server_name} Connection: User [{user}] from [{client_ip}] via [{method}] accessed shared folder [{folder}]."

cleared_notifications = "{time} {server_name} System {system_user}:#011Cleared [{user}] all notifications successfully."

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string greatly increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

synology_template_dict = {
    "System successfully": [process_start_or_stop, 4, "process_start_or_stop"],
    "Backup SYSTEM:#011": [backup_task, 5, "backup_task"],
    "Backup task": [multi_backup_task, 9, "multi_backup_task"],
    "version rotation": [version_rotation, 3, "version_rotation"],
    "integrity check": [integrity_check, 5, "integrity_check"],
    "logged in successfully via": [login, 5, "login"],
    "failed to log in": [failed_login, 5, "failed_login"],
    "logged out the server": [logout, 7, "logout"],
    "accessed shared folder": [folder_access, 6, "folder_access"],
    "signed in to": [sign_in, 6, "sign_in"],
    "failed to sign in": [failed_sign_in, 6, "failed_sign_in"],
    "scrubbing": [scrubbing, 5, "scrubbing"],
    "Cleared": [cleared_notifications, 4, "cleared_notifications"],
}
