window.onload = function() {


    function fetchJSON(uri, m='GET', b=''){
        if (m === "GET"){
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
};