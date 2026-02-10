function searchCourse() {
    let input = document.getElementById("search").value.toLowerCase();
    let items = document.querySelectorAll("li");

    items.forEach(item => {
        item.style.display = item.innerText.toLowerCase().includes(input)
            ? "block"
            : "none";
    });
}
