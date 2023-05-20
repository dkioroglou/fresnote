function addNewNotebook(project) {
  let notebook = prompt("Enter notebook name:", "");
  if (notebook != null) {
    const request = new XMLHttpRequest();
    request.open('POST', '/'+project+'/add_notebook', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                    'notebook': notebook,
    }));
    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success(
                  'New notebook added.',
                  'Success',
                {
                  timeOut: 1000,
                  fadeOut: 1000,
                  onHidden: function () {
                    window.location.href = "/serve/"+project+'/'+notebook+"/"+"First chapter";
                 }
               });
        } else {
            toastr.error('Error while adding notebook. Notebook not added.', 'Error');
            
        }
    };
  } else {
        toastr.error('Action cancelled.', 'Error');
  }
}



function addNewChapter(project, notebook) {
  let chapter = prompt("Enter chapter name:", "");
  if (chapter != null) {
    const request = new XMLHttpRequest();
    request.open('POST', '/'+project+'/add_chapter', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'notebook': notebook,
                        'chapter': chapter
    }));
    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success(
                  'New chapter added.',
                  'Success',
                {
                  timeOut: 1000,
                  fadeOut: 1000,
                  onHidden: function () {
                      window.location.href = "/serve/"+project+'/'+notebook+"/"+chapter;
                  }
                });
        } else {
            toastr.error('Error while adding chapter. Chapter not added.', 'Error');

        }
    };
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

    const request = new XMLHttpRequest();
    request.open('POST', '/'+project+'/change_notebook_title', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'previousNotebookTitle': previousNotebookTitle,
                        'newNotebookTitle': newNotebookTitle
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success(
                  'Notebook renamed.',
                  'Success',
                {
                  timeOut: 1000,
                  fadeOut: 1000,
                  onHidden: function () {
                    window.location.href = "/serve"+'/'+project+'/'+newNotebookTitle+'/'+chapter;
                 }
               });
        } else {
            toastr.error('Error while renaming notebook.', 'Error');

        }
    };
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

    const request = new XMLHttpRequest();
    request.open('POST', '/'+project+'/change_chapter_title', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'previousChapterTitle': previousChapterTitle,
                        'newChapterTitle': newChapterTitle,
                        'notebook': notebook
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success(
                  'Chapter renamed.',
                  'Success',
                {
                  timeOut: 1000,
                  fadeOut: 1000,
                  onHidden: function () {
                    window.location.href = '/serve'+'/'+project+'/'+notebook+'/'+newChapterTitle;
                 }
               });
        } else {
            toastr.error('Error while renaming chapter.', 'Error');

        }
    };
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


function saveSectionOrder(notebook, chapterName) {
    var projectSectionID = "projectSection";
    var projectSection = document.getElementById(projectSectionID);
    var projectTitle = projectSection.innerText;

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

    const request = new XMLHttpRequest();
    request.open('POST', '/'+notebook+'/save_chapter_sections_order', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'project': projectTitle,
                        'chapter': chapterName,
                        'sections': orderSectionText
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success(
                  'Sections order changed.',
                  'Success',
                {
                  timeOut: 1000,
                  fadeOut: 1000,
                  onHidden: function () {
                    document.location.reload(true);
                 }
               });
        } else {
            toastr.error('Error while changing sections order.', 'Error');

        }
    };
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


function saveTitle(notebook, sectionID) {
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

    const request = new XMLHttpRequest();
    request.open('POST', '/'+notebook+'/save_section_title', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'sectionID': sectionID,
                        'sectionTitle': titleText
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success( 'Section title saved.', 'Success');
        } else {
            toastr.error('Error while saving title.', 'Error');
            
        }
    };
}





