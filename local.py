import os
import zipfile
import shutil

def make_backup():

    # Function to extract a zip file 
    def extract_zip(zip_file, extract_dir): 
        with zipfile.ZipFile(zip_file, 'r') as zip_ref: 
            zip_ref.extractall(extract_dir) 
    
    # Function to delete a file 
    def delete_file(file_path): 
        os.remove(file_path) 
    
    # Directory containing the .zip files 
    zip_dir = '.' 
    
    # Directory to extract the contents of the .zip files 
    extract_dir = './Notion_Backup' 
    
    # Iterate over all files in the directory 
    for file_name in os.listdir(zip_dir): 
        if file_name.endswith('.zip'): 
            zip_file = os.path.join(zip_dir, file_name) 
            extract_zip(zip_file, extract_dir) 
            delete_file(zip_file) 

    count = 0
    files_paths = {}
    temp_id = "DhAH4r%)Im3<wX0u)BvXc6a~DjurHxKz41_IK$7zPEAfg6zX8ZS6{=!%7B,G#*!"

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                files_paths[file] = [root, str(count)]
                count += 1

    for file in files_paths:
        with open(files_paths[file][0]+"/"+file, "rt") as fin:
            with open(files_paths[file][0]+"/"+files_paths[file][1]+temp_id+".html", "wt") as fout:
                for line in fin:
                    for f in files_paths:
                        f2 = f.replace(" ", "%20")
                        f2 = f2.replace(".html", "")
                        line = line.replace(f2, files_paths[f][1]+temp_id)
                    fout.write(line)
                os.remove(files_paths[file][0]+"/"+file)

    count = 0
    for file in files_paths:
        with open(files_paths[file][0]+"/"+str(count)+temp_id+".html", "rt") as fin:
            with open(files_paths[file][0]+"/"+"f"+files_paths[file][1]+".html", "wt") as fout:
                for line in fin:
                    fout.write(line.replace(temp_id, ""))
                os.remove(files_paths[file][0]+"/"+str(count)+temp_id+".html")
        count += 1

    rename_dic = {}
    new_dirs = {}

    for root, dirs, files in os.walk("."):
        for dir in dirs:
            file_of_dir = dir+".html"
            old_path = root + "/" + dir
            if file_of_dir in files_paths:
                new_name = str(files_paths[file_of_dir][1])
            else:
                new_name = str(count)
                count += 1
                new_dirs[root] = [dir, new_name]
            new_path = root + "/" + new_name
            rename_dic[old_path] = new_path

    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith(".html"):
                continue
            with open(root+"/"+file, "rt") as fin:
                with open(root+"/"+file[1:], "wt") as fout:
                    for line in fin:
                        for key, value in new_dirs.items():
                            f2 = value[0].replace(" ", "%20")
                            line = line.replace(f2, value[1])
                        fout.write(line)
                    os.remove(root+"/"+file)

    for key, value in dict(reversed(list(rename_dic.items()))).items():
        os.rename(os.path.join("", key), value)

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                os.rename(os.path.join("", root), "Notion_Backup")

    shutil.make_archive("Notion_Backup", 'zip', ".")

make_backup()