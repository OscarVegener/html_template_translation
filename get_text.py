from bs4 import BeautifulSoup, Comment
import re, os


def get_strings_to_translate(file_path):
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    strings = soup.findAll(text=True)
    strings = [string.strip() for string in strings if not re.match(r'{%.*%}', r.string.strip()) and not re.match(r'{{.*}}', r.string.strip()) and r.string.strip()]
    return strings


def add_translate_tag_to_html(file_path):
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
    #     comments.extract()

    # elements = soup.findAll()
    # elements = [el for el in elements if el.string and el.name != "script"]

    # result_to_po_file = [r.string.strip() for r in elements if not re.match(r'{%.*%}', r.string.strip()) and not re.match(r'{{.*}}', r.string.strip()) and r.string.strip()]

    # for el in elements:
    #     el.string = '{{% translate "{}" %}}'.format(el.string)

    # str_html = "{% load i18n %}\n" + str(soup.prettify())

    # with open(file_path, 'w') as fp:
    #     fp.write(str_html)

    # return result_to_po_file

    texts = soup.findAll(text=True)
    for text in texts:
        print(text)


def get_list_of_html_files(dir, file_list=[]):
    entries = os.scandir(dir)
    for entry in entries:
        if entry.is_file() and entry.name.endswith(".html"):
            file_list.append(entry.path)
        elif entry.is_dir():
            get_list_of_html_files(entry, file_list=file_list)
    
    return file_list


def main(opt):
    # lst = get_list_of_html_files(opt.directory)
    # print("List of html files:")
    # print("==========================================")
    # for item in lst:
    #     print(item)
    # print("==========================================")
    # input()
    # po_text = ""
    # for item in lst:
    #     "".join(add_translate_tag_to_html(item))
    # print(po_text)
    add_translate_tag_to_html('user.html')
    # add_translate_tag_to_html('C:\\Users\\Oscar\\Desktop\\zchen2711-oms-97f3e7ffdd22\\OnlineShoppingSystem\\online_shopping_system\\users\\templates\\user.html')


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, help="Directory to look up html files", required=True)
    parser.add_argument('-r', '--recursive', help="Look for html files in subdirectories", action="store_true")
    parser.add_argument('-o', '--output_file', type=str, help="Path to output file")

    opt = parser.parse_args()
    main(opt)

