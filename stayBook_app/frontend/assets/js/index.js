// ==================================================
// Autherization
// ==================================================
function getAuthHeader() {
    const token = localStorage.getItem("access_token");
    return token ? { "Authorization": `Bearer ${token}` } : {};
}


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
                                <a href="/listing.html?id=${item.uid}" class="listing-link">
                                    <div class="card listing-card" style="width: 18rem;">
                                        <img 
                                            src="${item.image || 'https://via.placeholder.com/300x200'}" 
                                            class="card-img-top" 
                                            alt="${item.title}"
                                        >
                                        <div class="card-img-overlay"></div>
                                            <div class="card-body">
                                                <b><span class="card-title">${item.title}</span></b>
                                                <p class="card-text" style="font-size: small;">
                                                ₹${item.price} / night
                                                </p>
                                            </div>
                                    </div>
                                </a>
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