// ==================================================
// Load Listings
// ==================================================
async function listings() {
    const response = await fetch("http://127.0.0.1:8000/listings/");
    const listings = await response.json();
    const container = document.getElementById("listings");

    container.innerHTML = '';
    
    listings.forEach(item => {
                    const cardWrapper = document.createElement("div");

                                cardWrapper.innerHTML = `
                                    <div class="card" style="width: 18rem;">
                                        <img 
                                            src="${item.image || 'https://via.placeholder.com/300x200'}" 
                                            class="card-img-top" 
                                            alt="${item.title}"
                                        >
                                        <div class="card-body">
                                            <h5 class="card-title">${item.title}</h5>
                                            <p class="card-text">₹${item.price} / night</p>
                                            <a href="/listing.html?id=${item.uid}" class="btn btn-primary">
                                                View Listing
                                            </a>
                                        </div>
                                    </div>
                                `;

                                container.appendChild(cardWrapper);
                            });
}



listings();



// ==================================================
// Create Button
// ==================================================
// async function create_new_listing(){
//     const btn = document.getElementById("create-btn")

//     if (btn){
//         btn.addEventListener("click", () =>{
//             window.location.href = "/new_listing.html";
//         })
//     }
// }

// create_new_listing();