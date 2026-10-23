// ${project_name} - Vanilla JS app

let count = 0;
const btn = document.getElementById("counter-btn");

btn.addEventListener("click", () => {
    count++;
    btn.textContent = `Count: ${count}`;
});

console.log("${project_name} loaded!");