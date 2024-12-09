const toggleButton = document.getElementById('dark-mode-toggle');

if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode');
}

toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('dark-mode', 'enabled');
    } else {
        localStorage.setItem('dark-mode', 'disabled');
    }
});

const celsiusToggle = document.getElementById('celsius-toggle');
const fahrenheitToggle = document.getElementById('fahrenheit-toggle');

celsiusToggle.addEventListener('change', () => {
    if (celsiusToggle.checked) {
        fahrenheitToggle.checked = false; // Deselect Fahrenheit
    }
});

fahrenheitToggle.addEventListener('change', () => {
    if (fahrenheitToggle.checked) {
        celsiusToggle.checked = false; // Deselect Celsius
    }
});
