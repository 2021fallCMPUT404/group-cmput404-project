const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function fetchJSON(uri, m='GET', b=''){
    if (m === "GET" || m === "DELETE"){
        var request = new Request(uri, {method:m, headers:{'X-CSRFToken':csrfToken}});
    } else if (m ==='POST' || m === "PUT") {
        var request = new Request(uri, {method:m, headers:{'X-CSRFToken':csrfToken}, body:JSON.stringify(b)});
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
    // This will make a DELETE request to the url
    // The foreign_id user will unfollow the user_id user
    var url = 'http://' + location.host + '/authors/' + user_id + '/followers/' + foreign_id + '/'

    fetchJSON(url, m="DELETE").then((json) => {
        console.log("Delete request json: " + json);
        console.log("Calling update on id: " + foreign_id);
        update(foreign_id);

    });

    

}


function viewFollowerList(user_id){
    //console.log("CALLING FOLLOWER FUNCTION")
    var wrapper = document.getElementById('followers')
    //console.log(wrapper.length)
    var url = 'http://' + location.host + '/authors/' + user_id + '/followers/'

    fetchJSON(url).then((json) => {
        console.log("Printing Follower list JSON:");
        console.log(json.items);
        console.log(JSON.stringify(json));

        var list = json.items
        wrapper.innerHTML = ''
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
            //item += '<input aria-current="true"type="button" onclick="unfollowUser('+ user_id + ',' + user.user + '); viewFollowerList('+user_id+')" value="Unfollow">'
            //item += "<input type='button' onclick='viewFollowerList(" + user.id + ") value='Update'></div></div>";
            wrapper.innerHTML += item;
        }

        console.log(wrapper.innerHTML);
    });

}

function viewFollowingList(user_id){
    console.log("user_id is: " + user_id)
    var wrapper = document.getElementById('follows')
    //console.log(wrapper.length)
    var url = 'http://' + location.host + '/authors/' + user_id + '/following/'

    fetchJSON(url).then((json) => {
        console.log("Printing Following list JSON:");
        console.log(json.items);
        console.log(JSON.stringify(json));

        var list = json.items
        wrapper.innerHTML = ''
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
            item += '<input aria-current="true"type="button" onclick="unfollowUser('+user.user + ',' + user_id + ');" value="Unfollow">'
            //item += "<input type='button' onclick='viewFollowerList(" + user.id + ") value='Update'></div></div>";
            wrapper.innerHTML += item;
        }

        console.log(wrapper.innerHTML);
    });

}

function update(user_id){
    viewFollowerList(user_id);
    viewFollowingList(user_id);
}

