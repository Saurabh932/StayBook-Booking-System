// ==================================================
// Load Listings
// ==================================================
async function listings() {
    const response = await fetch("http://127.0.0.1:8000/listings/");
    const listings = await response.json();
    const ul = document.getElementById("listings");

    listings.forEach(item => {
        const li = document.createElement("li");
        const a = document.createElement("a");

        a.textContent = item.title;
        a.href = `/listing.html?id=${item.uid}`;

        li.appendChild(a);
        ul.appendChild(li);
    });
}

listings();



// ==================================================
// Create Button
// ==================================================
async function create_new_listing(){
    const btn = document.getElementById("create-btn")

    if (btn){
        btn.addEventListener("click", () =>{
            window.location.href = "/new_listing.html";
        })
    }
}

create_new_listing();