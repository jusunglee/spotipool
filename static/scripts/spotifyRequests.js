sendTrackSearchRequest = function() {
    var searchBarText = document.getElementById("searchBar").value;
    $.get("demo_test.asp/", function (rawData, status) {
        var data = JSON.parse(rawData);
        console.log(data);
        alert("dpne");
    });
}