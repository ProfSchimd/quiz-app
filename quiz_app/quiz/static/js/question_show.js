"use strict";

window.addEventListener("load", function() {
    const formatSelector = document.querySelector("#formatSelector");
    const exportButton = document.querySelector("#exportButton");
    exportButton.innerText = ` Export ${formatSelector.options[formatSelector.selectedIndex].text}`;
    formatSelector.addEventListener("change", function() {
        exportButton.innerText = ` Export: ${this.options[this.selectedIndex].text}`;
    });
});
