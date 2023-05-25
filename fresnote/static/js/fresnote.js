function flaskRequest({requestType, url, payload = null, toastParams = false} = {}) {
    const request = new XMLHttpRequest();
    request.open(requestType, url, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(payload);

    request.onload = function() {
        responseStatus = request.status;
        responseText = request.responseText;
        if (responseStatus == 200){
            if (toastParams == false) {
                toastr.success(responseText, 'Success');
            } else {
                toastr.success(responseText, 'Success', toastParams);
            }
        } else {
            toastr.error(responseText, 'Error');
        }
    };
}


function addNewNotebook(project) {
    let notebook = prompt("Enter notebook name:", "");
    if (notebook != null) {
        requestType = "POST";
        url = '/'+project+'/add_notebook';
        payload = JSON.stringify({'notebook': notebook});
        toastParams = {timeOut: 1000,
                       fadeOut: 1000,
                       onHidden: function () {
                       window.location.href = "/serve/"+project+'/'+notebook+"/"+"First chapter";
                      }};
        flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
        } else {
            toastr.error('Action cancelled.', 'Error');
        }
}



function addNewChapter(project, notebook) {
    let chapter = prompt("Enter chapter name:", "");
    if (chapter != null) {
        requestType = "POST";
        url = '/'+project+'/add_chapter';
        payload = JSON.stringify({ 'notebook': notebook, 'chapter': chapter });
        toastParams = {timeOut: 1000,
                        fadeOut: 1000,
                        onHidden: function () {
                          window.location.href = "/serve/"+project+'/'+notebook+"/"+chapter;
                       }};
        flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
    } else {
        toastr.error('Action cancelled.', 'Error');
    }
}



function editNotebook() {
    var notebookSectionID = "notebookSection";
    var notebookSection = document.getElementById(notebookSectionID);

    var editButtonID = "editNotebookButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveNotebookButton";
    var saveButton = document.getElementById(saveButtonID);

    notebookSection.style.border = "3px solid #24a2b8";
    notebookSection.setAttribute('contenteditable', 'true');

    editButton.classList.add('disabled');
    saveButton.classList.remove('disabled');
}


function saveNotebook(project, previousNotebookTitle, chapter) {
    var notebookSectionID = "notebookSection";
    var notebookSection = document.getElementById(notebookSectionID);

    var newNotebookTitle = notebookSection.innerText;

    var editButtonID = "editNotebookButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveNotebookButton";
    var saveButton = document.getElementById(saveButtonID);

    notebookSection.style.border = "";
    notebookSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');

    requestType = "POST";
    url = '/'+project+'/change_notebook_title';
    payload = JSON.stringify({ 'previousNotebookTitle': previousNotebookTitle, 'newNotebookTitle': newNotebookTitle });
    toastParams = {timeOut: 1000,
                   fadeOut: 1000,
                   onHidden: function () {
                        window.location.href = "/serve"+'/'+project+'/'+newNotebookTitle+'/'+chapter;
                  }};
    flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
}


function editChapter() {
    var chapterSectionID = "chapterSection";
    var chapterSection = document.getElementById(chapterSectionID);

    var editButtonID = "editChapterButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveChapterButton";
    var saveButton = document.getElementById(saveButtonID);

    chapterSection.style.border = "3px solid #24a2b8";
    chapterSection.setAttribute('contenteditable', 'true');

    editButton.classList.add('disabled');
    saveButton.classList.remove('disabled');
}


function saveChapter(project, notebook, previousChapterTitle) {
    var chapterSectionID = "chapterSection";
    var chapterSection = document.getElementById(chapterSectionID);

    var newChapterTitle = chapterSection.innerText;

    var editButtonID = "editChapterButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveChapterButton";
    var saveButton = document.getElementById(saveButtonID);

    chapterSection.style.border = "";
    chapterSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');

    requestType = "POST";
    url = '/'+project+'/change_chapter_title';
    payload = JSON.stringify({'previousChapterTitle': previousChapterTitle,
                              'newChapterTitle': newChapterTitle,
                              'notebook': notebook});
    toastParams = {timeOut: 1000,
                   fadeOut: 1000,
                   onHidden: function () {
                        window.location.href = '/serve'+'/'+project+'/'+notebook+'/'+newChapterTitle;
                  }};
    flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
}


function editSectionOrder() {
    var orderSectionID = "sectionsOrderText";
    var orderSection = document.getElementById(orderSectionID);

    var editButtonID = "editSectionOrderButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveSectionOrderButton";
    var saveButton = document.getElementById(saveButtonID);

    orderSection.style.border = "3px solid #24a2b8";
    orderSection.setAttribute('contenteditable', 'true');

    editButton.classList.add('disabled');
    saveButton.classList.remove('disabled');
}


function saveSectionOrder(project, notebook, chapter) {
    var orderSectionID = "sectionsOrderText";
    var orderSection = document.getElementById(orderSectionID);
    var orderSectionText = orderSection.innerText;

    var editButtonID = "editSectionOrderButton";
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveSectionOrderButton";
    var saveButton = document.getElementById(saveButtonID);

    orderSection.style.border = "";
    orderSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');

    requestType = "POST";
    url = '/'+project+'/save_chapter_sections_order';
    payload = JSON.stringify({'notebook': notebook,
                              'chapter': chapter,
                              'sections': orderSectionText});
    toastParams = {timeOut: 1000,
                   fadeOut: 1000,
                   onHidden: function () {
                        document.location.reload(true);
                  }};
    flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
}


// Functions for section title
function editTitle(sectionID) {
    var titleSectionID = "title_section_"+sectionID;
    var titleSection = document.getElementById(titleSectionID);

    var editButtonID = "editTitleButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveTitleButton_"+sectionID;
    var saveButton = document.getElementById(saveButtonID);

    titleSection.style.border = "3px solid #24a2b8";
    titleSection.setAttribute('contenteditable', 'true');

    editButton.classList.add('disabled');
    saveButton.classList.remove('disabled');
}


function saveTitle(project, sectionID) {
    var titleSectionID = "title_section_"+sectionID;
    var titleSection = document.getElementById(titleSectionID);

    var titleID = "title_"+sectionID;
    var title = document.getElementById(titleID);
    var titleText = title.innerText;

    var editButtonID = "editTitleButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveTitleButton_"+sectionID;
    var saveButton = document.getElementById(saveButtonID);

    titleSection.style.border = "";
    titleSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');

    requestType = "POST";
    url = '/'+project+'/save_section_title';
    payload = JSON.stringify({'sectionID': sectionID,
                              'sectionTitle': titleText});
    toastParams = false;
    flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
}





// Functions for section tags
function editTags(project, sectionID) {
    var tagsSectionID = "tags_section_"+sectionID;
    var tagsSection = document.getElementById(tagsSectionID);

    var tagsID = "tags_"+sectionID;
    var tags = document.getElementById(tagsID);

    var editButtonID = "editTagsButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveTagsButton_"+sectionID;
    var saveButton = document.getElementById(saveButtonID);

    tagsSection.style.border = "3px solid #24a2b8";
    tagsSection.setAttribute('contenteditable', 'true');

    editButton.classList.add('disabled');
    saveButton.classList.remove('disabled');


    const request = new XMLHttpRequest();
    request.open('GET', '/'+project+'/get_tags/'+sectionID, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
    request.onload = function() {
            tags.innerText = request.responseText;
        };
}


function saveTags(project, sectionID) {
    var tagsSectionID = "tags_section_"+sectionID;
    var tagsSection = document.getElementById(tagsSectionID);

    var tagsID = "tags_"+sectionID;
    var tags = document.getElementById(tagsID);
    var tagsText = tags.innerText;

    if( tagsText.indexOf(',') != -1 ) {
        newTags = tagsText.split(',');
    } else {
        newTags = [tagsText];
    }

    var editButtonID = "editTagsButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveTagsButton_"+sectionID;
    var saveButton = document.getElementById(saveButtonID);

    tagsSection.style.border = "";
    tagsSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');


    const request = new XMLHttpRequest();
    request.open('POST', '/'+project+'/save_section_tags', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'sectionID': sectionID,
                        'sectionTags': tagsText
    }));

    request.onload = function() {
        responseStatus = request.status;
        responseText = request.responseText;
        if (responseStatus == 200){
            toastr.success( responseText, 'Success');
            tags.textContent = '';
            for (var i = 0; i < newTags.length; i++) {
                var newTag = document.createElement("span");
                newTag.className = "badge badge-warning mr-2";
                newTag.innerText = newTags[i];
                tags.appendChild(newTag);
            }
        } else {
            toastr.error( responseText, 'Error');

        }
    };
}


