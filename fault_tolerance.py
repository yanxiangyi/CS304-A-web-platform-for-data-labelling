def ft_algo(ans,nb_json, threshold,init_acc,nb_bel_ratio):
    print("threshold:{}  init_acc:{}, nb_bel_ratio{}".format(threshold, init_acc, nb_bel_ratio))

    if threshold ==0 :  #fault tolerance off
        answerset = []
        for a in ans:
            answerset.append(a[0])
        return answerset

    total = 0
    answers = []
    accset = []
    nb_bel = nb_bel_ratio*nb_json
    if len(ans)>1:
        # print('length: ')
        # print(len(ans))
        for i in ans:
            if i[1] not in answers :
                # print(i[1])
                if i[4] < nb_bel:
                    answers.append(i[1])
                    accset.append(init_acc)
                    total += init_acc
                else:
                    answers.append(i[1])
                    accset.append(i[3]/i[4])
                    total += i[3]/i[4]
            else:
                if i[4] <nb_bel:
                    accset[answers.index(i[1])] += init_acc
                    total += init_acc
                else:
                    accset[answers.index(i[1])] += i[3]/i[4]
                    total += i[3]/i[4]
        if (max(accset)/total) if total !=0 else 0 >= threshold:
            coranswer = answers[accset.index(max(accset))]
            answerset = []
            for an in ans:
                if an[1] == coranswer:
                    answerset.append(an[0])
            # print(total)
            # print(k/total)
            return answerset
    else :
        return None