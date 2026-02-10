/**
 * Live filtering of courses based on title or category
 */
function filterCourses() {
    const query = document.getElementById('courseSearch').value.toLowerCase();
    const cards = document.getElementsByClassName('course-card');

    for (let i = 0; i < cards.length; i++) {
        const title = cards[i].querySelector('h3').innerText.toLowerCase();
        const category = cards[i].getAttribute('data-category').toLowerCase();

        if (title.includes(query) || category.includes(query)) {
            cards[i].style.display = "block";
        } else {
            cards[i].style.display = "none";
        }
    }
}