const backButton = document.querySelector('[data-go-back]');

if (backButton) {
    backButton.addEventListener('click', () => {
        const homeUrl = backButton.dataset.homeUrl;
        const cameFromThisSite = document.referrer.startsWith(`${window.location.origin}/`);

        if (cameFromThisSite && window.history.length > 1) {
            window.history.back();
            return;
        }

        window.location.assign(homeUrl);
    });
}
