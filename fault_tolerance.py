import database

def fault_tolerance():
    temp = 0
    total = 0
    answers = []
    conn = connection.MySQLConnection(user='root',
                                     password='se2018',
                                     host='127.0.0.1',
                                     database='se_proj')
    a = database.sql_conn(conn)
    ans = a.load_ft_data()
    if len(ans)>1 :
        for i in ans:
            if i[1] not in answers :
                if i[4] < 10:
                    answers.append((i[1], 0.5))
                    total += 0.5
                else:
                    answers.append((i[1], i[3]/i[4]))
                    total += i[3]/i[4]
            else:
                for j in range(0,len(answers)-1):
                    if answers[j] == i[1]:
                        temp = j
                        j = len(answers)
                if i[4] <10:
                    crd = answers[j][1] + 0.5
                else:
                    crd = answers[j][1]+ i[3]/i[4]
                answers[temp] = (i[1], crd)
                total += crd
        for k in range(0,len(answers)):
            if answers[k][1]/total > 0.8:
                coranswer = answers[k][0]
                answerset = []
                for an in ans:
                    if an[1] == coranswer:
                        answerset.append(an[0])
                return answerset
    else :
        return None
