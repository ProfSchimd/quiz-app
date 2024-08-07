"use strict";

let options = []

window.addEventListener("load", function() {
    const inputArea = this.document.querySelector("#inputArea");
    inputArea.addEventListener("input", function(event) {
        const text = event.target.value;
        const solutionList = document.querySelector("#solutionList");
        solutionList.innerHTML = "";
        const matchResult = text.matchAll(/{{\d+}}/gm);
        console.log();
        for (let m of matchResult) {
            const i = parseInt(m[0].slice(2,-2));
            console.log(i);
            options[i] = options[i] || "";
            const li = document.createElement("li");
            li.innerText = `${i}:`;
            li.appendChild(document.createElement("input"))
            solutionList.appendChild(li);
        }
        console.log(options)
    });
});