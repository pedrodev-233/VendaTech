document.addEventListener('DOMContentLoaded', function () {
    const eyeSvg = `
        <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
            <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"></path>
            <circle cx="12" cy="12" r="3"></circle>
        </svg>
    `;

    const eyeOffSvg = `
        <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
            <path d="M3 3l18 18"></path>
            <path d="M10.58 10.58A2 2 0 0 0 13.42 13.42"></path>
            <path d="M9.88 5.56A10.96 10.96 0 0 1 12 5c6.5 0 10 7 10 7a17.64 17.64 0 0 1-4.23 5.2"></path>
            <path d="M6.61 6.61A18.39 18.39 0 0 0 2 12s3.5 7 10 7a11.53 11.53 0 0 0 5.39-1.61"></path>
        </svg>
    `;

    const toggleButtons = document.querySelectorAll('.password-toggle');

    toggleButtons.forEach(function (button) {
        const icon = button.querySelector('.toggle-icon');
        if (icon) {
            icon.innerHTML = eyeSvg;
        }

        button.addEventListener('click', function () {
            const input = this.parentElement.querySelector('input');
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            this.setAttribute('aria-label', isPassword ? 'Ocultar senha' : 'Mostrar senha');

            const toggleIcon = this.querySelector('.toggle-icon');
            if (toggleIcon) {
                toggleIcon.innerHTML = isPassword ? eyeOffSvg : eyeSvg;
            }
        });
    });
});
