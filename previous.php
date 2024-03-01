<?php
// Read raw JSON data from the request
$input_json = file_get_contents('php://input');

// Decode the JSON data
$input_data = json_decode($input_json, true);

// Check if decoding was successful
if (isset($input_data['email'])) {
    // Extract the 'email' value
    $email = $input_data['email'];
    // echo "Received email: " . $email;
    $host = 'localhost';
    $user = 'root';
    $password = '';
    $database = 'truetalent';

    // Create a new connection
    $conn = new mysqli($host, $user, $password, $database);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    else{
        $query = "SELECT * FROM users WHERE email = '$email'";
        $result = $conn->query($query);

        if ($result) {
            // Check if any rows are returned
            if ($result->num_rows > 0) {
                // Loop through each row
                while ($row = $result->fetch_assoc()) {
                    echo "" . $row['dateTime'];
                    echo "<br>";
                     // Add a line break for better readability
                }
            } else {
                echo "Email is not available";
            }
            // Free result set
            $result->free();
        } else {
            echo "Error: " . $conn->error;
        }
    }
} else {
    echo "Error: Email parameter is missing";
}

?>


