

async function registerNurse() {
        
    const fullname = document.getElementById('full_name').value;
    const email = document.getElementById('email').value;   
    const phonenumber = document.getElementById('phone_number').value;
    const password = document.getElementById('password').value;
    const gender = document.getElementById('gender').value;
    const  nationalID = document.getElementById('nationalID').value;
    console.log(phonenumber);
    console.log(gender);

    
  
    try {
      backendUrl='http://127.0.0.1:5000'
      const response = await fetch(`${backendUrl}/registerNurse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          fullname,
          email,
          phonenumber,
          password,
          gender,
          nationalID
          
        })
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Successfully created user. Redirecting...");
        window.location.href = data.redirectUrl;  // Redirect to provided URL
      } else {
        const errorData = await response.json();
        console.error("Error creating user:", errorData.error);
        // Handle error message display or other actions
      }
  
    } catch (error) {
      console.error("Error during request:", error);
      // Handle network errors or other exceptions
    }
  }

  registerNurse();