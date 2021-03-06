var tokenBool = false;
if (document.querySelector('[name=csrfmiddlewaretoken]')){
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrfToken);
    tokenBool = true;
}


function fetchJSON(uri, m='GET', b='',){
    var auth = {'Authorization': 'Basic' + btoa('socialcircleauth:cmput404')}
    if (m === "GET" || m === "DELETE"){
        if (tokenBool){
            var request = new Request(uri, {method:m, headers:{'X-CSRFToken':csrfToken}});
        } else {
            var request = new Request(uri, {method:m, headers:auth});
        }
    } else if (m ==='POST' || m === "PUT") {
        if (tokenBool){
            var request = new Request(uri, {method:m, headers:{'X-CSRFToken':csrfToken}, body:JSON.stringify(b)});
        } else {
            var request = new Request(uri, {method:m, headers:auth, body:JSON.stringify(b)});
        }
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
    var url = 'https://' + location.host + '/authors/' + user_id + '/followers/' + foreign_id + '/'

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
    var url = 'https://' + location.host + '/authors/' + user_id + '/followers/'

    fetchJSON(url).then((json) => {
        console.log("Printing Follower list JSON:");
        console.log(json.items);
        console.log(JSON.stringify(json));

        var list = json.items
        wrapper.innerHTML = ''
        for (var i in list){
            var user = list[i]
            console.log('PRINTING LIST' + Object.keys(list[i]));
            var userPage = 'https://' + location.host + "/authors/" + list[i].user + "/";
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
            var userPage = 'https://' + location.host + "/authors/" + list[i].user + "/";
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

function fetchUserPage(user_id, host=location.host){
    var url = 'https://' + host + '/authors/' + user_id + '/'

    var frame = document.getElementsByTagName('body');
    console.log(frame)
    
    fetchJSON(url).then((json) => {

        var list = json
        console.log("Printing json: " + JSON.stringify(list));
        //var node = document.createElement("div");
        var item = "<div><h1>" + list.displayName + "</h1>"
        item += "<img src=" + list.profileImage + " alt = 'NO IMAGE'>"
        item += "<p>" + list.bio + "</p>"
        //node.innerHTML = item
        //rame.appendChild(node)
        frame[0].innerHTML += item
    
    });
}
    

function update(user_id){
    viewFollowerList(user_id);
    viewFollowingList(user_id);
}

