// TODO: убрать баг с ручным удалением класса и отрицательным счётчиком лайков
document.addEventListener("DOMContentLoaded", () => {
    function changeColor(icon) {
        const result = icon.classList.toggle("active");
        return result;
    }

    function hiddenLikeInfo() {
        likeInfo.classList.remove('active');
    }

    function addLikeToCounter(counter, likeInfo) {
        let value = parseInt(counter.innerHTML) + 1;
        counter.innerHTML = value;

        likeInfo.classList.add('active');
        setTimeout(hiddenLikeInfo, 4000);
    }

    function removeLikeToCounter(counter, likeInfo) {
        let value = parseInt(counter.innerHTML) - 1;
        counter.innerHTML = value

        likeInfo.classList.remove('active');
    }

    const likeIcon = document.querySelector('.like-icon');
    const dislikeIcon = document.querySelector('.dislike-icon');
    const likeInfo = document.querySelector('#like-info');

    likeIcon.addEventListener('click', () => {
        const result = changeColor(likeIcon);
    })
    dislikeIcon.addEventListener('click', () => {
        const result = changeColor(dislikeIcon);
    })
})