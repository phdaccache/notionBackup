import os
import zipfile
import shutil
import time

def make_backup():
    final_folder = "Notion_Backup"
    zip_dir = "." 
    extract_dir = "./" + final_folder

    # Extracting zip file
    for file_name in os.listdir(zip_dir): 
        if file_name.endswith(".zip"): 
            zip_file = os.path.join(zip_dir, file_name) 
            extract_zip(zip_file, extract_dir) 
            delete_file(zip_file)

    count = 0
    dic = {}

    # Files: getting id and giving it a new name (count)
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            if file.endswith(".html"): # we don't need to change any other file (line .png)
                id = file[-37:-5] # the id is always a string with 32 numbers, and the last 5 are '.html'
                if id not in dic:
                    dic[id] = count
                    count += 1

    # Folders: getting id and giving it a new name (count)
    for root, dirs, files in os.walk(zip_dir):
        for dir in dirs:
            if root.find(extract_dir) == -1: continue # if the dir being looked is outside of ./Notion_Backup
            if dir == final_folder: continue # if the dir is Notion_Backup, we don't change its name
            id = dir[-32:] # the id is always a string with 32 numbers, and dirs don't end with '.html'
            if id not in dic: # a dir may have the same id as its corresponding file
                dic[id] = count
                count += 1
    
    # Files: changing all the references of the previous names with the new names (count)
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            if file.endswith(".html"):
                id = file[-37:-5]
                with open(os.path.join(root, file), "rt") as fin: # old file
                    with open(os.path.join(root, str(dic[id])) + ".html", "wt") as fout: # new file
                        for line in fin: # iterating over every line in the file
                            for key, value in dic.items(): # key = id, value = count
                                f = get_substring(line, key) # get the complete file name with an certain id
                                if f is not None: # not every line will have every file referenced
                                    f = f.replace(".html", "") # we want to change dirs too
                                    line = line.replace(f, str(value))
                            fout.write(line)
                        os.remove(os.path.join(root, file)) # remove the old file

    # Folders
    for root, dirs, files in os.walk(zip_dir, topdown=False): # iterate from inside out to avoid crash
        for dir in dirs:
            if root.find(extract_dir) == -1: continue
            if dir == final_folder: continue
            id = dir[-32:]
            os.rename(os.path.join(root, dir), os.path.join(root, str(dic[id])))

def extract_zip(zip_file, extract_dir): 
    with zipfile.ZipFile(zip_file, 'r') as zip_ref: 
        zip_ref.extractall(extract_dir) 

def delete_file(file_path): 
    os.remove(file_path)

# gets the substring with a given id isolated by the closest left and right delimiters
def get_substring_containing_id(line, id, left_delimiter, right_delimiter):
    start_index = line.find(id)
    if start_index == -1:
        return None
  
    left_delim_index = line.rfind(left_delimiter, 0, start_index)
    right_delim_index = line.find(right_delimiter, start_index + len(id))

    left_delim_index += len(left_delimiter)
    
    return line[left_delim_index:right_delim_index]

def get_shortest_string(*strings):
    non_none_strings = [s for s in strings if s is not None]

    if not non_none_strings:
        return None

    return min(non_none_strings, key=len)

# tests every option to see which is the shortest (the correct one)
def get_substring(line, id):
    left_delimiter1 = '"'
    left_delimiter2 = '/'
    right_delimiter1 = '"'
    right_delimiter2 = '/'
    f1 = get_substring_containing_id(line,id,left_delimiter1, right_delimiter1)
    f2 = get_substring_containing_id(line,id,left_delimiter1, right_delimiter2)
    f3 = get_substring_containing_id(line,id,left_delimiter2, right_delimiter1)
    f4 = get_substring_containing_id(line,id,left_delimiter2, right_delimiter2)
    return get_shortest_string(f1,f2,f3,f4)

def zip_folder():
    shutil.make_archive("Notion_Backup", 'zip', "./Notion_Backup")

def time_function(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours >= 1:
        formatted_time = f"Took {int(hours)}h {int(minutes)}m {seconds:.1f}s."
    elif minutes >= 1:
        formatted_time = f"Took {int(minutes)}m {seconds:.1f}s."
    else:
        formatted_time = f"Took {seconds:.1f}s."
    
    return formatted_time, result


print("Make sure your folder looks like this:")
print("Your Folder")
print("  |-- NotionsBackup.zip")
print("  |-- backup.py")
print("Start backup? (y/n)", end = " ")
i = input()

if i in ("y","Y"):
    print("Making backup...")
    t, _ = time_function(make_backup)
    print("")
    print("Backup Completed!", end = " ")
    print(t)
    print("")
    print("Would you like to zip the folder? (y/n)", end = " ")
    i2 = input()

    if i2 in ("y","Y"):
        print("Zipping...")
        t2,_ = time_function(zip_folder)
        print("")
        print("Folder zipped!", end = " ")
        print(t)