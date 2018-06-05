// var json_to_return = undefined;
jQuery(document).ready(function() {
    // var json_to_return;
    // var ds_name;
    $.ajax({
        type: 'GET',
        url: 'http://47.106.34.103:5000/data',
        success: function (json){
            document.getElementById("jsonstring").setAttribute("name", JSON.stringify(json));
            document.getElementById("projname").setAttribute("name", json.message[0].projectName);
            // json_to_return = JSON.stringify(json);
            // ds_name = json.message.projectName;
            for (let i = 0; i < json.message.length; i++){
            // json_to_return = json;
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
                if((jsdataTask[j].mode !== "open" || jsdataTask[j].label.length > 0)) {
                    var sep = document.createElement("div");
                    sep.className = "m-separator m-separator--dashed m-separator--lg"
                    document.getElementById("m_portlet_body_Div" + i).appendChild(sep);

                    document.getElementById("m_portlet_body_Div" + i).appendChild(document.createTextNode(jsdataTask[j].aim)); //show subquestion

                    var rowWrapper = document.createElement("div");
                    rowWrapper.setAttribute("id", "rowWrapper" + i + j);
                    rowWrapper.className = "row";
                    // document.getElementById("m_portlet_body_Div" + i).appendChild(document.createElement("br"));
                    document.getElementById("m_portlet_body_Div" + i).appendChild(rowWrapper);
                    // rowWrapper.insertBefore(document.createElement("br"), rowWrapper);
                }
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
                        radioWrapper.setAttribute("value", jsdataTask[j].choices[k]);
                        // document.getElementById("lalalala").setAttribute("name", jsdataTask[0].label);
                        if(jsdataTask[j].choices[k] === jsdataTask[j].label){
                            radioWrapper.checked = true;
                        }
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
                        checkboxWrapper.setAttribute("value", jsdataTask[j].choices[k]);
                        if(jsdataTask[j].label !== null) {
                            for (let l = 0; l < jsdataTask[j].label.length; l++) {
                                if (jsdataTask[j].label[l] === jsdataTask[j].choices[k]) {
                                    checkboxWrapper.checked = true;
                                }
                            }
                        }
                        document.getElementById("labelWrapper" + i + j + k).appendChild(checkboxWrapper);
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createTextNode(jsdataTask[j].choices[k]));
                        document.getElementById("labelWrapper" + i + j + k).appendChild(document.createElement("span"));       
                    }                   
                }else if(jsdataTask[j].mode === "open" && jsdataTask[j].label.length > 0){
                  var col_sm_12_Div = document.createElement("div"); 
                  col_sm_12_Div.setAttribute("id", "col_sm_12_Div" + i + j);
                  col_sm_12_Div.className = "col-lg-4 col-md-9 col-sm-12";
                  document.getElementById("rowWrapper" + i + j).appendChild(col_sm_12_Div);

                  var selectedWrapper = document.createElement("div"); 
                  selectedWrapper.setAttribute("id", "selectedWrapper" + i + j);
                  selectedWrapper.setAttribute("name", "selectedWrapper" + i + j);
                  selectedWrapper.setAttribute("multiple", "multiple");
                  selectedWrapper.className = "form-control m-select2";
                  document.getElementById("col_sm_12_Div" + i + j).appendChild(selectedWrapper);

                  for(let k = 0; k < jsdataTask[j].label.length; k++){
                    var singleOption = document.createElement("option");
                    singleOption.setAttribute("id", "singleOption" + i + j + k); 
                    singleOption.setAttribute("value", jsdataTask[j].label[k]);
                    // singleOption.setAttribute("selected", "selected");
                    singleOption.selected=true;
                    document.getElementById("selectedWrapper" + i + j).appendChild(singleOption);
                    document.getElementById("singleOption" + i + j + k).appendChild(document.createTextNode(jsdataTask[j].label[k]));
                  }            
                }
                
            }    
        }
        }
    });
});

function gatherValues() {
    t = document.getElementById("jsonstring").getAttribute("name");
    console.log(t);
    json_to_return = JSON.parse(t);
    for (let i = 0; i < json_to_return.message.length; i++){
        for(let j = 0; j<json_to_return.message[i].task.length; j++){
            if(json_to_return.message[i].task[j].mode === "single"){
                var radioname = "radioWrapper" + i + j;
                if ($("input[name=" + radioname + "]:checked").length > 0){
                    json_to_return.message[i].task[j].label = document.querySelector('input[name="' + radioname + '"]:checked').value;
                }
                // var radios = document.getElementsByName("radioWrapper" + i + j);
                // for (let k = 0; k < radios.length; k++){
                //     if (radios[i].checked){
                //         json_to_return.message[i].task[j].label = radios[i].value;
                //         break;
                //     }
                // }
            }else if(json_to_return.message[i].task[j].mode === "multiple"){
                var checkboxname = "checkboxWrapper" + i + j;
                var returnArray = $("input:checkbox[name=" + checkboxname + "]:checked").map(function(){return $(this).val()}).get();
                // json_to_return.message[i].task[j].label = document.querySelector('input[name="' + checkboxname + '"]:checked').value;
                json_to_return.message[i].task[j].label = returnArray;
            }else if(json_to_return.message[i].task[j].mode === "open"){
                var selectedname = "#selectedwrapper" + i + j;
                json_to_return.message[i].task[j].label = $(selectedname).val();
            }
        }
    }
    alert(json_to_return.message[0].task[1].label);
    // $.ajax({
    //     type: 'POST',
    //     url: 'http://47.106.34.103:5000/retrieve',
    //     data:  JSON.stringify (json_to_return), //'{"name":"jonas"}',
    //     success: function(data) {
    //         alert("Thank you!");
    //         window.location.href = "choose.html";
    //     },
    //     contentType: "application/json",
    //     dataType: 'json'
    // });
}
function queryAgain(){
    ds_name = document.getElementById("projname").getAttribute("name");
    fetch_address = "http://47.106.34.103:5000/choose/" + ds_name;
    window.location.href = fetch_address;
}
$('button#submit_result').on('click', gatherValues())
$('button#five_more').on('click', gatherValues(), queryAgain());
//     $( "#submit_result" ).click(gatherValues());
//     $( "#five_more" ).click(gatherValues(), queryAgain());