function saveContentFromQuill() {
    var contentText = quill.container.innerText;

    const request = new XMLHttpRequest();
    request.open('POST', '/save_section_content', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'sectionID': sectionID,
                        'sectionContent': contentText
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            document.location.reload(true);
        } else {
            toastr.error('Error while saving content.', 'Error');
            
        }
    };
}



function editContent(project, sectionID) {
    var contentSectionID = "content_section_"+sectionID;
    var contentSection = document.getElementById(contentSectionID);

    var contentID = "content_"+sectionID;
    var content = document.getElementById(contentID);

    var editButtonID = "editContentButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var foldButtonID = "foldContentButton_"+sectionID;
    var foldButton = document.getElementById(foldButtonID);

    contentSection.style.border = "3px solid #24a2b8";
    contentSection.setAttribute('contenteditable', 'false');

    editButton.classList.add('disabled');

    const request = new XMLHttpRequest();
    request.open('GET', '/'+project+'/get_content/'+sectionID, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
    request.onload = function() {
            var emptyDiv = document.createElement("div");
            content.replaceWith(emptyDiv);

            editButton.remove();
            foldButton.remove();

            var toolBar = document.createElement("div");
            toolBar.id = "custom-toolbar";
            toolBar.classList.add('mt-2');
            toolBar.classList.add('col');
            toolBar.setAttribute('contenteditable', 'false');

            var tlb_button_bold = document.createElement("button");
            tlb_button_bold.id = "tlb-button-bold";
            tlb_button_bold.classList.add('btn');
            tlb_button_bold.classList.add('btn-sm');
            tlb_button_bold.style.border = "1px solid #24a2b8";
            tlb_button_bold.innerText = "B";

            var tlb_button_link = document.createElement("button");
            tlb_button_link.id = "tlb-button-link";
            tlb_button_link.classList.add('btn');
            tlb_button_link.classList.add('btn-sm');
            tlb_button_link.classList.add('ml-2');
            tlb_button_link.style.border = "1px solid #24a2b8";
            tlb_button_link.innerText = "L";

            var tlb_button_code = document.createElement("button");
            tlb_button_code.id = "tlb-button-code";
            tlb_button_code.classList.add('btn');
            tlb_button_code.classList.add('btn-sm');
            tlb_button_code.classList.add('ml-2');
            tlb_button_code.style.border = "1px solid #24a2b8";
            tlb_button_code.innerText = "C";

            var tlb_button_math_inline = document.createElement("button");
            tlb_button_math_inline.id = "tlb-button-math-inline";
            tlb_button_math_inline.classList.add('btn');
            tlb_button_math_inline.classList.add('btn-sm');
            tlb_button_math_inline.classList.add('ml-2');
            tlb_button_math_inline.style.border = "1px solid #24a2b8";
            tlb_button_math_inline.innerText = "Mi";

            var tlb_button_fold = document.createElement("button");
            tlb_button_fold.id = "tlb-button-fold";
            tlb_button_fold.classList.add('btn');
            tlb_button_fold.classList.add('btn-sm');
            tlb_button_fold.classList.add('ml-2');
            tlb_button_fold.style.border = "1px solid #24a2b8";
            tlb_button_fold.innerText = "Fo";

            var tlb_button_image = document.createElement("button");
            tlb_button_image.id = "tlb-button-image";
            tlb_button_image.classList.add('btn');
            tlb_button_image.classList.add('btn-sm');
            tlb_button_image.classList.add('ml-2');
            tlb_button_image.style.border = "1px solid #24a2b8";
            tlb_button_image.innerText = "Im";

            toolBar.appendChild(tlb_button_bold);
            toolBar.appendChild(tlb_button_link);
            toolBar.appendChild(tlb_button_code);
            toolBar.appendChild(tlb_button_math_inline);
            toolBar.appendChild(tlb_button_fold);
            toolBar.appendChild(tlb_button_image);

            emptyDiv.appendChild(toolBar);

            var quillEditor = document.createElement("div");
            quillEditor.id = "editorQuill";
            quillEditor.classList.add('ql-editor');
            quillEditor.classList.add('col');
            quillEditor.innerText = request.responseText;

            emptyDiv.appendChild(quillEditor);

            var quill = new Quill('#editorQuill', {
                modules: {
                    toolbar: '#custom-toolbar',
                    clipboard: {
                        matchVisual: false
                    }
                 },
                formats: [],
                theme: 'snow'
            });

            var Parchment = Quill.import("parchment");

            let CustomClass = new Parchment.Attributor.Class('custom', 'ql-custom', {
              scope: Parchment.Scope.INLINE
            });

            Quill.register(CustomClass, true);

            var tlb_button_bold = document.querySelector('#tlb-button-bold');
            tlb_button_bold.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, "****" );
                quill.setSelection(cursorPosition.index + 2, 0);
            });

            var tlb_button_link = document.querySelector('#tlb-button-link');
            tlb_button_link.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, "[]()" );
                quill.setSelection(cursorPosition.index + 1, 0);
            });

            var tlb_button_code = document.querySelector('#tlb-button-code');
            tlb_button_code.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, "```\n\n```" );
                quill.setSelection(cursorPosition.index + 4, 0);
            });

            var tlb_button_math_inline = document.querySelector('#tlb-button-math-inline');
            tlb_button_math_inline.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, "\\(\\)" );
                quill.setSelection(cursorPosition.index + 2, 0);
            });

            var tlb_button_fold = document.querySelector('#tlb-button-fold');
            tlb_button_fold.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, "\\begin{fold}Title\n\n\n\n\\end{fold}" );
                quill.setSelection(cursorPosition.index + 19, 0);
            });

            var tlb_button_image = document.querySelector('#tlb-button-image');
            tlb_button_image.addEventListener('click', function() {
                var cursorPosition = quill.getSelection(true);
                quill.insertText(cursorPosition, '<div class="container-fluid">\n\\btnimg{Title,file,200,100}\n<br><br>\n</div>' );
                quill.setSelection(cursorPosition.index + 38, 0);
            });

            quill.root.setAttribute('spellcheck', false);

            var saveButton = document.createElement('button');
            saveButton.innerText = 'Save';
            saveButton.classList.add('btn', 'btn-success', 'mt-4');
            emptyDiv.appendChild(saveButton);

            saveButton.onclick = function() {
                var contentText = quill.getText();

                const request = new XMLHttpRequest();
                request.open('POST', '/'+project+'/save_section_content', true);
                request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
                request.send(JSON.stringify({
                                    'sectionID': sectionID,
                                    'sectionContent': contentText
                }));

                request.onload = function() {
                    responseStatus = request.status;
                    if (responseStatus == 200){
                        document.location.reload(true);
                    } else {
                        toastr.error('Error while saving content.', 'Error');
                        
                    }
                };
            }

            var cancelButton = document.createElement('button');
            cancelButton.innerText = 'Cancel';
            cancelButton.classList.add('btn', 'btn-warning', 'mt-4', 'ml-4');
            emptyDiv.appendChild(cancelButton);

            cancelButton.onclick = function() {
                toastr.error('Action cancelled.', 'Error');
                setTimeout(function() {
                  document.location.reload();
                }, 2000);
            };
        };
}


 
function addNewSection(project, notebook, chapter) {
    const request = new XMLHttpRequest();
    request.open('POST', '/add_new_section/'+project+'/'+notebook+'/'+chapter, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            document.location.reload(true);
        } else {
            toastr.error('Error while saving content.', 'Error');

        }
    };
}


