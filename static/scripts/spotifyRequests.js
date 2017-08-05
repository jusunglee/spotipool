sendTrackSearchRequest = function() {
    var searchBarText = document.getElementById("searchBar").value;
    searchBarText = encodeURI(searchBarText);
    $.get("get_search_track/" + searchBarText, function (rawData, status) {
        var data = JSON.parse(rawData);
        console.log(data);
        alert("dpne");
    });
}