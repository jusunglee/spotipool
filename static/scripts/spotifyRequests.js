$(document).ready(function(){
    $("#search-button").click(function() {
        var query = $("#search-bar")[0].value;
        encodedQuery = encodeURI(query);
        $.get("track/" + encodedQuery, function (data, status) {
            displaySearchResults(data);
        });
    });
});

displaySearchResults = function(searchResults) {
    console.log(searchResults);
    for (var i = 0; i < searchResults.length; i++) {
        var track = searchResults[i];
        var trackName = track['song_name'];
        var artistName = track['artist_name'];
        var songId = track['song_id'];
        var $resultItemDiv = $("<div>", {id: "search-result-" + i, "class": "search-result-item"});
        var $trackNameItem = $("<p>", {"class": "track-name"});
        $trackNameItem.append(trackName);
        var $artistNameItem = $("<p>", {"class": "artist-name"});
        $artistNameItem.append(artistName);
        $resultItemDiv.append($trackNameItem);
        $resultItemDiv.append($artistNameItem);
        $resultItemDiv.click(function(){
            console.log(songId);
        });

        $("#search-results-container").append($resultItemDiv);
    }
}
