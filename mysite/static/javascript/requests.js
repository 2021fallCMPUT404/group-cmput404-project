function fetchJSON(uri, m='GET', b=''){
    if (m === "GET" || m === "DELETE"){
        var request = new Request(uri, {method:m,});
    } else if (m ==='POST' || m === "PUT") {
        var request = new Request(uri, {method:m, body:JSON.stringify(b)});
    }
    //console.log(request.method);
    return fetch(request).then((response) => {
        if (response.status === 200) {
            console.log(response);
            return response.json();
                
        } else {
            alert("Something went wrong: " + response.status);
        }
    });
}

function unfollowUser(user_id, foreign_id){
    var url = 'http://' + location.host + '/authors/' + user_id + '/followers/' + foreign_id + '/'

    fetchJSON(url, m="DELETE").then((json) => {
        console.log(json)

    });

}

function viewFollowerList(user_id){
    //console.log("CALLING FOLLOWER FUNCTION")
    var wrapper = document.getElementsByClassName('list-group')
    console.log(wrapper.length)
    var url = 'http://' + location.host + '/authors/' + user_id + '/followers/'

    fetchJSON(url).then((json) => {
        console.log("Printing JSON:");
        console.log(json.items);
        console.log(JSON.stringify(json));

        var list = json.items
        wrapper[0].innerHTML = ''
        for (var i in list){
            var user = list[i]
            console.log('PRINTING LIST' + Object.keys(list[i]));
            var userPage = 'http://' + location.host + "/authors/" + list[i].user + "/";
            var item = '<div class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">';
            item += "<a href=" + userPage + '>';
            item += '<img src=' + list[i].profileImage + ' alt="NO IMAGE" class="rounded-circle flex-shrink-0" width="100"></a>';
            item += "<div class='d-flex gap-3 w-100 justify-content-between'><div>";
            item += "<h2 class = 'mb-0'>" + user.displayName + "</h2>";
            item += "<p>" + user.bio + "</p>";
            item += "</div>";
            item += '<input aria-current="true"type="button" onclick="unfollowUser('+user_id + ',' + user.user + ')" value="Unfollow">'
            //item += "<input type='button' onclick='viewFollowerList(" + user.id + ") value='Update'></div></div>";
            wrapper[0].innerHTML += item;
        }

        console.log(wrapper.innerHTML);
    });

}
