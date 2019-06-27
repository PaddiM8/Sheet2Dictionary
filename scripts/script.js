const main = document.querySelector("main");
const listElement = document.getElementById("word-list");
const paginationHeight = document.querySelector(".pagination").offsetHeight;
const maxItems = listElement.offsetHeight / (listElement.children[0].offsetHeight + 4);
const options = {
   valueNames: ["word", "english", "id"],
   page: Math.floor(maxItems),
   pagination: true,
   indexAsync: true,
   pagination: {
      innerWindow: 1,
      left: 0,
      right: 0
   },
   item: listElement.children[0].outerHTML
};

listElement.children[0].remove();

const wordList = new List("wrapper", options, words);
selectWord(0);

document.getElementById("pagPrevious").addEventListener("click", () => {
   document.querySelector(".pagination .active").previousSibling.click();
});

document.getElementById("pagNext").addEventListener("click", () => {
   document.querySelector(".pagination .active").nextSibling.click();
});

listElement.addEventListener("click", e => {
   if (e.target.tagName == "UL") return;

   let id = "";
   if (e.target.tagName == "LI")
        id = e.target.querySelector(".id").innerHTML;
   else id = e.target.parentElement.querySelector(".id").innerHTML;
   selectWord(id);
});

function selectWord(id) {
   // Set the basic ones
   for (const child of main.children) {
      if (child.tagName == "H3") break; // Stop at definitions and all that
         let content = words[id][child.className];

         if (child.className == "types" && content.length > 0) {
            child.innerHTML = content.join(", ");
         } else if (content != undefined) {
            child.innerHTML = content;
         } else {
            child.innerHTML = "";
         }
   }

   // Definition
   const definitions = words[id].definitions;
   const definitionElement = main.querySelector(".definition");
   definitionElement.innerHTML = "";

   for (let i = 0; i < definitions.length; i++) {
      const type = words[id].types[i];
      const definition = words[id].definitions[i];
      if (type != undefined)
         definitionElement.innerHTML += `<b>${type}: </b>${definition}<br />`;
   }

   // Example
   const examples = words[id].examples;
   const exampleElement = main.querySelector(".examples");
   exampleElement.innerHTML = "";

   for (let i = 0; i < examples.length; i++) {
      const type = words[id].types[i];
      const typeExamples = words[id].examples[i];
      if (type != undefined)
         exampleElement.innerHTML += `<h4>${type}</h4>`;

      for (example of typeExamples) {
         exampleElement.innerHTML += `${example.join("<br />")}<br /><br />`;
      }
   }

   // hide if empty
   const definitionsState = definitions.length != 0 ? "" : "none";
   const examplesState = examples.length != 0 ? "" : "none";
   main.querySelector(".definitions-title").style.display = definitionsState;
   main.querySelector(".examples-title").style.display = examplesState;
};
