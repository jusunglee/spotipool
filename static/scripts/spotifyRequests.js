$(document).ready(function () {
    // event listener for the search button
    $("#search-button").click(function () {
        $("#search-results-container").empty();
        var query = $("#search-bar").val()
        var encodedQuery = encodeURI(query);
        $.get("track/" + encodedQuery, function (data, status) {
            displaySearchResults(data);
        });
    });

    $("#add-button").click(function () {
        var tracksList = []
        $("div[clicked='true']").val(function () {
            tracksList.push(($(this).attr('song_id')));
        });

        rawData = {
            'data': tracksList
        }

        $.ajax({
            type: "POST",
            url: "/dashboard/tracks",
            data: rawData,
        }).done(function (results) {
            console.log(results)
            if (results['status'] == "success") {
                alert('Songs successfully queued.');
                $("div[clicked='true']").val(function () {
                    var $clickedItem = $(this);
                    $clickedItem.toggleClass("search-result-item-highlighted");
                    $clickedItem.toggleClass("search-result-item");
                    $clickedItem.attr("clicked", "false");
                });
                $("#add-button").attr('disabled', 'disabled');
                $("#add-button").attr('num-selected-tracks', 0);
            }
            else {
                alert('Fail!');
            }
        });

    });
});

displaySearchResults = function (searchResults) {
    for (var i = 0; i < searchResults.length; i++) {
        var track = searchResults[i];
        var trackName = track['song_name'];
        var artistName = track['artist_name'];
        var songId = track['song_id'];
        var $resultItemDiv = $("<div>", { id: "search-result-" + i, "class": "search-result-item", "clicked": "false", "song_id": songId });
        var $trackNameItem = $("<p>", { "class": "track-name" });
        $trackNameItem.append(trackName);
        var $artistNameItem = $("<p>", { "class": "artist-name" });
        $artistNameItem.append(artistName);
        $resultItemDiv.append($trackNameItem);
        $resultItemDiv.append($artistNameItem);

        // onclick listener to highlight the individual search result item
        $resultItemDiv.click(function () {
            var $clickedItem = $(this);
            $clickedItem.toggleClass("search-result-item-highlighted");
            $clickedItem.toggleClass("search-result-item");
            var numSelectedTracks = parseInt($("#search-results-container").attr("num-selected-tracks"));
            if ($clickedItem.attr("clicked") == "false") {
                $clickedItem.attr("clicked", "true");
                $("#search-results-container").attr("num-selected-tracks", numSelectedTracks + 1);
                numSelectedTracks += 1;
            }
            else {
                $clickedItem.attr("clicked", "false");
                $("#search-results-container").attr("num-selected-tracks", numSelectedTracks - 1);
                numSelectedTracks -= 1;
            }

            if (numSelectedTracks > 0) {
                $("#add-button").removeAttr('disabled');
            }
            else {
                $("#add-button").attr('disabled', 'disabled');
            }
        });

        $("#search-results-container").append($resultItemDiv);
    }
}
