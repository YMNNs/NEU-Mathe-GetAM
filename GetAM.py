from mysql.connector import connect

interval = 0  # 下载图片的间隔
question_match = "colspan='3'"  # 题干所在行的特征（横跨三列）
choice_match_half = "<td align='center'><input type='radio' name='%d'"  # 用于匹配选项的前半部分
paper_id_match = '<input type="hidden" id="id"'  # 试卷id所在行特征


def get_answer_by_sql(question_ids, list_html):
    j = 1
    answers_list = []
    conn = connect(host="localhost", user="root", passwd="password", database="gs")
    cursor = conn.cursor()
    for question_id in question_ids:
        cursor.execute('SELECT `ans`,`ansurl` FROM `main` WHERE `sub` = \'%s\'' % question_id)
        result = cursor.fetchall()
        if not result:
            answers_list.append('?')
            j += 1
        else:
            answers_list.append(result[0][0])
            j += 1
    cursor.close()
    conn.close()
    max_questions = len(question_ids)

    key_list = []
    j = 0
    current_question = 0
    while j < len(list_html) and current_question < max_questions:
        if choice_match_half % (current_question + 1) in list_html[j]:
            if list_html[j].split("'")[-2] == answers_list[current_question]:
                key_list.append('A')
                j += 9
            elif list_html[j + 2].split("'")[-2] == answers_list[current_question]:
                key_list.append('B')
                j += 7
            elif list_html[j + 6].split("'")[-2] == answers_list[current_question]:
                key_list.append('C')
                j += 3
            elif list_html[j + 8].split("'")[-2] == answers_list[current_question]:
                key_list.append('D')
                j += 1
            else:
                key_list.append('?')
                j += 9
            current_question += 1
        else:
            j += 1
    if len(key_list) > 0:
        print('[INFO] 数据库中的答案')
        print('总题量：', max_questions)
        count = 0
        for temp in key_list:
            count += 1
            print(temp, end='')
            if count % 5 == 0:
                print()

    else:
        print('[WARNING] 未在数据库中找到答案')


def parse_line(html_line):
    question_id = html_line.split('_')[-2]
    chapter_id = html_line.split('_')[-4].split('/')[-1]
    return [chapter_id, question_id]


def main():
    with open('questions.html', 'r', encoding='UTF-8') as file_html:
        list_html = file_html.readlines()
    question_ids = []
    question_number = 0
    paper_id = ''
    for line in list_html:
        if question_match in line:
            question_number += 1
            question_ids.append(parse_line(line)[1])
        elif paper_id_match in line:
            paper_id = line.split('"')[-2]

    get_answer_by_sql(question_ids, list_html)


if __name__ == '__main__':
    main()
    # 如果出现“本次考试操作异常n次”，在console中运行如下代码
    # function monitor(){return;}
