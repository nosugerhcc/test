import os

def get_csv_file(path,keyword):
    file_lists=[]
    file_list=[x for x in os.listdir(path)]
    for i in range(len(file_list)):
        file_name=os.path.split(os.path.join(path,file_list[i]))[1]
        if file_name.find(keyword)!=-1:
            file_lists.append(os.path.join(path,file_list[i]))
    return file_lists

