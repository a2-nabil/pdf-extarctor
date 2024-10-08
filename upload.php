<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['pdf'])) {
    // Ensure the uploaded file is a PDF
    $file = $_FILES['pdf'];
    $filePath = 'uploads/' . basename($file['name']);
    
    // Move the uploaded file to the uploads directory
    if (move_uploaded_file($file['tmp_name'], $filePath)) {
        // Execute the Python script to extract text and images
        $command = escapeshellcmd("python extract.py " . escapeshellarg($filePath));
        $output = shell_exec($command);
        
        // Prepare extracted data for display
        $outputLines = explode("\n", trim($output));
        $textFields = [];
        $imageFields = [];
        
        foreach ($outputLines as $line) {
            if (strpos($line, 'Saved image:') !== false) {
                // Extract image filenames
                $imageFields[] = trim(str_replace("Saved image: ", "", $line));
            } else {
                // Extract text
                $textFields[] = trim($line);
            }
        }

        // Display the extracted data in the existing form
        echo "<h2>Extracted Data:</h2>";
        echo '<form id="extractedDataForm" action="" method="POST">';
        
        // Add image file inputs
        for ($i = 0; $i < count($imageFields); $i++) {
            echo '<input type="file" name="img-' . ($i + 1) . '" id="img-' . ($i + 1) . '" value="' . htmlspecialchars($imageFields[$i]) . '" readonly>';
        }

        // Add text inputs
        for ($i = 0; $i < count($textFields); $i++) {
            echo '<input type="text" name="text-' . ($i + 1) . '" id="text-' . ($i + 1) . '" value="' . htmlspecialchars($textFields[$i]) . '">';
        }

        // Fill in additional text fields if needed
        for ($i = count($textFields); $i < 6; $i++) {
            echo '<input type="text" name="text-' . ($i + 1) . '" id="text-' . ($i + 1) . '">';
        }

        echo '<input type="submit" value="Submit">';
        echo '</form>';
    } else {
        echo "Failed to upload the file.";
    }
}
?>
