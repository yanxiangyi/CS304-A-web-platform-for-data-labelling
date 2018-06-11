import database

def fault_tolerance(ans):
    total = 0
    answers = []
    accset = []
    # conn = connection.MySQLConnection(user='root',
    #                                  password='se2018',
    #                                  host='127.0.0.1',
    #                                  database='se_proj')
    # a = database.sql_conn(conn)
    # ans = a.load_ft_data()
    if len(ans)>1 :
        for i in ans:
            if i[1] not in answers :
                if i[4] < 10:
                    answers.append(i[1])
                    accset.append(0.5)
                    total += 0.5
                else:
                    answers.append(i[1])
                    accset.append(i[3]/i[4])
                    total += i[3]/i[4]
            else:
                if i[4] <10:
                    accset[answers.index(i[1])] += 0.5
                    total += 0.5
                else:
                    accset[answers.index(i[1])] += i[3]/i[4]
                    total += i[3]/i[4]
        for k in accset:
            if k/total >= 0.8:
                coranswer = k
                answerset = []
                for an in ans:
                    if an[1] == coranswer:
                        answerset.append(an[0])
                return answerset
    else :
        return None
