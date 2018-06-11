#coding=utf-8


def fault_tolerance(ans):
    total = 0
    answers = []
    accset = []
    if len(ans)>1 :
        # print('length: ')
        # print(len(ans))
        for i in ans:
            if i[1] not in answers :
                # print(i[1])
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
                coranswer = answers[accset.index(k)]
                answerset = []
                for an in ans:
                    if an[1] == coranswer:
                        answerset.append(an[0])
                # print(total)
                # print(k/total)
                return answerset
    else :
        return None
#
# if __name__ == '__main__':
#     ans= [(81, '1', 1, 15, 15),(66, '1', 2, 2, 3),(60, '1', 3, 0, 0),(65, '1', 17, 0, 0),(70, '1', 18, 0, 0),(76, '1', 19, 0, 5),(73, '[``, [`开心`, `满意`], []]', 26, 0, 0)]
#     print(fault_tolerance(ans))