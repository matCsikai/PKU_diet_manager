function main() {
    var submitButton = document.getElementById('submitbutton');
    submitButton.addEventListener('click', function() {
        this.innerText = 'Loading...'
        document.getElementById('loader').style.visibility = 'visible';
        // this.setAttribute('disabled', 'disabled');
    });
}

$(document).ready(main);