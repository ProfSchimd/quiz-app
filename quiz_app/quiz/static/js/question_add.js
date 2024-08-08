"use strict";

var tagList = [];
let keys = {};
    
function renameOptions() {
    const options = document.querySelector("#optionsList");
    options.querySelectorAll("input[type='text']").forEach((t,i) => t.name = `t_${i}`);
    options.querySelectorAll("input[type='checkbox']").forEach((t,i) => t.name = `c_${i}`);
}
// Function to add an option
function addOption() {
    var optionsList = document.getElementById("optionsList");

    // Create a new list item
    var optionItem = document.createElement("div");
    optionItem.classList.add("grid")

    // Create an input field for the option text
    var optionInput = document.createElement("input");
    //optionInput.name = "option[]" ;//+ optionsList.children.length;
    optionInput.type = "text";
    optionInput.placeholder = "Option text";
    optionItem.appendChild(optionInput);

    // Create an input field for the "correct" checkbox
    var correctInput = document.createElement("input");
    correctInput.type = "checkbox";
    //correctInput.name = "check[]";// + optionsList.children.length;
    optionItem.appendChild(correctInput);

    // Create a remove button
    var removeButton = document.createElement("a");
    removeButton.textContent = "";
    removeButton.classList.add("bi-x-circle-fill","danger");
    removeButton.onclick = function() {
        optionsList.removeChild(optionItem); // Remove the option when the button is clicked
        renameOptions();
    };
    optionItem.appendChild(removeButton);

    optionsList.appendChild(optionItem); // Add the new option to the list
    renameOptions();
}

function addTag() {
    const inputTag = document.querySelector("#inputTag");
    const newTag = inputTag.value;
    if (newTag && !tagList.some(tag => tag.toLowerCase() === newTag.toLowerCase())) {
        tagList.push(newTag);
    }
    showTags(); 
}

function removeTag(tag) {
    tagList = tagList.filter(t => t.toLowerCase() !== tag.toLowerCase());
    showTags();
}

function showTags() {
    const tagDiv = document.querySelector("#tagList");
    // remove all children
    while(tagDiv.firstChild) {
        tagDiv.removeChild(tagDiv.firstChild);
    }
    tagList.map( (tag, index) => {
        const tagP = document.createElement("a");
        tagP.setAttribute("href", "");
        tagP.setAttribute("role", "button");
        tagP.classList.add("bg-gray-300", "p-2", "text-gray-500", "hover:bg-gray-400", "rounded-lg");
        tagP.addEventListener("click", e => {
            e.preventDefault();
            removeTag(tag);
        });
        tagP.textContent = `#${tag}`;
        tagDiv.appendChild(tagP);
        const tagIn = document.createElement("input");
        tagIn.setAttribute("type", "hidden");
        tagIn.setAttribute("name", `tag_${index}`);
        tagIn.value = tag;
        tagDiv.appendChild(tagIn);
    });
}



function typeSelect() {
    var typeSelected = document.querySelector("#q_type").value;
    document.querySelector("#fillForm").style.display = (typeSelected === "FILL") ? "block" : "none";
    document.querySelector("#choiceForm").style.display = (typeSelected !== "FILL") ? "block" : "none";
    document.querySelector("#textInverted").disabled = (typeSelected !== "INVERTIBLE");
    if (typeSelected === "SINGLE") {
        const checkboxes = document.querySelector("#optionsList").querySelectorAll("input[type='checkbox']")
        var count = 0
        checkboxes.forEach(c => count = count + (c.checked ? 1 : 0));
        if (count > 1) {
            alert("With Single question select exactly 1 solution");
        }
    }
}

// Fill question
function updateKeys(text) {
    let placeholders = new Set();
    for (let match of [...text.matchAll(/{{\d+}}/g)]) {
        placeholders.add(parseInt(match[0].slice(2,-2)));
    }

    placeholders = [... placeholders].sort((a,b)=>a-b);
    const keysUl = document.querySelector("#keysList");
    keysUl.innerHTML = "";
    for (let i of placeholders) {
        const inputKey = document.createElement("input");
        inputKey.type = "text";
        inputKey.id = `inputKey_${i}`;
        inputKey.name = `inputKey_${i}`;
        inputKey.value = keys[i] || "";
        inputKey.classList.add("w-full", "text-black", "dark:text-black", "bg-white", "dark:bg-slate-300");
        inputKey.addEventListener("change", e => keys[i]=e.target.value);

        const key = document.createElement("p");
        key.append(`Answer for blank {{${i}}}: `, inputKey);
        keysUl.appendChild(key);
    }
}

function textInput(e) {
    var typeSelected = document.querySelector("#q_type").value;
    if (typeSelected !== "FILL") {
        return;
    }
    updateKeys(e.target.value);
}

window.addEventListener("load", function() {
    const typeSelector = document.querySelector("#q_type");
    typeSelector.addEventListener("click", typeSelect);
    const inputTag = document.querySelector("#inputTag");
    inputTag.addEventListener("keydown", function(e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            if (e.target.value) {
                addTag();
                e.target.value = ""
            }
        }
    })
    document.querySelector("#fillQuestion").addEventListener("input", textInput);
    typeSelect(undefined);
    updateKeys(document.querySelector("#fillQuestion").value);
});