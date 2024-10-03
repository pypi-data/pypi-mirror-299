import hashlib
import os.path
import shutil
import stat
from pathlib import Path


class FileOp:
    @staticmethod
    def create_file_dir(file_path):
        parent_dir = str(Path(file_path).parent)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

    @staticmethod
    def make_dir(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def copy_file(source, destination):
        FileOp.create_file_dir(destination)
        shutil.copy2(source, destination)

    @staticmethod
    def move_file(source, destination):
        FileOp.create_file_dir(destination)
        shutil.move(source, destination)

    @staticmethod
    def dir_exists(dir_path):
        if os.path.exists(dir_path):
            return True
        return False

    @staticmethod
    def file_exists(file_path):
        if os.path.exists(file_path):
            return True
        return False

    @staticmethod
    def remove_dir(dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, onerror=FileOp.remove_readonly)
            return True
        return False

    @staticmethod
    def remove_readonly(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise exc_info[1]

    @staticmethod
    def remove_file(file_path):
        if FileOp.file_exists(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def convert_unit(size_in_bytes, unit):
        """ Convert the size from bytes to other units like KB, MB or GB"""
        if unit == "KB":
            return size_in_bytes / 1024
        elif unit == "MB":
            return size_in_bytes / (1024 * 1024)
        elif unit == "GB":
            return size_in_bytes / (1024 * 1024 * 1024)
        else:
            return size_in_bytes

    @staticmethod
    def get_file_size(file_name, size_type="MB"):
        """ Get file in size in given unit like KB, MB or GB"""
        try:
            size = os.path.getsize(file_name)
        except Exception as e:
            size = 0
            print("Exception occurred while calculating file size: " + str(e))
        return FileOp.convert_unit(size, size_type)

    @staticmethod
    def get_dir_list(file_path):
        return_list = []
        dir_list = ""
        file_path = str(file_path.replace("___", "/")).replace("\\", "/")
        for path in str(file_path).split("/"):
            dir_list = str(dir_list) + "/" + path
            if not str(dir_list).__eq__("/") \
                    and not str(dir_list).__contains__(".") \
                    and not str(dir_list).endswith("/system") \
                    and not str(dir_list).endswith("/product") \
                    and not str(dir_list).endswith("/etc") \
                    and not str(dir_list).endswith("/framework") \
                    and not str(dir_list).startswith("/usr/srec/en-US/") \
                    and not str(dir_list).endswith("system_ext_seapp_contexts") \
                    and not str(dir_list).endswith("/priv-app"):
                return_list.append(dir_list[1:])
        return return_list

    @staticmethod
    def read_priv_app_temp_file(file_path, encoding='cp437'):
        return_list = []
        if FileOp.file_exists(file_path):
            file = open(file_path, encoding=encoding)
            text = file.readlines()
            for line in text:
                if line.startswith("uses-permission:"):
                    try:
                        permissions = line.split('\'')
                        if permissions.__len__() > 1:
                            return_list.append(permissions[1])
                    except Exception as e:
                        return_list = ["Exception: " + str(e)]
            file.close()
            FileOp.remove_file(file_path)
        else:
            return_list.append("Exception: " + str(1001))
        return return_list

    @staticmethod
    def read_package_name(file_path, encoding='cp437'):
        if FileOp.file_exists(file_path):
            file = open(file_path, encoding=encoding)
            text = file.readline()
            if text.startswith("package:"):
                index1 = text.find("'")
                if index1 == -1:
                    text = text.replace("package:", "").strip()
                else:
                    text = text[index1 + 1: -1]
                    index1 = text.find("'")
                    text = text[0: index1]
            file.close()
            FileOp.remove_file(file_path)
        else:
            text = "Exception: " + str(1001)
        return text

    @staticmethod
    def read_package_version(file_path, encoding='cp437'):
        if FileOp.file_exists(file_path):
            file = open(file_path, encoding=encoding)
            text = file.readline()
            if text.__contains__("versionName="):
                index1 = text.find("versionName='")
                text = text[index1 + 13: -1]
                index1 = text.find("'")
                text = text[0: index1]
            file.close()
            FileOp.remove_file(file_path)
        else:
            text = "Exception: " + str(1001)
        return text

    @staticmethod
    def read_key(file_path, key, encoding='cp437'):
        if FileOp.file_exists(file_path):
            file = open(file_path, encoding=encoding)
            text = file.readline()
            if text.__contains__(f"{key}="):
                index1 = text.find(f"{key}='")
                text = text[index1 + len(key) + 2: -1]
                index1 = text.find("'")
                text = text[0: index1]
            file.close()
            FileOp.remove_file(file_path)
        else:
            text = "Exception: " + str(1001)
        return text

    @staticmethod
    def write_string_file(str_data, file_path):
        FileOp.create_file_dir(file_path)
        if FileOp.file_exists(file_path):
            os.remove(file_path)
        file = open(file_path, "w")
        file.write(str_data)
        file.close()

    @staticmethod
    def convert_to_lf(filename):
        with open(filename, 'r', newline='\n', encoding='utf-8') as file:
            content = file.read()
        content = content.replace('\r\n', '\n')
        with open(filename, 'w', newline='\n', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def write_string_in_lf_file(str_data, file_path):
        FileOp.create_file_dir(file_path)
        if FileOp.file_exists(file_path):
            os.remove(file_path)
        file = open(file_path, "w", newline='\n')
        file.write(str_data)
        file.close()

    @staticmethod
    def read_string_file(file_path):
        if FileOp.file_exists(file_path):
            file = open(file_path, "r", encoding='cp437')
            lines = file.readlines()
            file.close()
            return lines
        else:
            print("File: " + file_path + " not found!")
            return ['File Not Found']

    @staticmethod
    def read_binary_file(file_path):
        if FileOp.file_exists(file_path):
            file = open(file_path, "rb")
            lines = file.readlines()
            file.close()
            return lines
        else:
            print("File: " + file_path + " not found!")
            return ['File Not Found']

    @staticmethod
    def get_md5(file_path):
        if FileOp.file_exists(file_path):
            md5_hash = hashlib.md5()
            a_file = open(file_path, "rb")
            content = a_file.read()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            a_file.close()
            return digest
        else:
            return "File Not Found"
