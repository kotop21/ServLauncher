import core.listeners.server

from .open_folder import OpenFolderListener
from .user_file_manager_listener import UserFileManagerListener
from .dialog import DialogListener

open_folder = OpenFolderListener()
user_file_manager = UserFileManagerListener()
dialog = DialogListener()
