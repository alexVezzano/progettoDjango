var scrollPositions = {};

function scrollContentLeft(id) {
    var container = document.getElementById(id);
    if (container) {
        if (!scrollPositions[id]) {
            scrollPositions[id] = 0;
        }
        scrollPositions[id] -= container.clientWidth;
        if (scrollPositions[id] < 0) {
            scrollPositions[id] = 0;
        }
        container.style.transform = 'translateX(-' + scrollPositions[id] + 'px)';
    }
}

function scrollContentRight(id) {
    var container = document.getElementById(id);
    if (container) {
        if (!scrollPositions[id]) {
            scrollPositions[id] = 0;
        }
        var maxScroll = container.scrollWidth - container.clientWidth;
        scrollPositions[id] += container.clientWidth;
        if (scrollPositions[id] > maxScroll) {
            scrollPositions[id] = maxScroll;
        }
        container.style.transform = 'translateX(-' + scrollPositions[id] + 'px)';
    }
}