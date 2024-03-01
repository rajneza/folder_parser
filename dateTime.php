<?php
// Read raw JSON data from the request
$input_json = file_get_contents('php://input');


// Decode the JSON data
$input_data = json_decode($input_json, true);

// Check if decoding was successful
if (isset($input_data['date'])) {
    // Extract the 'email' value
    $date = $input_data['date'];
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
        $query = "SELECT * FROM users WHERE dateTime = '$date'";
        $result = $conn->query($query);
        if ($result) {
            // Check if any rows are returned
            if ($result->num_rows > 0) {
                $row = $result->fetch_assoc();
        
                // Print the values of all four columns
                echo "" . $row['newfile'];
                echo ", " . $row['oldfile'];
                echo ", " . $row['duplicatefile'];
                echo ", " . $row['noEmail'];
            }
        }
    }
}
?>