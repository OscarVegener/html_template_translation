from bs4 import BeautifulSoup, Comment, Script
import re, os, shutil


def add_translate_tag_to_html(file_path, backup=False):
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        if backup:
            shutil.copyfile(file_path, file_path+".backup")

    texts = soup.findAll(text=lambda text: not isinstance(text, Script) and not isinstance(text, Comment))
    
    filtered_texts = [text for text in texts if not re.match(r'{%.*%}', text.string.strip()) and not re.match(r'{{.*}}', text.string.strip()) and text.string.strip()]
    for text in filtered_texts:
        text.replace_with(text.replace(text, "{{% translate '{}' %}}".format(text)))

    with open(file_path, 'w') as fp:
        fp.write(str(soup.prettify()))


def get_list_of_html_files(dir, file_list=[], recursive=False, subdirectories_only=".*"):
    entries = os.scandir(dir)
    pattern = '.*/{}/.*'.format(subdirectories_only)
    if recursive:
        for entry in entries:
            
            if entry.is_file() and entry.name.endswith(".html") and re.match(r'.*/templates/.*', entry.path):
                file_list.append(entry.path)
            elif entry.is_dir():
                get_list_of_html_files(entry, file_list=file_list, recursive=True)
    
        return file_list
    else:
        for entry in entries:
             if entry.is_file() and entry.name.endswith(".html"):
                file_list.append(entry.path)
        return file_list

def main(opt):
    if opt.logging:
        with open(opt.logging, "a") as file:
            file.truncate()
    if opt.subdirectoriesonly:
        subdirectories_only = opt.subdirectoriesonly
    else:
        subdirectories_only = ".*"
    lst = get_list_of_html_files(dir=opt.directory, recursive=opt.recursive, subdirectories_only=subdirectories_only)
    print("List of html files:")
    print("==========================================")
    for item in lst:
        print(item)
    print("==========================================")
    input()
    for item in lst:
        try:
            path = str(item).replace("//", "/")
            add_translate_tag_to_html(path, opt.backup)
        except Exception as e:
            print("Exception happened: {}. Item: {}".format(e, item))
            if opt.logging:
                with open(opt.logging, "a") as file:
                    file.write("Exception happened: {}\n. Item: {}\n".format(e, item))
            continue


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, help="Directory to look up html files", required=True)
    parser.add_argument('-r', '--recursive', help="Look for html files in subdirectories", action="store_true")
    parser.add_argument('-b', '--backup', help="Make backup of html files", action="store_true")
    parser.add_argument('-l', '--logging', type=str, help="Save exceptions to file")
    parser.add_argument('-s', '--subdirectoriesonly', type=str, help="Search for html files in specified subdirectories only")

    opt = parser.parse_args()
    main(opt)

