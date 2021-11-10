import { octokit } from "https://cdn.skypack.dev/@octokit/core";
let events = await octokit.request('GET /users/{username}/events/public', {
    username: "{{ insert_github_username }}"
})

for (let event of events) {
    console.log(event)
}