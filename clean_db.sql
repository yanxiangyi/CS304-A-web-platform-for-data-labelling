use se_proj;
update text_data set final_labelid = NULL where  dataid>0;
update users set nb_answer =0 where userid>0;
update users set nb_accept =0 where userid>0;
update users set credits =0 where userid>0;
DELETE FROM text_label where labelid>0;
update source set nb_finished = 0 where sourceid>0;
