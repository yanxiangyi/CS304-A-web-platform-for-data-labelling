jQuery(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/data',
        success: function (json){
        for (let i = 0; i < json.message.length; i++){
            jsonObject = json.message;
            jsdata = jsonObject[i];
            jsdataTask=jsdata.task;

            var questionDiv = document.createElement("div"); 
            questionDiv.setAttribute("id", "question_wrapper" + i);
            questionDiv.className = "m-content";
            document.getElementById("for_loop_wrapper").appendChild(questionDiv);

            var m_portlet_bordered_semi_Div = document.createElement("div"); 
            m_portlet_bordered_semi_Div.setAttribute("id", "m_portlet_bordered_semi_Div" + i);
            m_portlet_bordered_semi_Div.className = "m-portlet m-portlet--creative m-portlet--first m-portlet--bordered-semi";
            document.getElementById("question_wrapper" + i).appendChild(m_portlet_bordered_semi_Div);

            var m_portlet_head_Div = document.createElement("div"); 
            m_portlet_head_Div.setAttribute("id", "m_portlet_head_Div" + i);
            m_portlet_head_Div.className = "m-portlet__head";
            document.getElementById("m_portlet_bordered_semi_Div" + i).appendChild(m_portlet_head_Div);

            var m_portlet_head_caption_Div = document.createElement("div"); 
            m_portlet_head_caption_Div.setAttribute("id", "m_portlet_head_caption_Div" + i);
            m_portlet_head_caption_Div.className = "m-portlet__head-caption";
            document.getElementById("m_portlet_head_Div" + i).appendChild(m_portlet_head_caption_Div);

            var m_portlet_head_title_Div = document.createElement("div"); 
            m_portlet_head_title_Div.setAttribute("id", "m_portlet_head_title_Div" + i);
            m_portlet_head_title_Div.className = "m-portlet__head-title";
            document.getElementById("m_portlet_head_caption_Div" + i).appendChild(m_portlet_head_title_Div);

            var projectNameWrapper = document.createElement("h3"); 
            projectNameWrapper.appendChild(document.createTextNode(jsdata.projectName));  //change to real name
            // projectNameWrapper.setAttribute("id", "projectNameWrapper" + i);
            projectNameWrapper.className = "m-portlet__head-text";
            document.getElementById("m_portlet_head_title_Div" + i).appendChild(projectNameWrapper);

            var m_portlet_head_label_info_Div = document.createElement("h2"); 
            m_portlet_head_label_info_Div.setAttribute("id", "m_portlet_head_label_info_Div" + i);
            m_portlet_head_label_info_Div.className = "m-portlet__head-label m-portlet__head-label--info";
            document.getElementById("m_portlet_head_title_Div" + i).appendChild(m_portlet_head_label_info_Div);

            var questionNumberWrapper = document.createElement("span"); 
            questionNumberWrapper.appendChild(document.createTextNode("Question" +(i+1))); 
            document.getElementById("m_portlet_head_label_info_Div" + i).appendChild(questionNumberWrapper);    

            var m_portlet_body_Div = document.createElement("div"); 
            m_portlet_body_Div.appendChild(document.createTextNode(jsdata.data));
            m_portlet_body_Div.setAttribute("id", "m_portlet_body_Div" + i);
            m_portlet_body_Div.className = "m-portlet__body";
            document.getElementById("m_portlet_bordered_semi_Div" + i).appendChild(m_portlet_body_Div); 

            for(let j = 0; j < jsdataTask.length; j++){//the length of sub-questions in a question
                var sep = document.createElement("div"); 
                sep.className="m-separator m-separator--dashed m-separator--lg"
                document.getElementById("m_portlet_body_Div" + i).appendChild(sep);

                document.getElementById("m_portlet_body_Div" + i).appendChild(document.createTextNode(jsdataTask[j].aim)); //show subquestion

                var rowWrapper = document.createElement("div"); 
                rowWrapper.setAttribute("id", "rowWrapper" + i + j);
                rowWrapper.className="row";
                document.getElementById("m_portlet_body_Div" + i).appendChild(rowWrapper);

                if(jsdataTask[j].mode === "single"){
                    for(let k = 0; k < jsdataTask[j].choices.length; k++){
                        var optionWrapper = document.createElement("div"); 
                        optionWrapper.appendChild(document.createTextNode("\n"));
                        optionWrapper.setAttribute("id", "optionWrapper" + i + j + k);
                        optionWrapper.className = "col-lg-4 m--align-center";
                        document.getElementById("rowWrapper" + i + j).appendChild(optionWrapper);

                        var labelWrapper = document.createElement("label"); 
                        labelWrapper.setAttribute("id", "labelWrapper" + i + j + k);
                        labelWrapper.className = "m-radio";
                        document.getElementById("optionWrapper" + i + j + k).appendChild(labelWrapper);

                        var radioWrapper = document.createElement("input"); 
                        radioWrapper.setAttribute("id", "radioWrapper" + i + j + k);
                        radioWrapper.setAttribute("name", "radioWrapper" + i + j);
                        radioWrapper.setAttribute("type", "radio");
                        radioWrapper.setAttribute("value", k);
                        document.getElementById("labelWrapper" + i + j + k).appendChild(radioWrapper);
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createTextNode(jsdataTask[j].choices[k]));
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createElement("span"));       
                    }
                }else if(jsdataTask[j].mode === "multiple"){
                    for(let k = 0; k < jsdataTask[j].choices.length; k++){
                        var optionWrapper = document.createElement("div"); 
                        optionWrapper.appendChild(document.createTextNode("\n"));
                        optionWrapper.setAttribute("id", "optionWrapper" + i + j + k);
                        optionWrapper.className = "col-lg-4 m--align-center";
                        document.getElementById("rowWrapper" + i + j).appendChild(optionWrapper);

                        var labelWrapper = document.createElement("label"); 
                        labelWrapper.setAttribute("id", "labelWrapper" + i + j + k);
                        labelWrapper.className = "m-checkbox";
                        document.getElementById("optionWrapper" + i + j + k).appendChild(labelWrapper);

                        var checkboxWrapper = document.createElement("input"); 
                        checkboxWrapper.setAttribute("id", "checkboxWrapper" + i + j + k);
                        checkboxWrapper.setAttribute("name", "checkboxWrapper" + i + j);
                        checkboxWrapper.setAttribute("type", "checkbox");
                        // checkboxWrapper.setAttribute("value", k);
                        document.getElementById("labelWrapper" + i + j + k).appendChild(checkboxWrapper);
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createTextNode(jsdataTask[j].choices[k]));
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createElement("span"));       
                    }                   
                }
                
            }    
        }
    }
    });
});