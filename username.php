<?php
// Log the raw input data for debugging
file_put_contents('debug.txt', file_get_contents('php://input'));

// Retrieve the JSON data sent from the Python script
$input_data = json_decode(file_get_contents('php://input'), true);

// Check if the required keys are present in the JSON data
if (isset($input_data['email'], $input_data['domain'], $input_data['row_newfile'], $input_data['row_oldfile'], $input_data['row_duplicate'], $input_data['row_duplicate'], $input_data['none_email'])) {
    // Extract the data
    $email = $input_data['email'];
    $domain = $input_data['domain'];
    $row_newfile = $input_data['row_newfile'];
    $row_oldfile = $input_data['row_oldfile'];
    $row_duplicate = $input_data['row_duplicate'];
    $none_email = $input_data['none_email'];

    // Database connection parameters
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

    // Insert the data into the database
    $insert_query = "INSERT INTO users (email, domain, newfile, oldfile, duplicatefile, noEmail) 
                     VALUES ('$email', '$domain', $row_newfile, $row_oldfile, $row_duplicate, $none_email)";
                     
    if ($conn->query($insert_query) === TRUE) {
        // Return success response
        echo json_encode(['status' => 'success']);
    } else {
        // Return error response if insertion fails
        echo json_encode(['status' => 'error', 'message' => 'Error inserting record']);
    }

    // Close the connection
    $conn->close();
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON data']);
}
?>
