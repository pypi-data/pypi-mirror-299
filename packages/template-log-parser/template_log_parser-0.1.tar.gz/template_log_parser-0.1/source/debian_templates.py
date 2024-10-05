# Base templates for Debian Type log analysis

anacron = "{time} {server_name} anacron[{anacron_id}]: {description}"

cleaning_up_disabled = "{time} {server_name} {service}: Cleaning up snapshots from shared folders has been disabled."

cpu_time = "{time} {server_name} systemd[{system_id}]: {service}: Consumed {cpu_time} CPU time."

cron_session_opened = "{time} {server_name} CRON[{cron_id}]: {type}: session opened for user {user}({user_id}) by ({by_user_id})"
cron_session_closed = (
    "{time} {server_name} CRON[{cron_id}]: {type}: session closed for user {user}"
)
cron_cmd = "{time} {server_name} CRON[{cron_id}]: ({user}) CMD {command}"

deleted = "{time} {server_name} {service}[{service_id}]: Deleted: {number_of_messages}"

rsync_receiving_file_list = (
    "{time} {server_name} rsyncd[{rsync_id}]: receiving file list"
)
rsync_building_file_list = "{time} {server_name} rsyncd[{rsync_id}]: building file list"
rsync_on = "{time} {server_name} rsyncd[{rsync_id}]: rsync on {path} from {client} ({client_ip})"
rsync_to = "{time} {server_name} rsyncd[{rsync_id}]: rsync to {path} from {client} ({client_ip})"
rsync_allowed = "{time} {server_name} rsyncd[{rsync_id}]: rsync allowed access on module {rsync_module} from {client} ({client_ip})"
rsync_name_failed = "{time} {server_name} rsyncd[{rsync_id}]: forward name lookup for {client} failed: Name or service not known"
rsync_connect = (
    "{time} {server_name} rsyncd[{rsync_id}]: connect from {client} ({client_ip})"
)
rsync_total_size = "{time} {server_name} rsyncd[{rsync_id}]: sent {sent} bytes  received {received} bytes  total size {total}"
rsync_syncing = "{time} {server_name} rsync-{rsync_task} Please wait, syncing {source} to {destination} ...{newline}"
rsync_synchronisation = (
    "{time} {server_name} rsync-{rsync_task} The synchronisation {result}"
)
rsync_sender = "{time} {server_name} rsyncd[{rsync_id}]: rsync: [sender] {action} {location} {module} {result}: {description}"


systemd_starting = "{time} {server_name} systemd[{systemd_id}]: Starting {service_name} - {description}"
systemd_started = (
    "{time} {server_name} systemd[{system_id}]: Started {service_name} - {description}"
)
systemd_stopping = "{time} {server_name} systemd[{systemd_id}]: Stopping {service_name} - {description}"
systemd_stopped = (
    "{time} {server_name} systemd[{system_id}]: Stopped {service_name} - {description}"
)
systemd_finished = "{time} {server_name} systemd[{systemd_id}]: Finished {service_name} - {description}"
systemd_deactivated = (
    "{time} {server_name} systemd[{systemd_id}]: {service_name}: Deactivated {result}."
)

apt_systemd_daily = "{time} {server_name} apt.systemd.daily[{apt_id}]: {description}"

warning = "{time} {server_name} {task}[{task_id}]:{service}warning: {description}"

smbd_registered = "{time} {server_name} smbd[{smbd_id}]:   Registered {message}"


# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

debian_template_dict = {
    "anacron[": [anacron, 4, "acron"],
    "building": [rsync_building_file_list, 3, "rsync_building_file_list"],
    "receiving": [rsync_receiving_file_list, 3, "rsync_receiving_file_list"],
    "Cleaning up": [cleaning_up_disabled, 3, "cleaning_up_disabled"],
    "CPU time": [cpu_time, 5, "cpu_time"],
    "Deleted": [deleted, 5, "deleted"],
    "session opened": [cron_session_opened, 7, "cron_session_opened"],
    "session closed": [cron_session_closed, 5, "cron_session_closed"],
    "synchronisation": [rsync_synchronisation, 4, "rsync_synchronisation"],
    "syncing": [rsync_syncing, 6, "rsync_syncing"],
    "rsync on": [rsync_on, 6, "rsync_on"],
    "rsync to": [rsync_to, 6, "rsync_to"],
    "rsync: [sender]": [rsync_sender, 8, "rsync_sender"],
    "rsync allowed": [rsync_allowed, 6, "rsync_allowed"],
    "forward name lookup": [rsync_name_failed, 4, "rsync_name_failed"],
    "total size": [rsync_total_size, 6, "rsync_data"],
    "connect from": [rsync_connect, 5, "rsync_connect"],
    "Starting": [systemd_starting, 5, "systemd_service_starting"],
    "Started": [systemd_started, 5, "systemd_service_started"],
    "Stopped": [systemd_stopped, 5, "system_service_stopped"],
    "Stopping": [systemd_stopping, 5, "systemd_service_stopping"],
    "Finished": [systemd_finished, 5, "systemd_service_finished"],
    "Deactivated": [systemd_deactivated, 5, "systemd_service_deactivated"],
    "CMD": [cron_cmd, 5, "cron_cmd"],
    "apt.systemd.daily[": [apt_systemd_daily, 4, "apt_systemd_daily"],
    "warning": [warning, 6, "warning"],
    'Registered': [smbd_registered, 4, 'smbd_registered'],
}
