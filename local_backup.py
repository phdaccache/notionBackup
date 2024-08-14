import os
import zipfile
import shutil
import time

def make_backup():
    final_folder = "Notion_Backup"
    zip_dir = "." 
    extract_dir = "./" + final_folder

    for file_name in os.listdir(zip_dir): 
        if file_name.endswith(".zip"): 
            zip_file = os.path.join(zip_dir, file_name) 
            extract_zip(zip_file, extract_dir) 
            delete_file(zip_file)

    count = 0
    dic = {}

    # Files
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            if file.endswith(".html"):
                #if count == 0: original_name = file[:-38]
                id = file[-37:-5]
                if id not in dic:
                    dic[id] = count
                    count += 1

    # Folders
    for root, dirs, files in os.walk(zip_dir):
        for dir in dirs:
            if dir == final_folder: continue
            id = dir[-32:]
            if id not in dic:
                dic[id] = count
                count += 1
    
    # Files
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            if file.endswith(".html"):
                id = file[-37:-5]
                with open(os.path.join(root, file), "rt") as fin:
                    with open(os.path.join(root, str(dic[id])) + ".html", "wt") as fout:
                        for line in fin:
                            for key, value in dic.items():
                                f = get_substring(line, key)
                                if f is not None:
                                    f = f.replace(".html", "")
                                    line = line.replace(f, str(value))
                            fout.write(line)
                        os.remove(os.path.join(root, file))

    # Folders
    for root, dirs, files in os.walk(zip_dir, topdown=False):
        for dir in dirs:
            if dir == final_folder: continue
            id = dir[-32:]
            os.rename(os.path.join(root, dir), os.path.join(root, str(dic[id])))

def extract_zip(zip_file, extract_dir): 
    with zipfile.ZipFile(zip_file, 'r') as zip_ref: 
        zip_ref.extractall(extract_dir) 

def delete_file(file_path): 
    os.remove(file_path)

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