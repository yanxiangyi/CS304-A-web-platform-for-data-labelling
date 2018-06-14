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
    nb_bel = 100*nb_bel_ratio*nb_json
    print("lenth of ans: {} number_belief: {}".format(len(ans),nb_bel))
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
                    print("new answer detect||use init belief, total = {}".format(total))
                else:
                    answers.append(i[1])
                    accset.append(float(i[3])/float(i[4]))
                    total += float(i[3])/float(i[4])
                    print("new answer detect||use user belief, total = {}".format(total))
            else:
                if i[4] <nb_bel:
                    accset[answers.index(i[1])] += init_acc
                    total += init_acc
                    print("hit old answer || use init belief, total = {}".format(total))
                else:
                    accset[answers.index(i[1])] += float(i[3])/float(i[4])
                    total += float(i[3])/float(i[4])
                    print("hit old answer || use user belief, total = {}".format(total))
        if total ==0:
            return None
        if (float(max(accset))/float(total)) >= threshold:
            print("find answer ")
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