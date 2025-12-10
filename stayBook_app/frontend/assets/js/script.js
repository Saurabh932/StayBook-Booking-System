export async function loadLayout(pageContentId){
    const layoutContainer = document.getElementById("layout");

    // Check for the container first
    if (!layoutContainer) {
        console.error("Layout container (#layout) not found in the HTML.");
        return;
    }

    // Load layout.html
    try {
        const layoutResponse = await fetch("/templates/layout.html");
        
        if (!layoutResponse.ok) {
            // Throw an error if the HTTP status is 404, 500, etc.
            throw new Error(`HTTP Error: ${layoutResponse.status} - Could not load layout.html`);
        }
        
        const layoutHTML = await layoutResponse.text();
        layoutContainer.innerHTML = layoutHTML;

    } catch (error) {
        console.error("Failed to load or parse layout.html:", error);
        // Stop execution if the layout cannot be loaded
        return; 
    }

    // Moving content inside layout
    const contentSlot = document.querySelector("#content");
    const pageContent = document.getElementById(pageContentId);

    if (contentSlot && pageContent){
        contentSlot.appendChild(pageContent);
        pageContent.style.display = "block";
    } else {
        // Fallback error check
        console.error("Content slot (#content) or page content could not be found.");
    }
}