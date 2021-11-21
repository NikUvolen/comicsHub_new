let top_profile_link = document.querySelector('#top_profile_link');
let top_profile_menu = document.querySelector('#top_profile_menu');

top_profile_link.addEventListener('click', () => {
    top_profile_link.classList.toggle('active');
    top_profile_menu.classList.toggle('show');
})
