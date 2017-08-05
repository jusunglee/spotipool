sendTrackSearchRequest = function() {
    var searchBarText = document.getElementById("searchBar").value;
    searchBarText = encodeURI(searchBarText);
    $.get("track/" + searchBarText, function (rawData, status) {
        return data;
    });
};