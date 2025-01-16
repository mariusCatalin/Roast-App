async function uploadImage() {
    const imageUpload = document.getElementById('imageUpload');
    const roastResult = document.getElementById('roastResult');
    const uploadedImage = document.getElementById('uploadedImage');

    const file = imageUpload.files[0];

    if (!file) {
        roastResult.textContent = "Please select an image first.";
        return;
    }

    const formData = new FormData();
    formData.append('image', file);
    roastResult.textContent = "Loading...";
    uploadedImage.src = URL.createObjectURL(file);
    uploadedImage.style.display = 'block';

    try {
        const response = await fetch('/roast', {
            method: 'POST',
            body: formData,
        });
    
        const data = await response.json();
        if (response.ok) {
            roastResult.textContent = data.roast;
        } else {
            roastResult.textContent = "Error: " + (data.error || "Something went wrong");
        }
    } catch (error) {
        roastResult.textContent = "Network Error: Could not connect to the server";
        console.error('Error:', error);
    }
}