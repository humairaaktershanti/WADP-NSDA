# First Class

<details>
<summary><b>Start with Django</b></summary>


Django is a high-level Python web framework. We can do everything using CMD.

+ First Install Python. Because Django is a pthon framework. Here we do everything using python.
+ Create a Root Folder. In this folder we do django related every work.
+ Open Folder and click the folder path. To open command prompt type 'cmd' and press entry.
+ We need to Create a Virtual Environment. Virtual Environent allows for isolating project dependencies, ensuring version control, resolving conflicts, maintaining a clean development environment.
  ```cmd
  python -m venv foldername
  ```
+ After create the virtual environment then activate the virtual environment.
  ```cmd
  .\foldername\Scripts\activate
  ```
+ After activate, Install Django.
  ```cmd
  pip install django
  ```
+ Create a Django project  under the root folder.
  ```cmd
  django-admin startporject projectname
  ```
+ After create project install some django files and folder. Then entry the project folder.
  ```cmd
  cd projectname
  ```
+ Run Django project server
  ```cmd
  python manage.py runserver
  ```
After run the server create a local server url. Copy url and paste on any browser. After paste if open this then server run properly.

![image](../images/runserver.png)

</details>

# Home Work

### <b>Command Prompt (cmd) command list:</b>

+ `cd: ` It is used to change the current directory

  ```cmd
  cd [directory_path]
  ```
+ `mkdir:` Used to create a new directory

  ```cmd
  mkdir [directory_path]
  ```
+ `dir:` Used to list all files and directories in a specific directory
  ```cmd
  dir [directory_path]
  ```
+ `rmdir:` Used to remove a directory
  ```cmd
  rmdir [directory_name]
  ```
+ `echo:` Used to create file
  ```cmd
  echo. > filename.extension
  ```
+ `del:` Used to remove one or more files
  ```cmd
  del file_name
  ```
+ `copy:` Used to copy files
  ```cmd
  copy [source_file] [destination]
  ```
+ `move:`  Moves one or more files from one directory to another.
  ```cmd
  move [source_file] [destination]
  ```
+ `rename:` Used to change file name
  ```cmd
  rename [old_file_name] [new_file_name]
  ```
+ `type:` Displays the contents of a file.
  ```cmd
  type filename.extension
  ```
+ `ping:` Used to test the network connection
  ```cmd
  ping Ip _address
  ```
+ `ipconfig:` Displays IP configuration for all network adapters.
  ```cmd
  ipconfig
  ```
+ `tasklist:` Display a list of the current running process.
  ```cmd
  tasklist
  ```
+ `taskkill:` Terminates a running process.
  ```cmd
  taskkill /pid [typepid]
  ```
+ `cls:` This command will clear the command prompt console.
  ```cmd
  cls
  ```
+ `hostname:` This windows command displays the host name of the computer.
  ```cmd
  hostname
  ```
+ `chdir:` Displays the name of the current directory
  ```cmd
  chdir
  ```
+ `color:` Sets the default console foreground and background colors.
  ```cmd
  color [background][foreground]
  ```
+ `comp:` Compares the contents of two files or sets of files.
  ```cmd
  comp [file1] [file2]
  ```
+ `date:` Displays or sets the system date.
  ```cmd
  date
  ```
+ `exit:`Used to close the Command Prompt window or terminate the currently running script or batch file. 
  
  ```cmd
  exit
  ```
+ `fc:` Compares two files or sets of files, and displays the differences between them.
  ```cmd
  fc [file] [file2]
  ```
+ `erase:` Deletes one or more files.
  ```cmd
  erase [file1][file2][....]
  ```