// Functions for section tags
function editTags(notebook, sectionID) {
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
    request.open('GET', '/'+notebook+'/tags/'+sectionID, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
    request.onload = function() {
            tags.innerText = request.responseText;
        };
}



function saveTags(notebook, sectionID) {
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
    request.open('POST', '/'+notebook+'/save_section_tags', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify({
                        'sectionID': sectionID,
                        'sectionTags': tagsText
    }));

    request.onload = function() {
        responseStatus = request.status;
        if (responseStatus == 200){
            toastr.success( 'Section tags saved.', 'Success');
            tags.textContent = '';
            for (var i = 0; i < newTags.length; i++) {
                var newTag = document.createElement("span");
                newTag.className = "badge badge-warning mr-2";
                newTag.innerText = newTags[i];
                tags.appendChild(newTag);
            }
        } else {
            toastr.error('Error while saving tags', 'Error');

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





// Functions for section content
function editContent(notebook, sectionID) {
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
    request.open('GET', '/'+notebook+'/content/'+sectionID, true);
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
                request.open('POST', '/'+notebook+'/save_section_content', true);
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
        };
}


 
function saveContent(sectionID) {
    var contentSectionID = "content_section_"+sectionID;
    var contentSection = document.getElementById(contentSectionID);

    var contentID = "content_"+sectionID;
    var content = document.getElementById(contentID);
    var contentText = content.innerText;

    var editButtonID = "editContentButton_"+sectionID;
    var editButton = document.getElementById(editButtonID);

    var saveButtonID = "saveContentButton_"+sectionID;
    var saveButton = document.getElementById(saveButtonID);

    contentSection.style.border = "";
    contentSection.setAttribute('contenteditable', 'false');

    editButton.classList.remove('disabled');
    saveButton.classList.add('disabled');

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




// NOTES: STAYS - changed
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



function toggleFoldState(notebook, sectionID) {
    const request = new XMLHttpRequest();
    request.open('GET', '/'+notebook+'/toggle_fold_state/'+sectionID, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(null);
}



function deleteSection(notebook, sectionID) {
    var confirmation = confirm("Permantly delete section?");
    if (confirmation == true) {
        const request = new XMLHttpRequest();
        request.open('GET', '/'+notebook+'/delete_section/'+sectionID, true);
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        request.send(null);

        request.onload = function() {
            responseStatus = request.status;
            if (responseStatus == 200){
                toastr.success(
                      'Section deleted.',
                      'Success',
                    {
                      timeOut: 300,
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
                        }, 1000);
                     }
                   });
            } else {
                toastr.error('Error while deleting section.', 'Error');
                
            }
        };

    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}


function deleteChapter(notebook, projectName, chapterName) {
    var confirmation = confirm("Permantly delete chapter?");
    if (confirmation == true) {
        var confirmation = confirm("Keep chapter sections?\nNote: Cancel deletes!");
        if (confirmation == true) {
            const request = new XMLHttpRequest();
            request.open('GET', '/'+notebook+'/delete_chapter_keep_sections/'+projectName+'/'+chapterName, true);
            request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
            request.send(null);

            request.onload = function() {
                responseStatus = request.status;
                if (responseStatus == 200){
                    toastr.success( 'Deleted only chapter.', 'Success');
                } else {
                    toastr.error('Error while deleted chapter.', 'Error');
                    
                }
            };
        } else {
            const request = new XMLHttpRequest();
            request.open('GET', '/'+notebook+'/delete_chapter_and_sections/'+projectName+'/'+chapterName, true);
            request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
            request.send(null);

            request.onload = function() {
                responseStatus = request.status;
                if (responseStatus == 200){
                    toastr.success( 'Deleted chapter and sections.', 'Success');
                } else {
                    toastr.error('Error while deleted chapter and sections.', 'Error');
                    
                }
            };
        }
    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}


function deleteProject(notebook, projectName) {
    var confirmation = confirm("Permantly delete topic?");
    if (confirmation == true) {
        var confirmation = confirm("Keep topic sections?\nNote: Cancel deletes!");
        if (confirmation == true) {
            const request = new XMLHttpRequest();
            request.open('GET', '/'+notebook+'/delete_project_keep_sections/'+projectName, true);
            request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
            request.send(null);

            request.onload = function() {
                responseStatus = request.status;
                if (responseStatus == 200){
                    toastr.success( 'Deleted only topic.', 'Success');
                } else {
                    toastr.error('Error while deleted topic.', 'Error');
                    
                }
            };
        } else {
            const request = new XMLHttpRequest();
            request.open('GET', '/'+notebook+'/delete_project_and_sections/'+projectName, true);
            request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
            request.send(null);

            request.onload = function() {
                responseStatus = request.status;
                if (responseStatus == 200){
                    toastr.success( 'Deleted topic and sections.', 'Success');
                } else {
                    toastr.error('Error while deleted topic and sections.', 'Error');
                    
                }
            };
        }
    } else {
        toastr.error('Action cancelled.', 'Warning');
    }
}