function toggleFoldState(project, sectionID) {
    const request = new XMLHttpRequest();
    request.open('GET', '/'+project+'/toggle_fold_state/'+sectionID, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
}


function deleteSection(project, sectionID) {
    var confirmation = confirm("Permantly delete section?");
    if (confirmation == true) {
        requestType = "GET";
        url = '/'+project+'/delete_section/'+sectionID;
        payload = null;
        toastParams = {timeOut: 300,
                       fadeOut: 300,
                       onHidden: function () {
                            // window.location.reload();
                            let CardAnimation = anime({
                                              targets: '#chapterSectionCard_'+sectionID,
                                              opacity: [1,0],
                                              duration: 500,
                                              easing: 'easeInOutSine'
                                            });

                            setTimeout(function(){ 
                                var sectionCard = document.getElementById('chapterSectionCard_'+sectionID);
                                sectionCard.style.display = "none";
                            }, 1000);}}
        flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}


function deleteChapter(project, notebook, chapter) {
    var confirmation = confirm("Permantly delete chapter?");
    if (confirmation == true) {
        var confirmation = confirm("Keep chapter sections?\nNote: Cancel deletes!");
        if (confirmation == true) {
            requestType = "GET";
            url = '/'+project+'/delete_chapter_keep_sections/'+notebook+'/'+chapter;
            payload = null;
            toastParams = {timeOut: 1000,
                           fadeOut: 1000,
                           onHidden: function () {
                           window.location.href = "/load/"+project;
                          }};
            flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
        } else {
            requestType = "GET";
            url = '/'+notebook+'/delete_chapter_and_sections/'+projectName+'/'+chapterName;
            payload = null;
            toastParams = {timeOut: 1000,
                           fadeOut: 1000,
                           onHidden: function () {
                           window.location.href = "/load/"+project;
                          }};
            flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
        }
    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}


function deleteNotebook(project, notebook) {
    var confirmation = confirm("Permantly delete notebook?");
    if (confirmation == true) {
        var confirmation = confirm("Keep notebook sections?\nNote: Cancel deletes!");
        if (confirmation == true) {
            requestType = "GET";
            url = '/'+project+'/delete_notebook_keep_sections/'+notebook;
            payload = null;
            toastParams = {timeOut: 1000,
                           fadeOut: 1000,
                           onHidden: function () {
                           window.location.href = "/load/"+project;
                          }};
            flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
        } else {
            requestType = "GET";
            url = '/'+project+'/delete_notebook_and_sections/'+notebook;
            payload = null;
            toastParams = {timeOut: 1000,
                           fadeOut: 1000,
                           onHidden: function () {
                           window.location.href = "/load/"+project;
                          }};
            flaskRequest({requestType:requestType, url:url, payload:payload, toastParams:toastParams});
        }
    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}


function searchBar(project) {
    var searchBarID = "searchBarQuery";
    var query = document.getElementById(searchBarID).value;
    const request = new XMLHttpRequest();
    request.open("POST", '/'+project+"/search", true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({'query': query}));

    request.onload = function() {
        responseStatus = request.status;
        responseText = request.responseText;
        if (responseStatus == 200){
            window.location.href = "/"+project+"/search/"+responseText;
        } else {
            toastr.error(responseText, 'Error');
        }
    };
}

function viewScript(project, scriptPath) {
    window.location.href = "/"+project+"/highlight/"+scriptPath;
}

function runScript(project, scriptName, scriptID) {
    var runIndicator = document.getElementById(scriptID);
    runIndicator.innerText = "Running..."
    runIndicator.style.color = "red";
    runIndicator.removeAttribute("hidden");

    toastr.success('Script running.', 'Success');

    const request = new XMLHttpRequest();
    request.open("POST", '/'+project+"/run_script", true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({'script': scriptName}));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success('Script done.', 'Success');
            runIndicator.innerText = "Run successful."
            runIndicator.style.color = "green";
        } else {
            toastr.error('Script error.', 'Error');
            runIndicator.innerText = "Run error."
            runIndicator.style.color = "red";
        }
    };
}
