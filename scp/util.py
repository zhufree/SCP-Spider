import csv
import sqlite3
import os

csv.field_size_limit(100000000)


def merge_files(file_name_list, file_prefix='other'):
    """
    merge several csv files
    :param file_name_list:
    :param file_prefix:
    :return:
    """
    append_str = ''
    for i in range(0, len(file_name_list)):
        with open(file_name_list[i], 'r+', encoding='utf-8') as f:
            next(f)
            append_str += f.read()
    with open(file_prefix + '-merge.csv', 'w+', encoding='utf-8') as f:
        f.write(append_str)


def merge_all_file(dir_name, file_prefix='other'):
    """
    merge all files in a dir
    :return:
    """
    files = [dir_name + name for name in os.listdir(dir_name)]
    print(files)
    merge_files(files, file_prefix)  # 31m


def get_scp_from_file(filename):
    """
    read other list from csv file
    :param filename:
    :return:
    """
    with open(filename, 'r', encoding='utf-8', newline='') as f:
        # 统一header，方便后续合并文件一起上传
        reader = csv.DictReader(f)
        category_list = [dict(order_dict) for order_dict in reader]
        return category_list


def write_to_csv(article_list, file_name):
    """
    write a other dict list to csv file, deprecated now because of db export csv
    :param article_list:
    :param file_name:
    :return:
    """
    with open(file_name, 'w+', encoding='utf-8', newline='') as f:
        # 统一header，方便后续合并文件一起上传
        writer = csv.DictWriter(f, ['link', 'title', 'scp_type', 'download_type', 'detail', 'cn', 'not_found', \
                                    'author', 'desc', 'snippet', 'subtext', 'contest_name', 'contest_link', \
                                    'created_time', 'month', 'event_type', 'page_code', 'tags'])
        writer.writeheader()
        writer.writerows(article_list)


def write_sub_cate_to_csv(sub_cate_list, filename):
    """
    write a other list item (like settings) dict list to csv file, deprecated now because of db export csv
    :param sub_cate_list:
    :param filename:
    :return:
    """
    with open(filename, 'w+', encoding='utf-8', newline='') as f:
        # 统一header，方便后续合并文件一起上传
        writer = csv.DictWriter(f, ['link', 'title', 'scp_type', 'detail', 'cn', 'not_found',
                                    'author', 'desc', 'snippet', 'subtext', 'tags', 'sub_scps'])
        writer.writeheader()
        writer.writerows(sub_cate_list)


def split_csv_file():
    """
    split a big csv file to several file for upload to bmob
    :return:
    """
    all_scp = get_scp_from_file('other.csv')
    # 4000一组
    for i in range(0, 2):
        if i * 6000 + 6000 > len(all_scp):
            scp_group = all_scp[i * 6000:]
        else:
            scp_group = all_scp[i * 6000: i * 6000 + 6000]
        write_to_csv(scp_group, "other-split-" + str(i) + '.csv')


def update_tag_by_db(filename, db_filename):
    """
    update other tags from tags table in db
    :param filename:
    :param db_filename:
    :return:
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    tag_article_list = get_scp_from_file(filename)
    print(len(tag_article_list))
    for article in tag_article_list:
        # del article['story_num']
        # del article['number']
        cur.execute('''select tags from tag_scp where link = ?''', (article['link'],))
        for row in cur:
            if row[0] is not None:
                article['tags'] = row[0]
    write_to_csv(tag_article_list, filename)
    # write_sub_cate_to_csv(tag_article_list, filename)


def write_to_db(filename, db_filename):
    """
    write other list from csv to db, deprecated now.
    :param filename:
    :return:
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    scp_list = get_scp_from_file(filename)
    print(len(scp_list))
    for scp in scp_list:
        cur.execute('''insert into scps values (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (scp['title'], scp['link'], scp['detail'], scp['download_type'], scp['scp_type'],
                     scp['cn'], scp['not_found'], scp['author'], scp['desc'], scp['snippet'], scp['subtext'],
                     scp['contest_name'], scp['contest_link'], scp['created_time'], scp['month'],
                     scp['event_type'], scp['page_code'], scp['tags'],))

    con.commit()
    con.close()

