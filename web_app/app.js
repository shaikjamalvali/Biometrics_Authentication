const API_BASE = "http://localhost:8000"; // change if needed

/*
Should Return this JSON on Success:
{
  "message": "User registered successfully"
}
Else:
{
  "message": "Error message"
}
*/
async function registerUser() {
    const userId = document.getElementById("regUserId").value;

    const fingerprint = document.getElementById("regFingerprint").files[0];
    const face = document.getElementById("regFace").files[0];
    const iris = document.getElementById("regIris").files[0];
    const voice = document.getElementById("regVoice").files[0];

    if (!userId || !fingerprint || !face || !iris || !voice) {
        alert("Please provide all inputs");
        return;
    }

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("fingerprint", fingerprint);
    formData.append("face", face);
    formData.append("iris", iris);
    formData.append("voice", voice);

    const status = document.getElementById("regStatus");
    status.innerText = "Registering...";

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        status.innerText = result.message || "Registration successful";
    } catch (err) {
        console.error(err);
        status.innerText = "Registration failed";
    }
}

/*
{
  "success": true,
  "user_id": "abc123"
}
OR
{
  "success": false
}

*/

async function authenticateUser() {
    const fingerprint = document.getElementById("authFingerprint").files[0];
    const face = document.getElementById("authFace").files[0];
    const iris = document.getElementById("authIris").files[0];
    const voice = document.getElementById("authVoice").files[0];

    if (!fingerprint || !face || !iris || !voice) {
        alert("Please provide all inputs");
        return;
    }

    const formData = new FormData();
    formData.append("fingerprint", fingerprint);
    formData.append("face", face);
    formData.append("iris", iris);
    formData.append("voice", voice);

    const status = document.getElementById("authStatus");
    status.innerText = "Authenticating...";

    try {
        const response = await fetch(`${API_BASE}/authenticate`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            status.innerText = `Authenticated as User ID: ${result.user_id}`;
            status.style.color = "green";
        } else {
            status.innerText = "Authentication failed";
            status.style.color = "red";
        }
    } catch (err) {
        console.error(err);
        status.innerText = "Authentication failed";
    }
}
