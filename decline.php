<?php
// Read raw JSON data from the request
$input_json = file_get_contents('php://input');

// Decode JSON data
$input_data = json_decode($input_json, true);

// Check if decoding was successful
if ($input_data === null) {
    // JSON decoding failed
    echo "Error decoding JSON data";
} else {
    $accept_data = $input_data['accept'];
    $email = $input_data['email'];
    $date = $input_data['date'];
    
    $host = 'localhost';
    $user = 'root';
    $password = '';
    $database = 'truetalent';

    // Create a new connection
    $conn = new mysqli($host, $user, $password, $database);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } else {
        // If both email and accept_data are provided
        if (!empty($date) && !empty($email) && !empty($accept_data)) {
            // Check if 'result' column is empty for the provided email and date
            $check_query = "SELECT result FROM users WHERE email = '$email' AND dateTime = '$date'";
            $check_result = $conn->query($check_query);
            if ($check_result && $check_result->num_rows > 0) {
                $row = $check_result->fetch_assoc();
                $current_result = $row['result'];
                if (empty($current_result)) {
                    // Update the column 'result' with 'accept_data' value for the row with matching email and date
                    $escaped_accept_data = $conn->real_escape_string($accept_data);
                    $update_query = "UPDATE users SET result = '$escaped_accept_data' WHERE email = '$email' AND dateTime = '$date'";
                    $update_result = $conn->query($update_query);
                    if ($update_result) {
                        echo 'Value updated for the row with the provided email and date';
                    } else {
                        echo 'Failed to update value';
                    }
                } else {
                    echo 'The result is already set and cannot be changed.';
                }
            } else {
                echo 'No matching record found for the provided email and date';
            }
        }
        else if (!empty($date) && !empty($email)) {
            $query = "SELECT result FROM users WHERE email = '$email' AND dateTime = '$date'";
            $result = $conn->query($query);

            if ($result && $result->num_rows > 0) {
                $row = $result->fetch_assoc();
                $result_value = $row['result'];
                if (empty($result_value)) {
                    echo json_encode(array('result' => 'changable'));
                } else {
                    echo json_encode(array('result' => $result_value));
                }
            } else {
                echo 'No result found for the provided email and date';
            }
        } 
        // If all three parameters are provided
        else if (!empty($email) && !empty($accept_data)) {
            $query = "SELECT * FROM users WHERE email = '$email' ORDER BY `s.no` DESC LIMIT 1";
             $result = $conn->query($query);
 
             if ($result && $result->num_rows > 0) {
                 $row = $result->fetch_assoc();
                 $escaped_accept_data = $conn->real_escape_string($accept_data);
                 $email = $row['email'];
 
                 $update_query = "UPDATE users SET result = '$escaped_accept_data' WHERE `s.no` = " . $row['s.no'];
                 $update_result = $conn->query($update_query);
                 if ($update_result) {
                     echo 'Value changed for the last row with the provided email';
                 } else {
                     echo 'Failed to update value';
                 }
             } else {
                 echo 'No user found with the provided email';
             }
         } 
    }
}
?>
