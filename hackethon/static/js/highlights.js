document.addEventListener('DOMContentLoaded', function() {
    const highlightReel = document.getElementById('highlight-reel');
    const YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'; // Replace with your actual API key
    const PLAYLIST_ID = 'YOUR_PLAYLIST_ID'; // Replace with the ID of the XIE YouTube playlist

    function fetchHighlights() {
        const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${PLAYLIST_ID}&key=${YOUTUBE_API_KEY}&maxResults=6`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.items) {
                    data.items.forEach(item => {
                        const videoId = item.snippet.resourceId.videoId;
                        const thumbnailUrl = item.snippet.thumbnails.medium.url;
                        const title = item.snippet.title;

                        const videoElement = `
                            <div class="card m-2" style="width: 18rem;">
                                <img src="${thumbnailUrl}" class="card-img-top" alt="${title}">
                                <div class="card-body">
                                    <h5 class="card-title">${title}</h5>
                                    <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" class="btn btn-danger">Watch on YouTube</a>
                                </div>
                            </div>
                        `;
                        highlightReel.innerHTML += videoElement;
                    });
                }
            })
            .catch(error => console.error('Error fetching YouTube highlights:', error));
    }

    fetchHighlights();
});
