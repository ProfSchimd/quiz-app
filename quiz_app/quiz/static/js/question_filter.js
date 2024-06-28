"use strict";

window.addEventListener("load", function() {
    const allSelect = this.document.querySelector("#allSelector");
    allSelect.addEventListener('change', function() {
        document.querySelectorAll("#questionList input[name^='id_']")
            .forEach(cb => cb.checked = allSelect.checked);
    })
    randomCheck.addEventListener('change', function() {
        document.querySelector("#randomSeed").disabled = 
            document.querySelector("#randomCheck").checked ? false : true;
    })
});