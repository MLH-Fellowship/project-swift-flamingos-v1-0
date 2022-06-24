const form = document.getElementById('form');
 
form.addEventListener('submit', function(e) {
    // Prevent default behavior:
    e.preventDefault();
    // Create payload as new FormData object:
    const payload = new FormData(form);
    // Post the payload using Fetch:
    fetch('http://mlhportofolio.duckdns.org:5000/api/timeline_post', {
    method: 'POST',
    body: payload,
    })
    .then(res => res.json())
    .then(data => console.log(data))
})