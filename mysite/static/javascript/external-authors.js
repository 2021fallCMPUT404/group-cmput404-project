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




function viewUsersExternal(request){
    var wrapper = document.getElementById('list-users')
    url = "https://unhindled.herokuapp.com/service/authors"

    fetch(url).then(json => {
        console.log(json);
        return json.JSON();
    }).then( json =>{
        console.log((JSON.stringify(json))
    })




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
            item += '<h1>' + list[i].username + '</h1>';
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