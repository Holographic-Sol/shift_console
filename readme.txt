--- shift_console ---

Short Description:
Updates Local Backup Files and Directories.
Can Be used to update a backup of steam instead of copying the entire steam directory.

The why?
Saves writes to disk.
Faster than copying everything in circumstances where modified files are unknown & or
saves hassle of manually going in and out of directories looking for files that need to be backed up.

Python Version: 3.9.2

Please ensure win32 long paths are enabled either inn registry or using gpedit.
    1. Run Gpedit.
    2. Computer Configuration -> Administrative Tolls -> System -> Filesystem -> Enable Win32 long paths.